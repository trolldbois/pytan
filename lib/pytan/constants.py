"""PyTan Constants

This contains a number of constants that drive PyTan.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

# debug log format
DEBUG_FORMAT = (
    "[%(lineno)-5d - %(filename)20s:%(funcName)s()] %(asctime)s\n%(levelname)-8s %(name)s %(message)s"
)
"""
Logging format for debugformat=True
"""

# info log format
INFO_FORMAT2 = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
"""
Logging format for debugformat=False
"""
INFO_FORMAT1 = "%(asctime)s [%(name)s] [%(funcName)s] %(levelname)-8s %(message)s"
INFO_FORMAT = "[%(name)s] [%(funcName)s] %(levelname)-8s %(message)s"

# log levels to turn on extra loggers (higher the level the more verbose)
LOG_LEVEL_MAPS = [
    (
        0,
        {
            "stats": "DEBUG",
            "method_debug": "DEBUG",
        },
        "Sets all loggers to only output at WARNING or above except for stats & method_debug",
    ),
    (
        1,
        {
            "pytan": "INFO",
            "pytan.pollers.QuestionPoller": "INFO",
            "pytan.pollers.ActionPoller": "INFO",
            "pytan.pollers.SSEPoller": "INFO",
        },
        "Pytan poller loggers show output at INFO or above",
    ),
    (
        2,
        {
            "pytan": "DEBUG",
            "pytan.handler": "INFO",
            "pytan.pollers.QuestionPoller.progress": "INFO",
            "pytan.pollers.ActionPoller.progress": "INFO",
            "pytan.pollers.SSEPoller.progress": "INFO",
            "pytan.pollers.QuestionPoller": "DEBUG",
            "pytan.pollers.ActionPoller": "DEBUG",
            "pytan.pollers.SSEPoller": "DEBUG",
        },
        "Pytan handler logger show output at INFO or above, poller logs at DEBUG or above, and poller progress logs at INFO or above",
    ),
    (
        3,
        {
            "pytan.handler": "DEBUG",
            "pytan.pollers.QuestionPoller.progress": "DEBUG",
            "pytan.pollers.ActionPoller.progress": "DEBUG",
            "pytan.pollers.SSEPoller.progress": "DEBUG",
            "pytan.pollers.QuestionPoller.resolver": "INFO",
            "pytan.pollers.ActionPoller.resolver": "INFO",
            "pytan.pollers.SSEPoller.resolver": "INFO",
        },
        "Pytan handler logger show output at DEBUG or above, poller progress at DEBUG or above, and poller resolver at INFO or above",
    ),
    (
        4,
        {
            "pytan.ask_manual": "DEBUG",
            "pytan.pollers.QuestionPoller.resolver": "DEBUG",
            "pytan.pollers.ActionPoller.resolver": "DEBUG",
            "pytan.pollers.SSEPoller.resolver": "DEBUG",
        },
        "Pytan ask manual logger show output at DEBUG or above and poller resolver at DEBUG or above",
    ),
    (
        5,
        {
            "pytan.parser": "DEBUG",
        },
        "Pytan parser logger show output at DEBUG or above",
    ),
    (
        6,
        {
            "pytan.handler.timing": "DEBUG",
            "XMLCleaner": "DEBUG",
        },
        "Pytan timing and XMLCleaner loggers show output at DEBUG or above",
    ),
    (
        7,
        {
            "pytan.sessions.Session": "DEBUG",
        },
        "Taniumpy session loggers show output at DEBUG or above",
    ),
    (
        8,
        {
            "pytan.sessions.Session.auth": "DEBUG",
        },
        "PyTan session authentication loggers show output at DEBUG or above",
    ),
    (
        9,
        {
            "pytan.sessions.Session.http": "DEBUG",
        },
        "PyTan session http loggers show output at DEBUG or above",
    ),
    (
        10,
        {
            "pytan.handler.prettybody": "DEBUG",
        },
        "Pytan handler pretty XML body loggers show output at DEBUG or above",
    ),
    (
        11,
        {
            "pytan.sessions.Session.http.body": "DEBUG",
        },
        "PyTan session raw XML body loggers show output at DEBUG or above",
    ),
    (
        12,
        {
            "requests": "DEBUG",
            "requests.packages.urllib3": "DEBUG",
            "requests.packages.urllib3.connectionpool": "DEBUG",
            "requests.packages.urllib3.poolmanager": "DEBUG",
            "requests.packages.urllib3.util.retry": "DEBUG",
        },
        "Requests package show logging at DEBUG or above",
    ),

]
"""
Map for loglevel(int) -> logger -> logger level(logging.INFO|WARN|DEBUG|...). Higher loglevels will include all levels up to and including that level. Contains a list of tuples, each tuple consisting of:
    * int, loglevel
    * dict, `{{logger_name: logger_level}}` for this loglevel
    * str, description of this loglevel
