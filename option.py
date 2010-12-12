#!/usr/bin/python
# coding: utf8

"""
options.py
-----------

This module cares about the configuration of pyalpmm and if you want to: its
applications. PyChmViewerConfig at the bottom is the actual configuration
handler class. It defines all configuration options explicitly, describing its
properties.

All ConfigItem instances and derivates take two arguments: at first
the 'section' the option belongs to and then the default-value, which
should be used (optional).

After these definitions, the __init__ has to construct the filename for the
config file and then just call the super().__init__() and the ConfigMapper
instance gets populated with the data from the input file.
"""

from StringIO import StringIO
from ConfigParser import RawConfigParser

class ConfigError(Exception):pass


class ConfigItem(object):
    """The baseclass for all *ConfigItem instances. One ConfigItem represents
    one option and its value inside the ConfigMapper class.

    As long as used as an object attribute it behaves like a simple data type,
    but actually is a descriptor with also holds additional data for this
    option.

    Each derived class has to set those two class-attributes:

    - converter: a callable which converts the input (str) into the
                 representation of the wanted data type
    - default: a default value, which is taken if neither the instance defined
               a default nor the config file has an entry for this option
    """
    # this method is called for data that is read
    inconv = lambda s, v: v
    # and this one is called for data to be written
    outconv = lambda s, v: v

    default = None

    def __init__(self, section, default_value=None):
        self.section = section
        self.value = default_value or self.default
        # this is set inside ConfigMapper.__init__
        self.name = None

    def __get__(self, obj, owner):
        return self.value
    def __set__(self, obj, val):
        self.value = val

    def __repr__(self):
        return "<{0} name={1} val=\"{2}\" section=\"{3}\">".format(
            self.__class__.__name__,
            self.name, self.value, self.section
        )

class StringConfigItem(ConfigItem):
    """Holds a string of config data"""
    inconv = lambda s, v: str(v)
    outconv = lambda s, v: str(v)
    default = ""

class IntegerConfigItem(ConfigItem):
    """Holds an integer of config data"""
    inconv = lambda s, v: int(v)
    outconv = lambda s, v: str(v)
    default = 0

class ListConfigItem(ConfigItem):
    """Holds a list of config data"""
    inconv = lambda s, v: [x.strip() for x in
                              (v.split(",") if "," in v else v.split(" "))]
    outconv = lambda s, v: ",".join(v)
    default = []

    def __iter__(self):
        for item in self.value:
            yield item

    def __getitem__(self, key):
        return self.value[key]

    def __len__(self):
        return len(self.value)

class YesNoConfigItem(ConfigItem):
    """Is either True or False"""
    inconv = lambda s, v: v.lower() == "yes" if v.lower() in ["no", "yes"] \
              else bool(v)
    outconv = lambda s, v: "yes" if v else "no"
    default = False

class CommandlineItem(ConfigItem):
    """A special ConfigItem, which is passed through the commandline"""
    default = False

    def __init__(self, default_value=None):
        super(CommandlineItem, self).__init__(None, default_value)

class ConfigMapper(object):
    """The baseclass for a ConfigMapper class.
    The idea is to define your configuration options as precise as possible
    and the let the ConfigMapper do the rest, including r/w a configfile,
    convert into the needed data types and provide the right default values,
    if needed.

    You just define attributes in your CustomConfigMapper class like this:
    class CustomConfigMapper(ConfigMapper):
        path = StringConfigItem("general")
        other_path = StringConfigItem("foo", "my_default_value")
        alist = ListConfigItem("foo", [1,2,3,4])
        .
        .
        special_easter_egg = CommandlineItem(False)
        .
    Then call it with a 'stream' (means .read() must be available) and a
    options object from 'optparse', or something that behaves like it. You will
    get a fully populated CustomConfigMapper object already up-to-date with
    your config file.
    """
    config_items = {}

    # if strict is True, _all_ config options MUST be set in the config
    strict = False

    def __init__(self, stream=None):
        # all ConfigurationItems in class
        all_confs = ((name, attr) \
                     for name, attr in self.__class__.__dict__.items() \
                     if isinstance(attr, ConfigItem))

        # as an attribute doesn't know his own name automaticly, set it!
        # further append all Items to their appropriate lists:
        #    - config_items for ConfigItems
        for name, attr in all_confs:
            attr.name = name
            self.config_items[name] = attr

        self.stream = stream or StringIO()
        self.confobj = RawConfigParser()
        self.confobj.readfp(self.stream)

        # actually read the data from the file
        self.read_from_file()

    def __getitem__(self, key):
        if key in self:
            return self.config_items[key]
        raise KeyError("'{0}' is not an existing config key".format(key))

    def __contains__(self, key):
        return key in self.cmdline_items.keys()

    def __iter__(self):
        for k, v in self.config_items.items():
            yield (k, v)

    def read_from_file(self):
        """Read configuration from file into the object attributes"""
        for item in self.config_items.values():
            if self.confobj.has_option(item.section, item.name):
                item.value = item.inconv(self.confobj.get(item.section, item.name).strip())
            elif self.strict:
                raise ConfigError("Didn't find section: %s with option: %s" % (
                    item.section,
                    item.name
                ))

    def save_into_file(self, path):
        """Write the default config settings to a file"""
        conf_obj = RawConfigParser()
        written_sections = []
        for k, v in self.config_items.items():
            if v.section not in written_sections:
                written_sections.append(v.section)
                conf_obj.add_section(v.section)
            conf_obj.set(v.section, k, v.outconv(v.value))

        with open(path, "w") as stream:
            conf_obj.write(stream)



class PyChmViewerConfig(ConfigMapper):
    """The through the whole pyalpmm library used config class, usually there
    should be an instance of it around as attribute from a Session instance
    """

    defaultencoding = StringConfigItem("userconfig", "gb18030")
    fontfamily   = StringConfigItem("userconfig", "")
    fontsize     = IntegerConfigItem("userconfig", 10)
    session_restore = YesNoConfigItem("userconfig", True)
    openRemoteURL   = YesNoConfigItem("userconfig", True)

    lastdir = StringConfigItem("userdata", ".")

    def __init__(self, path):
        try:
            stream = open(path)
        except IOError:
            stream = None

        #with open(path) as stream:
        super(PyChmViewerConfig, self).__init__( stream )

        self.path = path

    def save_into_file(self, path=None):
        path = path or self.path
        super(PyChmViewerConfig, self).save_into_file(path)


    def __str__(self):
        """Showing all config options"""
        o  = "Showing all Configuration options:\n"
        o += "--------------------------------\n"
        for k,v in self.config_items.items():
            o += "{0:20} = {1}\n".format(k, v)

        return o

