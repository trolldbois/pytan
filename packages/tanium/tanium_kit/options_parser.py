"""Options parser module."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os
import sys

from . import ask, store, text_type, tools
# from . import integer_types, string_types,

LOG = logging.getLogger(__name__.split(".")[-1])


class OptionsParser(object):
    """Options parser class."""

    CHECKS = [
        "check_empty",
        "check_bool",
        "check_int",
        "check_crypt",
        "check_abs",
        "check_choices",
        "check_list_sep",
        "check_tmpl",
        "add_parsed_full",
        "add_parsed_flat",
    ]

    SECURE_VALUES = [
        "password",
        "crypt_key",
        "secret",
    ]

    LOG = LOG

    def start(self, config, env_prefix="TANIUM", options=[], parsed_base={}, crypt_key=None):
        """Constructor."""
        self.CONFIG = config
        self.CRYPT_KEY = crypt_key
        self.ENV_PREFIX = env_prefix
        self.OPTIONS = options
        self.PARSED_BASE = parsed_base
        self.check_options()
        self.parse_options()

    def check_options(self):
        if not isinstance(self.OPTIONS, (list, tuple)):
            m = "Option definitions supplied is not a list: {!r}"
            m = m.format(self.OPTIONS)
            raise Exception(m)

        for option in self.OPTIONS:
            if not isinstance(option, dict):
                m = "Option definition supplied is not a dictionary: {!r}"
                m = m.format(option)
                raise Exception(m)

            if "section" not in option:
                m = "Option definition does not supply 'section': {!r}"
                m = m.format(option)
                raise Exception(m)

            if "entry" not in option:
                m = "Option definition does not supply 'entry': {!r}"
                m = m.format(option)
                raise Exception(m)

    def parse_options(self):
        self.PARSED_FULL = store.Store(**self.PARSED_BASE)

        self.PARSED_FLAT = store.Store()

        for k, v in self.PARSED_BASE.items():
            self.PARSED_FLAT.update(v)

        for option in self.OPTIONS:
            this_option = store.Store(**option)
            this_option["config"] = self.CONFIG
            self.parse_option(**this_option)

    def parse_option(self, **kwargs):
        """Get the value of an entry from a section from config.

        If value not supplied or is not the right type, prompt user for value.

        Parameters
        ----------
        section : :obj:`str`
            * section to look for ``entry`` as :attr:`OptionsParser.CONFIG`[section]
        entry : :obj:`str`
            * entry to look for in ``section`` as :attr:`OptionsParser.CONFIG`[section][entry]
        config
        prompt : :obj:`str`
            * Prompt to use when asking user for value
        is_bool : :obj:`bool`, optional
            * default: False
            * True: value of entry must be a boolean
            * False: value of entry does not have to be a boolean
        is_int : :obj:`bool`, optional
            * default: False
            * True: value of entry must be an integer
            * False: value of entry does not have to be an integer
        empty_ok : :obj:`bool`, optional
            * default: False
            * True: value of entry can be empty
            * False: value of entry can not be empty
        force_absolute : :obj:`bool`, optional
            * default: False
            * True: if value of entry is not an absolute path, prepend it with the path of THAT
            * False: leave value of entry alone
        is_crypt : :obj:`bool`, optional
            * default: False
            * True: run value of entry through :meth:`tanium_kit.tools.deobfuscate`
            * False: leave value of entry alone
        list_separator
        list_stripper
        choices
        lower_choices
        is_template
        default
        on_invalid
        quiet_template
        is_password
        prompt
        dependencies
        on_empty_subsections
        """
        if not self.dependencies_met(**kwargs):
            return

        if self.is_sub_section(**kwargs):
            return

        if self.is_sub_entry(**kwargs):
            return

        kwargs = self.value_defined(**kwargs)

        for self.CHECK in self.CHECKS:
            check_method = getattr(self, self.CHECK)
            kwargs = check_method(**kwargs)

    def is_sub_entry(self, **kwargs):
        section = kwargs["section"]
        config = kwargs["config"]
        sub_section = kwargs.get("sub_section", "")
        section_config = config.get(section, {})
        entry = kwargs["entry"]
        on_empty_subentries = kwargs.get("on_empty_subentries", "info")

        ret = False

        if entry.endswith("__"):
            ret = True

            sub_entries = store.Store(**{k: v for k, v in section_config.items() if k.startswith(entry)})

            if not sub_entries and entry not in self.PARSED_FULL.get(section, {}):

                m = "No entries found matching: {} in section: {}::{}"
                m = m.format(entry, section, sub_section)

                if on_empty_subentries == "debug":
                    self.LOG.debug(m)
                elif on_empty_subentries == "info":
                    self.LOG.info(m)
                elif on_empty_subentries == "warning":
                    self.LOG.warning(m)
                else:
                    self.LOG.error(m)
                    raise Exception(m)

            sub_dict = {}
            for sub_entry, sub_value in sub_entries.items():
                _, sub_entry = sub_entry.split("__", 1)
                sub_dict[sub_entry] = sub_value

            this_option = dict(**kwargs)
            this_option["entry"] = entry.rstrip("__")
            this_option["value"] = sub_dict

            self.add_parsed_full(**this_option)
            self.add_parsed_flat(**this_option)

        return ret

    def is_sub_section(self, **kwargs):
        section = kwargs["section"]
        config = kwargs["config"]
        on_empty_subsections = kwargs.get("on_empty_subsections", "warning")

        ret = False

        if section.endswith("::"):
            ret = True

            sub_section_name = section.rstrip("::")
            sub_configs = store.Store(**{k: v for k, v in config.items() if k.startswith(section)})

            if not sub_configs and sub_section_name not in self.PARSED_FULL:
                self.PARSED_FULL[sub_section_name] = store.Store()
                self.PARSED_FLAT[sub_section_name] = store.Store()

                m = "No sections found matching: {}"
                m = m.format(section)

                if on_empty_subsections == "debug":
                    self.LOG.debug(m)
                elif on_empty_subsections == "info":
                    self.LOG.info(m)
                elif on_empty_subsections == "warning":
                    self.LOG.warning(m)
                else:
                    self.LOG.error(m)
                    raise Exception(m)

            for sub_name, sub_config in sub_configs.items():
                sub_name = sub_name.split("::", 1)[1]

                this_option = dict(**kwargs)
                this_option["section"] = sub_section_name
                this_option["config"] = store.Store(**{sub_section_name: sub_config})
                this_option["sub_section"] = sub_name
                self.parse_option(**this_option)
        return ret

    def is_invalid(self, msg, **kwargs):
        section = kwargs["section"]
        entry = kwargs["entry"]
        ret = kwargs.get("value", None)

        sub_section = kwargs.get("sub_section", None)
        src_section = "{}::{}".format(section, sub_section) if sub_section else section

        on_invalid = kwargs.get("on_invalid", "ask")
        # ask, error, exit, default

        show_val = self.hide_value(**kwargs)
        tpre = "Section [{}], Option '{}', Value {!r}, Check '{}()' - "
        tpre = tpre.format(src_section, entry, show_val, self.CHECK)

        if on_invalid == "ask":
            m = "{}{}, prompting for value"
            m = m.format(tpre, msg)
            self.LOG.warning(m)
            ret = ask.ask(**kwargs)
        elif on_invalid == "error":
            m = "{}{}, error"
            m = m.format(tpre, msg)
            self.LOG.error(m)
            raise Exception(m)
        elif on_invalid == "exit":
            m = "{}{}, exiting"
            m = m.format(tpre, msg)
            self.LOG.error(m)
            sys.exit(99)
        elif on_invalid == "default":
            if "default" in kwargs:
                default = kwargs["default"]
                m = "{}{}, using default value of '{}'"
                m = m.format(tpre, msg, default)
                self.LOG.warning(m)
                ret = default
            else:
                m = "{}{}, but no default value supplied!"
                m = m.format(tpre, msg)
                self.LOG.warning(m)
                ret = ask.ask(**kwargs)
        else:
            m = "{}{}, bad 'on_invalid': '{}'"
            m = m.format(tpre, msg, on_invalid)
            self.LOG.error(m)
            raise Exception(m)

        return ret

    def is_skip(self, **kwargs):
        section = kwargs["section"]
        entry = kwargs["entry"]

        show_val = self.hide_value(**kwargs)
        tpre = "Section [{}], Option '{}', Value {!r}, Check '{}()' - "
        tpre = tpre.format(section, entry, show_val, self.CHECK)

        m = "{}check skipped, option not supplied"
        m = m.format(tpre)
        self.LOG.debug(m)

    def is_valid(self, msg, **kwargs):
        section = kwargs["section"]
        entry = kwargs["entry"]

        show_val = self.hide_value(**kwargs)
        tpre = "Section [{}], Option '{}', Value {!r}, Check '{}()' - "
        tpre = tpre.format(section, entry, show_val, self.CHECK)

        m = "{}{}"
        m = m.format(tpre, msg)
        self.LOG.debug(m)

    def is_secure(self, **kwargs):
        prompt = kwargs.get("prompt", "")
        entry = kwargs.get("entry", "")
        secure_values = kwargs.get("secure_values", self.SECURE_VALUES)
        is_password = kwargs.get("is_password", False)

        if is_password:
            return True

        for x in secure_values:
            if x.lower() in prompt.lower():
                return True
            if x.lower() in entry.lower():
                return True

        return False

    def hide_value(self, **kwargs):
        ret = "**HIDDEN**" if self.is_secure(**kwargs) else kwargs["value"]
        return ret

    def find_section_path(self, section_path, source):
        for i in section_path.split("/"):
            if i in source:
                source = source[i]
            else:
                source = None
                break
        return source

    def dependencies_met(self, **kwargs):
        section = kwargs["section"]
        entry = kwargs["entry"]

        # "dependencies": {["main", "port"]: 443},
        dependencies = kwargs.get("dependencies", {})

        self.CHECK = "dependencies_met"

        tpre = "Section [{}], Option '{}', {} - "
        tpre = tpre.format(section, entry, self.CHECK)

        ret = True
        for section_path, check_value in dependencies.items():

            section_value = self.find_section_path(section_path, self.PARSED_FULL)

            if section_value is None:
                m = "dependency '{}' not defined"
                m = m.format(tpre, section_value)
                self.LOG.debug(m)
                ret = False
                break

            if check_value is not None:
                if check_value != section_value:
                    m = "dependency '{}' defined but does not meet check_value '{}'"
                    m = m.format(tpre, section_value, check_value)
                    self.LOG.debug(m)
                    ret = False
                    break
            else:
                m = "dependency '{}' = '{}' met"
                m = m.format(tpre, section_value, check_value)
                self.LOG.debug(m)

        m = "{}parsing option: '{}'"
        m = m.format(tpre, ret)
        self.LOG.debug(m)

        return ret

    def value_defined(self, **kwargs):
        """Check if value is defined in :attr:`OptionsParser.CONFIG`.

        * Checks :data:`os.environ` for ${ENV_PREFIX}_${ENTRY} and uses that as value if defined
        * Checks if :attr:`OptionsParser.CONFIG` is defined/is a dict, asks user for value if not
        * Checks :attr:`OptionsParser.CONFIG` for entry and uses that as value if found
        """
        section = kwargs["section"]
        entry = kwargs["entry"]
        config = kwargs["config"]
        kwargs["value"] = config.get(section, {}).get(entry, None)

        self.CHECK = "value_defined"
        env_entry = "{}_{}".format(self.ENV_PREFIX, entry).upper()

        if env_entry in os.environ:
            kwargs["value"] = os.environ[env_entry]
            self.is_valid("Environment Variable '{}' override provided".format(env_entry), **kwargs)
        elif not config:
            kwargs["value"] = self.is_invalid("Empty Configuration", **kwargs)
        elif not isinstance(config, dict):
            kwargs["value"] = self.is_invalid("Configuration not parsed properly", **kwargs)
        elif section not in config:
            kwargs["value"] = self.is_invalid("Section missing from configuration", **kwargs)
        elif entry not in config[section]:
            kwargs["value"] = self.is_invalid("Entry missing from configuration", **kwargs)
        else:
            kwargs["value"] = config[section][entry]
            self.is_valid("Configuration provided value", **kwargs)
        return kwargs

    def check_crypt(self, **kwargs):
        """Check if value is cryptable.

        Parameters
        ----------
        is_crypt : :obj:`bool`, optional
            * default : False
            * True : value is could be a crypted value, use :func:`tanium_kit.tools.deobfuscate` to convert it
            * False : leave value alone
        """
        is_crypt = kwargs.get("is_crypt", False)

        if is_crypt:
            self.is_valid("Trying to deobfuscate", **kwargs)
            kwargs["value"] = tools.deobfuscate(key=self.CRYPT_KEY, text=kwargs["value"])
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_empty(self, **kwargs):
        """Check if value is empty.

        Parameters
        ----------
        empty_ok : :obj:`bool`, optional
            * default : False
            * True : value is allowed to be empty
            * False : value is not allowed to be empty, re-ask user if it is empty
        """
        empty_ok = kwargs.get("empty_ok", False)

        if kwargs["value"] in [None, ""]:
            if not empty_ok:
                kwargs["value"] = self.is_invalid("Requires a non-empty value", **kwargs)
            else:
                self.is_valid("Empty value allowed", **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_bool(self, **kwargs):
        """Convert value into boolean.

        Parameters
        ----------
        is_bool : :obj:`bool`, optional
            * default : False
            * True : value should be converted to bool using :func:`tanium_kit.ask.coerce_bool`, ask user if it fails to be converted
            * False : leave value alone
        """
        is_bool = kwargs.get("is_bool", False)

        if is_bool:
            check = ask.coerce_bool(kwargs["value"])
            if check is None:
                kwargs["value"] = self.is_invalid("Requires a valid boolean value", **kwargs)
            else:
                kwargs["value"] = check
                self.is_valid("Value is a valid boolean", **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_int(self, **kwargs):
        """Convert value into integer.

        Parameters
        ----------
        is_int : :obj:`bool`, optional
            * default : False
            * True : value should be converted to int using :func:`tanium_kit.tools.int_check`, ask user if it fails to be converted
            * False : leave value alone
        """
        is_int = kwargs.get("is_int", False)

        if is_int:
            check = tools.int_check(kwargs["value"])
            if check is None:
                kwargs["value"] = self.is_invalid("Requires a valid integer value", **kwargs)
            else:
                kwargs["value"] = check
                self.is_valid("Value is a valid integer", **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_choices(self, **kwargs):
        """Check that value is in list of valid choices.

        Parameters
        ----------
        choices : :obj:`list` or :obj:`str`, optional
            * default : []
            * choices to check against
        lower_choices
        """
        choices = kwargs.get("choices", [])
        lower_choices = kwargs.get("lower_choices", True)

        if choices:
            found_valid = False
            for vc in choices:
                check = text_type(vc).lower() if lower_choices else vc
                val = text_type(kwargs["value"]).lower() if lower_choices else vc
                if val == check:
                    found_valid = True
                    kwargs["value"] = vc

            vcs = ", ".join(choices)
            if not found_valid:
                kwargs["value"] = self.is_invalid("Must be one of {}".format(vcs), **kwargs)
            else:
                self.is_valid("Is one of {}".format(vcs), **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_list_sep(self, **kwargs):
        """Convert value into list based on separator.

        Parameters
        ----------
        list_separator : :obj:`str`, optional
            * default : False
            * :obj:`str` : separator to use to split string into list
            * False : leave value alone
        list_stripper
        """
        list_separator = kwargs.get("list_separator", False)
        list_stripper = kwargs.get("list_stripper", False)  # left, right, both, False

        if list_separator:
            value = kwargs["value"]
            value = value.split(list_separator)
            value = [x for x in value if x.strip() != ""]
            self.is_valid("Split into list on {!r}".format(list_separator), **kwargs)

            if list_stripper == "left":
                value = [x.lstrip() for x in value]
            elif list_stripper == "right":
                value = [x.rstrip() for x in value]
            elif list_stripper == "both":
                value = [x.strip() for x in value]
            elif list_stripper is False:
                pass
            else:
                value = [x.strip(list_stripper) for x in value]
            kwargs["value"] = value
            self.is_valid("List stripped: {}".format(list_stripper), **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_tmpl(self, **kwargs):
        """Templatize value.

        Parameters
        ----------
        is_template : :obj:`bool`, optional
            * default : False
            * True : value should be templatized using :meth:`OptionsParser.tmpl`
            * False : leave value alone
        """
        is_template = kwargs.get("is_template", False)

        if is_template:
            kwargs["value"] = self.tmpl(kwargs["value"], **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def check_abs(self, **kwargs):
        """Pre-pend value if it is not absolute.

        Parameters
        ----------
        force_absolute : :obj:`bool`, optional
            * default : False
            * str : value should be prefixed with str if value is not absolute
            * False : leave value alone
        """
        force_absolute = kwargs.get("force_absolute", False)

        if force_absolute:
            if not os.path.isabs(kwargs["value"]):
                force_absolute = self.tmpl(force_absolute, **kwargs)
                kwargs["value"] = os.path.join(force_absolute, kwargs["value"])
                self.is_valid("forced to absolute path", **kwargs)
            else:
                self.is_valid("already absolute path", **kwargs)
        else:
            self.is_skip(**kwargs)
        return kwargs

    def tmpl(self, value, **kwargs):
        """Templatize a value.

        Parameters
        ----------
        value : :obj:`str`
            * string to templatize using :attr:`tanium_hat.main.Main.PCONFIG`
        """
        try:
            value = value.format(**self.PARSED_FLAT)
            self.is_valid("Template successful")
        except Exception as e:
            value = self.is_invalid("Invalid template, error: {}".format(e), **kwargs)
        return value

    def add_parsed_full(self, **kwargs):
        section = kwargs["section"]
        entry = kwargs["entry"]
        value = kwargs["value"]
        sub_section = kwargs.get("sub_section", None)

        if section not in self.PARSED_FULL:
            self.is_valid("added section", **kwargs)
            self.PARSED_FULL[section] = store.Store()
        else:
            self.is_valid("section already exists", **kwargs)

        if sub_section:
            if sub_section not in self.PARSED_FULL[section]:
                self.PARSED_FULL[section][sub_section] = store.Store()
                self.is_valid("added sub_section for section", **kwargs)
            else:
                self.is_valid("sub_section for section already exists", **kwargs)

            self.PARSED_FULL[section][sub_section][entry] = value
            self.is_valid("added value for option in sub_section for section", **kwargs)
        else:
            self.PARSED_FULL[section][entry] = value
            self.is_valid("added value for option in section", **kwargs)
        return kwargs

    def add_parsed_flat(self, **kwargs):
        section = kwargs["section"]
        entry = kwargs["entry"]
        value = kwargs["value"]
        sub_section = kwargs.get("sub_section", None)

        if sub_section:
            if section not in self.PARSED_FLAT:
                self.is_valid("added section for sub_section", **kwargs)
                self.PARSED_FLAT[section] = store.Store()
            else:
                self.is_valid("section for sub_section already exists", **kwargs)

            if sub_section not in self.PARSED_FLAT[section]:
                self.is_valid("added sub_section for section", **kwargs)
                self.PARSED_FLAT[section][sub_section] = store.Store()
            else:
                self.is_valid("sub_section for section already exists", **kwargs)

            self.PARSED_FLAT[section][sub_section][entry] = value
            self.is_valid("added value for option in sub_section for section", **kwargs)
        else:
            self.PARSED_FLAT[entry] = value
            self.is_valid("added value for option", **kwargs)
        return kwargs