"""

SENSOR_TYPE_MAP = {
    0: "Hash",
    # SENSOR_RESULT_TYPE_STRING
    1: "String",
    # SENSOR_RESULT_TYPE_VERSION
    2: "Version",
    # SENSOR_RESULT_TYPE_NUMERIC
    3: "NumericDecimal",
    # SENSOR_RESULT_TYPE_DATE_BES
    4: "BESDate",
    # SENSOR_RESULT_TYPE_IPADDRESS
    5: "IPAddress",
    # SENSOR_RESULT_TYPE_DATE_WMI
    6: "WMIDate",
    #  e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes:
    # "TimeDiff", and 3.67 seconds" or "4.2 hours"
    # (numeric + "Y|MO|W|D|H|M|S" units)
    7: "TimeDiff",
    #  e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
    8: "DataSize",
    9: "NumericInteger",
    10: "VariousDate",
    11: "RegexMatch",
    12: "LastOperatorType",
}
"""
Maps a Result type from the Tanium SOAP API from an int to a string
"""

EXPORT_MAPS = {
    "ResultSet": {
        "csv": [
            {
                "key": "header_sort",
                "valid_types": [bool, list, tuple],
                "valid_list_types": ["str", "unicode"],
            },
            {
                "key": "sensors",
                "valid_types": [list, tuple],
                "valid_list_types": ["taniumpy.Sensor"],
            },
            {
                "key": "header_add_sensor",
                "valid_types": [bool],
                "valid_list_types": [],
            },
            {
                "key": "header_add_type",
                "valid_types": [bool],
                "valid_list_types": [],
            },
            {
                "key": "expand_grouped_columns",
                "valid_types": [bool],
                "valid_list_types": [],
            },
        ],
        "json": [],
        "xml": [],
    },
    "BaseType": {
        "csv": [
            {
                "key": "header_sort",
                "valid_types": [bool, list, tuple],
                "valid_list_types": ["str", "unicode"],
            },
            {
                "key": "explode_json_string_values",
                "valid_types": [bool],
                "valid_list_types": [],
            },
        ],
        "json": [
            {
                "key": "include_type",
                "valid_types": [bool],
                "valid_list_types": [],
            },
            {
                "key": "explode_json_string_values",
                "valid_types": [bool],
                "valid_list_types": [],
            },
        ],
        "xml": [
            {
                "key": "minimal",
                "valid_types": [bool],
                "valid_list_types": [],
            },
        ]
    },

}
"""
Maps a given TaniumPy object to the list of supported export formats for each object type, and the valid optional arguments for each export format. Optional arguments construct:
    * key: the optional argument name itself
    * valid_types: the valid python types that are allowed to be passed as a value to `key`
    * valid_list_types: the valid python types in str format that are allowed to be passed in a list, if list is one of the `valid_types`
