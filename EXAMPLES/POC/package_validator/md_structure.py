"""METADATA parsing structure."""
md_structure = [
    {
        "KEY": "name",
        "TYPE": "str",
        "HELP": "Correlates to name in package UI. Name of package to find & update or create.",
        "REQUIRED": True
    },
    {
        "KEY": "display_name",
        "TYPE": "str",
        "HELP": "Correlates to display name in package UI.",
        "REQUIRED": False
    },
    {
        "KEY": "command",
        "TYPE": "str",
        "HELP": "Correlates to command in package UI.",
        "REQUIRED": False
    },
    {
        "KEY": "command_timeout",
        "TYPE": "int",
        "HELP": "Correlates to command timeout in package UI.",
        "REQUIRED": False
    },
    {
        "KEY": "expire_seconds",
        "TYPE": "int",
        "HELP": "Correlates to download timeout in package UI.",
        "REQUIRED": False
    },
    {
        "KEY": "hidden_flag",
        "TYPE": "bool",
        "HELP": "Hide package from package list in UI or not.",
        "REQUIRED": False
    },
    {
        "KEY": "files",
        "TYPE": "list",
        "HELP": "list of str of paths to files that should be attached to package object. non-absolute paths must exist in same directory as METADATA file.",
        "REQUIRED": False,
        "ITEM_TYPE": "str"
    },
    {
        "KEY": "parameters",
        "TYPE": "list",
        "HELP": "list of dict of parameters to files that should be assigned to package object.",
        "REQUIRED": False,
        "ITEM_TYPE": "dict",
        "ITEM_STRUCTURE": [
            {
                "KEY": "mode",
                "TYPE": "str",
                "HELP": "Mode to use for this parameter.",
                "VALUES": ["text", "checkbox", "number", "dropdown"],
                "DEFAULT": "text",
                "REQUIRED": False
            },
            {
                "KEY": "max_chars",
                "TYPE": "int",
                "HELP": "Max number of characters to allow for a parameter of mode: text.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["text"],
                },
            },
            {
                "KEY": "maximum",
                "TYPE": "int",
                "HELP": "Max integer to allow for a parameter of mode: number.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["number"],
                },
            },
            {
                "KEY": "minimum",
                "TYPE": "int",
                "HELP": "Min integer to allow for a parameter of mode: number.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["number"],
                },
            },
            {
                "KEY": "help",
                "TYPE": "str",
                "HELP": "Help string to display in UI for this parameter.",
                "REQUIRED": False
            },
            {
                "KEY": "label",
                "TYPE": "str",
                "HELP": "Label to display in UI for this parameter.",
                "REQUIRED": False
            },
            {
                "KEY": "default_text",
                "TYPE": "str",
                "HELP": "Default value to use for a parameter of mode: text.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["text"],
                },
            },
            {
                "KEY": "default_number",
                "TYPE": "int",
                "HELP": "Default value to use for a parameter of mode: number or checkbox.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["number", "checkbox"],
                },
            },
            {
                "KEY": "prompt",
                "TYPE": "str",
                "HELP": "Value to show greyed-out in value entry box for a parameter of mode: text.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["text"],
                },
            },
            {
                "KEY": "validations",
                "TYPE": "list",
                "HELP": "list of dict of validations to use for a parameter of mode: text.",
                "REQUIRED": False,
                "DEPS": {
                    "mode": ["text"],
                },
                "ITEM_TYPE": "dict",
                "ITEM_STRUCTURE": [
                    {
                        "KEY": "help",
                        "TYPE": "str",
                        "HELP": "Help string to display in UI when user supplied value fails to pass expression.",
                        "REQUIRED": False
                    },
                    {
                        "KEY": "expression",
                        "TYPE": "str",
                        "HELP": "Regular expression to validate user supplied value.",
                        "REQUIRED": True
                    },
                ]
            },
        ]
    }
]