"""

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
"""
Tanium"s format for date time strings
"""

SSE_FORMAT_MAP = [
    ("csv", "0", 0),
    ("xml", "1", 1),
    ("xml_obj", "1", 1),
    ("cef", "2", 2),
]
"""
Mapping of human friendly strings to API integers for server side export
"""

SSE_RESTRICT_MAP = {
    1: ["6.5.314.4300"],
    2: ["6.5.314.4300"],
}
"""
Mapping of API integers for server side export format to version support
"""

SSE_CRASH_MAP = ["6.5.314.4300"]
"""
Mapping of versions to watch out for crashes/handle bugs for server side export
"""

PYTAN_USER_CONFIG = "~/.pytan_config.json"
"""
Default path to file to use for Handler parameter overrides
"""

PYTAN_KEY = "mT1er@iUa1kP9pelSW"
"""
Key used for obfuscation/de-obfsucation
"""

HANDLER_ARG_DEFAULTS = {
    "username": None,
    "password": None,
    "session_id": None,
    "host": None,
    "port": 443,
    "loglevel": 0,
    "gmt_log": False,
}
"""
Map of handler arguments and their defaults
"""

SESSION_ARG_DEFAULTS = {
    "host": "",
    "port": 443,
    "protocol": "https",
    "verify_ssl": "False",
    "port_fallback": 444,
    "session_fallback": True,
    "retry_count": 5,
    "record_all": False,
    "force_version": "",
    "connect_secs": 5,
    "connect_secs_soap": 15,
    "response_secs": 15,
    "response_secs_soap": 540,
    "clean_xml_restricted": True,
    "clean_xml_invalid": True,
    "http_proxy": "",
    "https_proxy": "",
    "request_headers": {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "{title}/{version}",
    },
}

# 3.0.0
CHECK_LIMIT_MAPS = [
    {"key": "limit_min", "msg": "items or more", "expr": ">=", "exc": "TooFewFoundError"},
    {"key": "limit_max", "msg": "items or less", "expr": "<=", "exc": "TooManyFoundError"},
    {"key": "limit_exact", "msg": "items exactly", "expr": "==", "exc": "NotFoundError"},
]

# REGEXES:
ESCAPED_COMMAS = r"(?<!\\),"
ESCAPED_COLONS = r"(?<!\\):"
IP_ADDRESS = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

PARAM_INDEX = r"^param__(\d+)"
PARAM_NAMED = r"^param_(\w+)"

DEFAULT_FIELD = "name"
DEFAULT_OPERATOR = "contains"
ROOT_BUCKET = "0"
DEFAULT_BUCKET = "1"
DEFAULT_HIDDEN = False
DEFAULT_PARAMS_DEFAULT = True
DEFAULT_PARAMS_VALIDATE = True
DEFAULT_PARAMS_EXTRAS = False
DEFAULT_PARAMS_SURROUND = "||"

FILTER_PROCESS_TOKENS = [
    {
        "token": "search_field",
        "methods": ["default", "required"],
        "default": DEFAULT_FIELD,
    },
    {
        "token": "search",
        "methods": ["required"],
    },
    {
        "token": "include_hidden_flag",
        "methods": ["default", "boolean", "integer"],
        "default": DEFAULT_HIDDEN,
    },
    {
        "token": "obj",
        "methods": ["search_obj"],
        "obj_type": "Sensor",
        "valid_fields": ["id", "name", "hash"],
    },
    {
        "token": "operator",
        "methods": ["default", "required", "operator"],
        "default": DEFAULT_OPERATOR,
    },
    {
        "token": "value",
        "methods": ["required"],
    },
    {
        "token": "value_type",
        "methods": ["value_type"],
    },
    {
        "token": "bucket",
        "methods": ["default", "required"],
        "default": DEFAULT_BUCKET,
    },
    {
        "token": "max_age_seconds",
        "methods": ["integer"],
    },
    {
        "token": "ignore_case_flag",
        "methods": ["boolean", "integer"],
    },
    {
        "token": "all_values_flag",
        "methods": ["boolean", "integer"],
    },
    {
        "token": "all_times_flag",
        "methods": ["boolean", "integer"],
    },
    {
        "token": "not_flag",
        "methods": ["boolean", "integer"],
    },
    {
        "token": "params_surround",
        "methods": ["default"],
        "default": DEFAULT_PARAMS_SURROUND,
    },
    {
        "token": "params_default",
        "methods": ["default", "boolean"],
        "default": DEFAULT_PARAMS_DEFAULT,
    },
    {
        "token": "params_validate",
        "methods": ["default", "boolean"],
        "default": DEFAULT_PARAMS_VALIDATE,
    },
    {
        "token": "params_extras",
        "methods": ["default", "boolean"],
        "default": DEFAULT_PARAMS_EXTRAS,
    },
    {
        "token": "param_",
        "methods": ["params"],
    },
]

FILTER_PARSE_ARGS = {"processors": FILTER_PROCESS_TOKENS, "unnamed": "search"}

GROUP_PROCESS_TOKENS = [
    {
        "token": "search_field",
        "methods": ["default", "required"],
        "default": DEFAULT_FIELD,
    },
    {
        "token": "search",
        "methods": ["required"],
    },
    {
        "token": "include_hidden_flag",
        "methods": ["default", "boolean", "integer"],
        "default": DEFAULT_HIDDEN,
    },
    {
        "token": "obj",
        "methods": ["search_obj"],
        "obj_type": "Group",
        "valid_fields": ["id", "name"],
    },
    {
        "token": "bucket",
        "methods": ["default", "required"],
        "default": DEFAULT_BUCKET,
    },
]

GROUP_PARSE_ARGS = {"processors": GROUP_PROCESS_TOKENS, "unnamed": "search"}

OPTION_PROCESS_TOKENS = [
    {
        "token": "bucket",
        "methods": ["default", "required"],
        "default": DEFAULT_BUCKET,
    },
    {
        "token": "not_flag",
        "methods": ["boolean", "integer"],
    },
    {
        "token": "and_flag",
        "methods": ["boolean", "integer"],
    },

]

OPTION_PARSE_ARGS = {"processors": OPTION_PROCESS_TOKENS, "unnamed": "bucket"}

BUCKET_PARSERS = [
    {"target": "filters", "args": FILTER_PARSE_ARGS},
    {"target": "groups", "args": GROUP_PARSE_ARGS},
    {"target": "options", "args": OPTION_PARSE_ARGS},
]

# -------------------- TANIUM OPERATOR TYPES
T_L = "Less"
T_LEQ = "LessEqual"
T_G = "Greater"
T_GEQ = "GreaterEqual"
T_E = "Equal"
T_R = "RegexMatch"
T_H = "HashMatch"
TANIUM_OPS = [T_L, T_LEQ, T_G, T_GEQ, T_E, T_R, T_H]

# -------------------- BASE OPERATOR TYPES
OP_LESS = {"o": T_L, "n": False, "h": "less than VALUE"}
OP_NOTLESS = {"o": T_L, "n": True, "h": "not less than VALUE"}
OP_LESSEQ = {"o": T_LEQ, "n": False, "h": "less than or equal to VALUE"}
OP_NOTLESSEQ = {"o": T_LEQ, "n": True, "h": "not less than or equal to VALUE"}
OP_GREATER = {"o": T_G, "n": False, "h": "greater than VALUE"}
OP_NOTGREATER = {"o": T_G, "n": True, "h": "not greater than VALUE"}
OP_GREATEQ = {"o": T_GEQ, "n": False, "h": "greater than or equal to VALUE"}
OP_NOTGREATEQ = {"o": T_GEQ, "n": True, "h": "not greater than or equal to VALUE"}
OP_EQ = {"o": T_E, "n": False, "h": "equal to VALUE"}
OP_NOTEQ = {"o": T_E, "n": True, "h": "not equal to VALUE"}
OP_HASH = {"o": T_H, "n": False, "h": "matches hash VALUE"}
OP_NOTHASH = {"o": T_H, "n": True, "h": "does not match hash VALUE"}
OP_RE = {"o": T_R, "n": False, "h": "matches regex VALUE"}
OP_NOTRE = {"o": T_R, "n": True, "h": "does not match regex VALUE"}
OP_CONTAINS = {"o": T_R, "n": False, "pre": ".*", "post": ".*", "h": "matches regex .*VALUE.*"}
OP_NOTCONTAINS = {"o": T_R, "n": True, "pre": ".*", "post": ".*", "h": "does not match regex .*VALUE.*"}
OP_STARTS = {"o": T_R, "n": False, "pre": ".*", "h": "matches regex .*VALUE"}
OP_NOTSTARTS = {"o": T_R, "n": True, "pre": ".*", "h": "does not match regex .*VALUE"}
OP_ENDS = {"o": T_R, "n": False, "post": ".*", "h": "matches regex VALUE.*"}
OP_NOTENDS = {"o": T_R, "n": True, "post": ".*", "h": "does not match regex VALUE.*"}

# HUMAN STRING MAPPING TO BASE OPERATOR TYPES
OPERATOR_MAPS = {
    "<": OP_LESS,
    "less": OP_LESS,

    "!<": OP_NOTLESS,
    "not less": OP_NOTLESS,

    "<=": OP_LESSEQ,
    "less equal": OP_LESSEQ,

    "!<=": OP_NOTLESSEQ,
    "not less equal": OP_NOTLESSEQ,

    ">": OP_GREATER,
    "greater": OP_GREATER,

    "!>": OP_NOTGREATER,
    "not greater": OP_NOTGREATER,

    "=>": OP_GREATEQ,
    "greater equal": OP_GREATEQ,

    "!=>": OP_NOTGREATEQ,
    "not greater equal": OP_NOTGREATEQ,

    "=": OP_EQ,
    "equals": OP_EQ,
    "eq": OP_EQ,

    "!=": OP_NOTEQ,
    "not equals": OP_NOTEQ,
    "neq": OP_NOTEQ,

    "~=": OP_CONTAINS,
    "like": OP_CONTAINS,
    "contains": OP_CONTAINS,
    "in": OP_CONTAINS,

    "!~=": OP_NOTCONTAINS,
    "not like": OP_NOTCONTAINS,
    "not contains": OP_NOTCONTAINS,
    "not in": OP_NOTCONTAINS,

    "starts with": OP_STARTS,
    "not starts with": OP_NOTSTARTS,
    "ends with": OP_ENDS,
    "not ends with": OP_NOTENDS,

    "is": OP_RE,
    "regex": OP_RE,
    "re": OP_RE,
    "regexmatch": OP_RE,
    "matching": OP_RE,
    "matches": OP_RE,
    "match": OP_RE,

    "is not": OP_NOTRE,
    "not regex": OP_NOTRE,
    "not regexmatch": OP_NOTRE,
    "nre": OP_NOTRE,

    "hash": OP_HASH,
    "not hash": OP_NOTHASH,
}

YES_LIST = ["yes", "y", "ye", "true", "1", 1, True]
"""List of possible "True" strings."""

NO_LIST = ["no", "n", "false", "0", 0, False]
"""List of possible "No" strings."""

# -------------------- BASE TYPES
TYPE_STR = {
    "t": "String",
    "h": "standard lexicographical comparison (the default)",
    "e": "abcdefgh",
}
TYPE_VER = {
    "t": "Version",
    "h": "version strings",
    "e": "9.4.2 is less than 10.1.3",
}
TYPE_NUM = {
    "t": "Numeric",
    "h": "numeric, decimal, floating point, and scientific notation",
    "e": "1000.0",
}
TYPE_IP = {
    "t": "IPAddress",
    "h": "IP addresses",
    "e": "192.168.1.1",
}
TYPE_DATE = {
    "t": "Date",
    "h": "a date in the format YYYY-MM-DD HH:MM:SS",
    "e": "2010-01-01 01:01:01",
}
TYPE_BDATE = {
    "t": "BESDate",
    "h": "a date in the format YYYY-MM-DD HH:MM:SS",
    "e": "2010-01-01 01:01:01",
}
TYPE_WDATE = {
    "t": "WMIDate",
    "h": "a date in the format yyyymmddHHMMSS.ssssss(+/-)UUU",
    "e": "20100101010101.894035+330",
}
TYPE_TDIFF = {
    "t": "TimeDiff",
    "h": "amount of time as a number followed by one of Y, MO, W, D, H, M, or S",
    "e": "2Y, 2 years, 3 months, 18 days, 4 hours, 22 minutes, 3.67 seconds",
}
TYPE_DS = {
    "t": "DataSize",
    "h": "data size as a number followed by one of B, K, M, G, or T",
    "e": "125MB, 23K, 34.2Gig",
}
TYPE_NUMI = {
    "t": "NumericInteger",
    "h": "be integer numeric values",
    "e": "1000",
}

VALUE_TYPES = {
    "string": TYPE_STR,
    "str": TYPE_STR,
    "version": TYPE_VER,
    "ver": TYPE_VER,
    "date": TYPE_BDATE,
    "ipaddress": TYPE_IP,
    "ip": TYPE_IP,
    "wmidate": TYPE_WDATE,
    "timediff": TYPE_TDIFF,
    "datasize": TYPE_DS,
    "numeric": TYPE_NUM,
    "float": TYPE_NUM,
    "decimal": TYPE_NUM,
    "numericinteger": TYPE_NUMI,
    "integer": TYPE_NUMI,
    "int": TYPE_NUMI,
}

INIT_HASHES = {
    7318847: "Last Logged In User",
    8168018: "Video Driver Version",
    15451865: "USB Device",
    21983240: "AD Organizational Unit",
    45421433: "Operating System",
    63201224: "File Size",
    74624344: "Windows OS Type",
    75018363: "User Sessions",
    77425467: "SQL Log Sizes",
    93198492: "Open Share Details",
    95001259: "Tanium File Exists",
    98057726: "Boot Time",
    99939055: "Wireless Network SSID Strength",
    102224229: "Computer Serial Number",
    112406691: "File Version",
    131549066: "Online",
    151176619: "Onboard Devices",
    170942492: "System Drive",
    182214159: "Local User Login Dates",
    189860887: "Audio Controller",
    191451006: "Tanium Buffer Count",
    254407409: "Installed HotFixes",
    276664624: "Maximum Process Memory Size",
    283520893: "Tanium Client Dump Files",
    314220795: "USB Device Details",
    316030016: "Total Memory",
    319662655: "Running Processes Memory Usage",
    322086833: "Download Statuses",
    324032765: "UDP Connections",
    333178608: "Tanium Zone Server Version",
    341438855: "Recently Run Applications",
    367063513: "BIOS Name",
    391368340: "SQL Server Agent Long Running Jobs",
    422662332: "Static IP Addresses",
    432766313: "SQL Buffer Hit Ratio",
    435227963: "IP Route Details",
    435957060: "Tanium Client Version",
    462732724: "AD Domain",
    482346946: "SQL Product Level",
    487354270: "IP Routes",
    502812713: "Application Event Log IDs",
    508127351: "Disk Used Space",
    525163843: "AD Computer Groups",
    533135859: "Disk Used Percentage",
    542266296: "Share Folder Permissions",
    549503533: "Operating System Language",
    568581921: "Reboot Required",
    590837956: "Number of Fixed Drives",
    600562575: "CPU by Process",
    601571508: "Open Port",
    607666494: "Application Crashes Yesterday",
    617084407: "Logical Volumes",
    632662206: "Folder Size",
    664237249: "Application Run Time",
    676468157: "Installed RPMs",
    711837192: "Tanium Server Version",
    740857544: "Target",
    745447734: "Cached AD Logins",
    747106243: "System Slots In Use",
    749653644: "SQL Server Edition",
    782305667: "RAM Max Capacity",
    794103688: "Domain Name",
    801419063: "Defrag Needed",
    801908140: "User Details",
    824239263: "Tanium Client Core Health",
    833799742: "BIOS Version",
    856087598: "PST Information",
    861367460: "Shared Network Printer Details",
    865123401: "Kernel Modules",
    867160258: "Hyperthreading Enabled",
    876725971: "Network Printer Details",
    885259283: "Motherboard Manufacturer",
    889071797: "Firewall Status",
    902205018: "Country Code",
    916410332: "Data Execution Prevention Enabled",
    923740265: "CD-ROM Drive",
    926119908: "Service",
    945314213: "Disk Drives",
    953427826: "Video/Graphics Card",
    969736519: "Tanium Action Log",
    991644931: "Workgroup",
    1022769818: "Is Virtual",
    1039470236: "SQL Clustered",
    1043670154: "Disk Free Space Below Threshold",
    1046354727: "Virtual Platform",
    1092986182: "Logged In Users",
    1101836903: "Folder Exists",
    1125023461: "Boot Device",
    1132013379: "Open Shares",
    1140552555: "Internet Explorer Version",
    1154425412: "DHCP Enabled?",
    1155294592: "Domain Controller SYSVOL Size",
    1156943497: "Disk IOPS",
    1206550580: "Network Link Speed",
    1208633896: "MAC Address",
    1240245618: "SQL Database Recovery Mode",
    1260624634: "Free Memory",
    1260646358: "CPU Consumption",
    1263879283: "High Uptime",
    1265351278: "Application Crashes in Last X Days",
    1271450145: "Service Login Names",
    1281370578: "BitLocker Details",
    1302957088: "Disk Free Space",
    1314534715: "Security Event Log IDs",
    1315630323: "Used Memory",
    1326015223: "FileVault Details",
    1348043492: "Printers",
    1348161929: "Default Login Domain",
    1404374135: "Startup Programs",
    1417112132: "No Screen Saver Password",
    1426187539: "Physical Volumes",
    1466668831: "Wireless Network Connected SSID",
    1471370561: "DHCP Server",
    1496471156: "NET Version",
    1497251383: "Running Service",
    1502679547: "Monitor Details",
    1509255291: "Non-Approved Established Connections",
    1511329504: "Installed Applications",
    1512811088: "Registry Key Value Exists",
    1526750078: "Screen Saver Active",
    1527458369: "High Memory Processes",
    1528412180: "Established Connections",
    1544486184: "Operating System Boot Directory",
    1559751995: "Running Applications",
    1569955801: "Unencrypted Wireless Networks",
    1579270802: "Sound Card",
    1580351176: "BIOS Vendor",
    1591480148: "System Event Log IDs",
    1591958393: "Registry Value Data",
    1646244079: "CPU Speed Mhz",
    1652607578: "Disk Drive Details",
    1670489640: "High CPU Consumption",
    1688928675: "Has Application Management Tools",
    1718946935: "High Memory Consumption",
    1723627713: "Local User Password Change Dates",
    1724798097: "Last System Crash",
    1735107559: "Network Throughput Outbound",
    1742036917: "x64/x86?",
    1744818157: "Tanium Client Subnet",
    1782389954: "Has Tanium Standard Utilities",
    1785623864: "Ram Slots Unused",
    1792443391: "Action Statuses",
    1805210070: "Tanium PowerShell Execution Policy",
    1806420230: "Network Printers",
    1810333216: "Established Ports by Application",
    1815821395: "Last System Crash in X Days",
    1819649983: "Network Throughput Percentage",
    1832324705: "Run Once Keys",
    1845399463: "SQL Server CPU Consumption",
    1865193433: "Tanium Server Name List",
    1913997657: "Username",
    1927765752: "Active Devices",
    1927941770: "Last Application Launch Date",
    1978207968: "System Environment Variables",
    1982695066: "Operating System Install Date",
    1988427982: "User Accounts",
    1994896093: "Driver Details",
    2006202074: "Time Zone",
    2060254274: "Local Administrators Without Groups",
    2074877994: "Recently Closed Connections",
    2095666087: "Default Login UserID",
    2106396979: "Logged in User Details",
    2114351169: "Network Drives Accessed",
    2130080578: "CPU Manufacturer",
    2154864096: "Outlook Version",
    2177412849: "Last Logins",
    2177703669: "Memory Consumption",
    2183585490: "Path Permissions",
    2195303088: "SQL Product Version",
    2207214962: "Disk Type of C:",
    2222730558: "Operating System Temp Directory",
    2233537498: "Wireless Networks Visible",
    2254780098: "Stopped Service Short Name",
    2265461905: "Monitor Resolution",
    2290387752: "Tanium Client Action Folder Sizes",
    2322714946: "AD Short Domain",
    2344747808: "SQL Server Databases",
    2353715452: "Volume Group Names",
    2357545787: "Predicted Disk Failures",
    2361722934: "Load Average",
    2370758491: "Client Time",
    2384520458: "Service Details",
    2387001299: "Installed Application Version",
    2417208908: "Password Policy Details",
    2463256440: "CPU Architecture",
    2490353155: "Registry Key Exists",
    2505938414: "Default Printer",
    2513829483: "AD Distinguished Name",
    2542613392: "Manufacturer",
    2574398281: "Application Event Log Search",
    2581054686: "Has Hardware Tools",
    2595849133: "Motherboard Name",
    2607823237: "Video Graphics Card RAM",
    2614767778: "UAC Status",
    2620257697: "Domain Member",
    2623590847: "Network Throughput Total",
    2634431519: "Last Date of Local Administrator Login",
    2648511780: "Packet Loss",
    2671758800: "Action Lock Status",
    2680423840: "Local Account Last Password Change Days Ago",
    2704923764: "PowerShell Version",
    2706539957: "Local Printers",
    2711879278: "High CPU Processes",
    2721439124: "Is Windows",
    2728641061: "Chassis Type",
    2735360016: "Tanium Client Neighborhood",
    2753029185: "Primary Owner Name",
    2758038984: "Tanium Client Action Timing",
    2759217311: "BIOS Current Language",
    2783988057: "Network Adapter Name",
    2800817874: "Is Mac",
    2811135310: "Last Reboot",
    2811171321: "Time Zone Offset",
    2812601404: "File Creation Date",
    2819106613: "IP Connections",
    2823285829: "VMware Guest",
    2845896284: "Network Throughput Inbound",
    2853143977: "CPU",
    2866852225: "TCP connections",
    2881145629: "Service Pack",
    2932384540: "Default Web Browser",
    2939169480: "Low Disk Space",
    2950466201: "Number Of Users",
    2961425050: "Model",
    2977419696: "Subnet Mask",
    2997757654: "Operating System Language Code",
    3004497651: "Custom Tags",
    3005061811: "Has Stale Tanium Client Data",
    3009680784: "Network Adapter Details",
    3027378756: "Number of Application Crashes in Last X Days",
    3057103978: "Windows Server Installed Roles",
    3083322981: "Number of Processor Cores",
    3103658637: "Tanium Sensor Randomization Enabled",
    3112892791: "DNS Server",
    3114455387: "Internet Explorer Add-Ons",
    3133617106: "Motherboard Version",
    3133620839: "Revision of CPU",
    3134254821: "Java Auto Update",
    3145690673: "Hardware Device Failed to Load",
    3147407985: "SQL Recovery Mode",
    3147580256: "Total Swap",
    3157180652: "Tanium Client Downloads Directory Details",
    3170446499: "PCI Device",
    3170496172: "Number of Logged In Users",
    3177804004: "Locale Code",
    3188527889: "Stopped Service",
    3200371050: "Listen Ports",
    3209138996: "IP Address",
    3226581166: "OS Boot Time",
    3271577967: "SQL Database Count",
    3276808962: "Network Adapter Type",
    3285711879: "Registry Key Subkeys",
    3320877330: "Number of Processors",
    3369713834: "Organization",
    3394404860: "Wireless Networks Using WEP",
    3397569679: "Hosted Wireless Ad-Hoc Networks",
    3409330187: "Computer Name",
    3418227220: "Tanium Client Installation Date",
    3418263806: "Local Account Expiration Details",
    3479253433: "Tanium Client Installation Time",
    3480890585: "Uptime",
    3482410175: "System Directory",
    3499030954: "Page File Details",
    3518770446: "Hosts File Entries",
    3554080383: "Is Linux",
    3556221173: "Computer ID",
    3575849436: "Network IP Gateway",
    3595988712: "USB Write Protected",
    3603927824: "Installed Pkgs",
    3605572245: "Human Interface Device",
    3622133010: "Local Administrators",
    3646624356: "CPU Cache Size",
    3652459872: "Tanium Reboot Days Ago",
    3662289857: "File Exists",
    3682298314: "Processes Using Module",
    3685017662: "Is Terminal Server",
    3727949854: "Client Date",
    3734316770: "Tanium Client CPU",
    3756702099: "Is AIX",
    3760050184: "Tanium Client Explicit Setting",
    3763483691: "CPU Family",
    3764526140: "SCSI Controller Driver Name",
    3770282786: "Operating System Build Number",
    3792181176: "Is Solaris",
    3796118374: "SQL Database Sizes",
    3798171813: "BIOS Release Date",
    3799348944: "Registry Key Value Names with Data",
    3868118771: "Used Swap",
    3881863289: "Folder Contents",
    3891170751: "System UUID",
    3898138660: "Tanium Client NAT IP Address",
    3910101228: "Power Plans Active",
    3914171274: "CD-ROM Drive Loaded",
    3963156324: "Attached Battery",
    3993657420: "Installed Java Runtimes",
    3999173666: "User Profile Directory Details",
    4018912755: "Primary WINS Server",
    4055028299: "CPU Details",
    4058321794: "Run Keys",
    4070262781: "Tanium File Contents",
    4076878703: "Tanium Server Name",
    4080631087: "File Modification Date",
    4086041268: "RAM Slots Used and Unused",
    4086596771: "Tanium Client Logging Level",
    4105783647: "SCSI Controller Caption",
    4142232197: "Running Processes",
    4165545489: "AD Forest",
    4180356655: "System Disk Free Space",
    4201347922: "Free Swap",
    4206488295: "Wireless Network Used by Tanium",
    4212162125: "Disk Total Size of System Drive",
    4225957259: "Tanium Current Directory",
    4244179900: "Run Level",
    4244410676: "Disk Total Space",
    4254566410: "System Slots Available",
    4261354259: "Tanium Peer Address",
    4264207873: "AD User Groups",
    4264271977: "Tanium Client IP Address",
    4267153065: "Wireless Network Details",
    4276555360: "Registry Key Value Names",
    4279567267: "RAM",
    4284507739: "USB Storage Devices",
    4287813257: "Power Plans Available",
    4293389196: "Tanium Back Peer Address",
}

XMLNS = {
    "soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "t": "urn:TaniumSOAP",
    "encodingStyle": "http://schemas.xmlsoap.org/soap/encoding/",
}
"""The XML namespace mappings for all SOAP XML bodies"""

SOAP_REQUEST_BODY = (
    """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="{soap}" xmlns:xsd="{xsd}" soap:encodingStyle="{encodingStyle}">
  <soap:Body xmlns:t="{t}" xmlns:xsi="{xsi}">
    <t:tanium_soap_request>
      <command>$command</command>
      <object_list>$object_list</object_list>
      $options
    </t:tanium_soap_request>
  </soap:Body>
</soap:Envelope>
""")
"""
The XML template used for all SOAP Requests in string form
{} variables will be replaced with keys from XMLNS
$ variables will be replaced with strings from the objects during request time
"""

SOAP_CONTENT_TYPE = "text/xml; charset=utf-8"
