from random import randint

examples = {}
examples['ask_manual_question'] = [
    {
        'name': 'Print the help for sensors',
        'cmd': 'ask_manual_question.py $API_INFO --sensors-help csv',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for filters',
        'cmd': 'ask_manual_question.py $API_INFO --filters-help csv',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'ask_manual_question.py $API_INFO --options-help csv',
        'tests': 'notexitcode',
    },
    {
        'name': 'Ask a question example 1',
        'cmd': (
            'ask_manual_question.py $API_INFO --sensor "Computer Name" --file "$TMP/out.csv" csv'
        ),
        'notes': ['Ask a question with a single sensor', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 2',
        'cmd': 'ask_manual_question.py $API_INFO --sensor "id:1" --file "$TMP/out.csv" csv',
        'notes': ['Ask a question with a single sensor by id', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 3',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '--sensor "Computer Name" --sensor "Installed Applications" '
            ' --file "$TMP/out.csv" csv'
        ),
        'notes': ['Ask a question with two sensors', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 4',
        'cmd': (
            'ask_manual_question.py $API_INFO --sensor "Folder Name Search with RegEx Match'
            '{dirname=Program Files,regex=Microsoft.*}"'
            ' --file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with a sensor that requires parameters',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 5',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '--sensor "Operating System, that contains:Windows, opt:ignore_case, '
            'opt:max_data_age:60" --file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with a single sensor',
            'Supply a filter in the sensor that limits the column data to .*Windows.* matches',
            'Supply an option in the sensor that ignores case in the filter',
            'Supply an option in the sensor that re-fetches cached data older than 1 minute',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 6',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '-s "Computer Name" '
            '-s "Folder Name Search with RegEx Match{dirname=Program Files,regex=Microsoft.*, '
            'invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600" '
            '-f "Operating System, that contains:Windows" '
            '-f "IP Address, that not equals:10.10.10.10" '
            '-o "or" -o "ignore_case" '
            '--file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with two sensors',
            'Supply parameters to the 2nd sensor',
            'Supply a filter in the 2nd sensor that limits the column data to .*Shared.*',
            'Supply an option in the 2nd sensor that re-fetches cached data older than 1 minute',
            'Supply a question filter that limits the rows returned to machines whose '
            'Operating System sensor match .*Windows.*',
            'Supply a question filter that limits the rows returned to machines whose '
            'IP Address filter does not equal 10.10.10.10',
            'Supply two question options, one to OR the question filters supplied, and another '
            'to ignore the case while matching the question filters',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a question example 7',
        'cmd': (
            'ask_manual_question.py $API_INFO '
            '-s "Computer Name" -s "Last Logged In User" '
            '-s "Installed Applications, that contains:Google Search" '
            '-s "Installed Applications, that contains:Google Chrome" '
            '-f "Installed Applications, that contains:Google Search" '
            '-f "Installed Applications, that contains:Google Chrome" '
            '-o "and" -o "ignore_case" '
            '--file "$TMP/out.csv" csv'
        ),
        'notes': [
            'Ask a question with 4 sensors',
            'Use filters on 3rd and 4th sensor to limit the column data to only show certain apps',
            'Use 2 question filters to limit the row data to only show the same apps used in'
            ' the sensor filters',
            'Supply two question options, one to AND the question filters supplied, and another '
            'to ignore the case while matching the question filters',
            'Save the results to a CSV file',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
]

examples['ask_saved_question'] = [
    {
        'name': 'Ask a saved question',
        'cmd': (
            'ask_saved_question.py $API_INFO '
            '--name "Installed Applications" --file "$TMP/out.csv" csv'
        ),
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Ask a saved question and refresh the data available before fetching the data',
        'cmd': (
            'ask_saved_question.py $API_INFO '
            '--name "Installed Applications" --file "$TMP/out.csv" --refresh_data csv'
        ),
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
]

examples['create_whitelisted_url'] = [
    {
        'name': 'Create a whitelisted URL',
        'cmd': (
            'create_whitelisted_url.py $API_INFO '
            '--url "https://testing.com/$RAND_INT" '
            '--regex '
            '--download 3600 '
            '--property "property name" "property value"'
        ),
        'notes': [
            'Create a whitelisted_url for https://testing.com',
            'Set the new URL as a regex pattern',
            'Set thew new URL to be re-downloaded every 3600 seconds'
            'Create a property named property name with the value property value on the new URL',
        ],
        'tests': 'exitcode',
    },
]


examples['create_package'] = [
    {
        'name': 'Print the help for filters',
        'cmd': 'create_package.py $API_INFO --filters-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'create_package.py $API_INFO --options-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Create a new package',
        'cmd': (
            'create_package.py $API_INFO '
            '--name "1234 CMDLINE TEST package" '
            '--display-name "1234 CMDLINE TEST package display name" '
            '--command "testing.vbs \\$1 \\$2 \\$3 \\$4 \\$5 \\$6 \\$7 \\$8" '
            '--expire-seconds 1500 '
            '--file-url "3600::testing.vbs||https://testing.com/testing.vbs" '
            '--file-url "https://testing.com/another_testing.vbs" '
            '--parameters-file "$PYTAN_DIR/doc/example_of_all_package_parameters.json" '
            '--verify-expire-seconds 3600 '
            '--verify-filter "Custom Tags, that contains:tag" '
            '--verify-option "ignore_case" '
            '--command-timeout 600 '
        ),
        'notes': [
            'Create a package named 1234 CMDLINE TEST package',
            'Set the display name in the console for the new '
            'package to 1234 CMDLINE TEST package display name',
            'When this package is deployed, run the command testing.vbs and expect 8 arguments',
            'When this package is deployed as part of an action, default the action to expire '
            'after 3600 seconds',
            'Add a file to this package that will be redownloaded every 3600 seconds, named '
            'testing.vbs in Tanium, and downloaded from testing.com/testing.vbs',
            'Add another file to this package that will be downloaded once, '
            'extract the file name from the URL, and downloaded from '
            'testing.com/another_testing.vbs',
            'Add all the parameters defined in doc/example_of_all_package_parameters.json',
            'Expire the verification filter after 3600 seconds',
            'Expire the command if it takes longer than 600 seconds to run',
            'Supply a verification filter that will be used when this package is deployed as part '
            'of an action',
            'Supply an option for the verification filter that ignores case',
        ],
        'tests': 'exitcode',
    },
    {
        'name': 'Delete the recently created package',
        'cmd': (
            'delete_package.py $API_INFO --name "1234 CMDLINE TEST package" '
        ),
        'notes': [
            'Delete the package named 1234 CMDLINE TEST package',
        ],
        'tests': 'exitcode',
    },
]

examples['create_group'] = [
    {
        'name': 'Print the help for filters',
        'cmd': 'create_group.py $API_INFO --filters-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'create_group.py $API_INFO --options-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Create a new group',
        'cmd': (
            'create_group.py $API_INFO --name "All Windows Computers CMDLINE TEST GROUP" '
            '-f "Operating System, that contains:Windows" '
            '-f "IP Address, that not equals:10.10.10.10" '
            '-o "and" -o "ignore_case"'
        ),
        'notes': [
            'Create a group named All Windows Computers CMDLINE TEST GROUP',
            'Supply a filter that limits the group members to machines that match '
            '.*Windows.* for the Operating System sensor',
            'Supply a filter that limits the group members to machines that do not equal '
            '10.10.10.10 for the IP Address sensor',
            'Supply two options, one to AND the filters supplied, and another '
            'to ignore the case while matching the filters',
        ],
        'tests': 'exitcode',
    },
    {
        'name': 'Delete the recently created group',
        'cmd': (
            'delete_group.py $API_INFO --name "All Windows Computers CMDLINE TEST GROUP" '
        ),
        'notes': [
            'Delete the group named All Windows Computers CMDLINE TEST GROUP',
        ],
        'tests': 'exitcode',
    },
]

examples['deploy_action'] = [
    {
        'name': 'Print the help for package',
        'cmd': 'deploy_action.py $API_INFO --package-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for filters',
        'cmd': 'deploy_action.py $API_INFO --filters-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Print the help for options',
        'cmd': 'deploy_action.py $API_INFO --options-help',
        'tests': 'notexitcode',
    },
    {
        'name': 'Deploy an action example 1',
        'cmd': (
            'deploy_action.py $API_INFO --package "Distribute Tanium Standard Utilities" '
            '--file "$TMP/out.csv"'
        ),
        'notes': [
            'Deploys an action using the package Distribute Tanium Standard Utilities',
            'Since --run was not supplied, the results of the question for the filters '
            'of this action will be written to a CSV file for verification, and the deploy '
            'action will NOT be run'
        ],
        'precleanup': 'rm -f $TMP/VERIFY_BEFORE_DEPLOY_ACTION_out.csv',
        'file_exist': '$TMP/VERIFY_BEFORE_DEPLOY_ACTION_out.csv',
        'tests': 'notexitcode, file_exist_contents',
    },
    {
        'name': 'Deploy an action example 2',
        'cmd': (
            'deploy_action.py $API_INFO --package "Distribute Tanium Standard Utilities" '
            '--run --file "$TMP/out.csv"'
        ),
        'notes': ['Deploys an action using the package Distribute Tanium Standard Utilities'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Deploy an action example 3',
        'cmd': (
            'deploy_action.py $API_INFO '
            '--package "Custom Tagging - Add Tags{\\$1=new_tag}" '
            '--filter "Operating System, that contains:Windows" '
            '--run --file "$TMP/out.csv"'
        ),
        'notes': [
            'Deploys an action using the package "Custom Tagging - Add Tags", passing in a '
            'parameter for the tag to be added',
            'Uses a filter to only deploy the action agains machines that match .*Windows.* '
            'for the Operating System sensor',
        ],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
]

examples['get_results'] = [
    {
        'name': 'Ask a question',
        'cmd': (
            'ask_manual_question.py $API_INFO --no-results --sensor "Computer Name" csv | tee $TMP/ask.out'
        ),
        'notes': ['Ask a question without getting the results, save stdout to ask.out'],
        'precleanup': 'rm -f $TMP/ask.out',
        'file_exist': '$TMP/ask.out',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Wait 30 seconds',
        'cmd': (
            'sleep 15'
        ),
        'notes': ['Wait 30 seconds for data for the previously asked question to be available'],
        'tests': 'exitcode',
    },
    {
        'name': 'Get the results for a question',
        'cmd': (
            'get_results.py $API_INFO -o "question" --id `cat $TMP/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "$TMP/out.csv" csv'
        ),
        'notes': ['Get the results for the question ID asked previously ', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Get the results for a question via a server side export',
        'cmd': (
            'get_results.py $API_INFO -o "question" --id `cat $TMP/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "$TMP/out.csv" --sse csv'
        ),
        'notes': ['Get the results for the question ID asked previously using a server side export', 'Save the results to a CSV file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist_contents',
    },
]

examples['create_user'] = [
    {
        'name': 'Create a new user',
        'cmd': (
            'create_user.py $API_INFO --name "CMDLINE TEST user" '
            '--rolename "Administrator" '
            '--property "property name" "property value" | tee -a $TMP/create_user.out'
        ),
        'notes': [
            'Create a user named CMDLINE TEST user',
            'Assign the Administrator role to the new user',
            'Create a property named property name with the value property value on the new user',
        ],
        'precleanup': 'rm -f $TMP/create_user.out',
        'tests': 'exitcode',
    },
    {
        'name': 'Delete the recently created user',
        'cmd': (
            """delete_user.py $API_INFO """
            """--id `cat $TMP/create_user.out| grep created | sed 's/.*ID //' | cut -d, -f1` """
        ),
        'notes': [
            'Delete the user named CMDLINE TEST user',
        ],
        'tests': 'exitcode',
    },
]


examples['print_sensors'] = [
    {
        'name': 'Print all sensors',
        'cmd': 'print_sensor.py $API_INFO --all',
        'tests': 'exitcode',
    },
    {
        'name': 'Print all Linux sensors',
        'cmd': 'print_sensor.py $API_INFO --all --platform Linux',
        'tests': 'exitcode',
    },
    {
        'name': 'Print all Linux sensors that fall under the category "Operating System"',
        'cmd': 'print_sensor.py $API_INFO --all --platform Linux --category "Operating System"',
        'tests': 'exitcode',
    },
    {
        'name': 'Print all Mac and Windows sensors that fall under the category "User"',
        'cmd': 'print_sensor.py $API_INFO --all --platform Mac --platform Windows --category "User"',
        'tests': 'exitcode',
    },
]

examples['print_server_info'] = [
    {
        'name': 'Print the server info in JSON format',
        'cmd': 'print_server_info.py $API_INFO --json',
        'tests': 'exitcode',
    },
]

examples['stop_action'] = [
    {
        'name': 'Stop a deploy action',
        'cmd': 'stop_action.py $API_INFO --id 123456',
        'notes': ['This example does not actually run'],
        'norun': 'true',
        'tests': '',
    }
]

object_examples = {}
object_examples['create_object_from_json'] = [
    {
        'name': 'Export OBJECTNAME id 1 as JSON',
        'cmd': 'get_OBJECTNAME.py $API_INFO --id 1 --file "$TMP/out.json" json',
        'notes': ['Get the first OBJECTNAME object', 'Save the results to a JSON file'],
        'precleanup': 'rm -f $TMP/out.json',
        'file_exist': '$TMP/out.json',
        'tests': 'exitcode, file_exist_contents',
    },
    {
        'name': 'Change name or url_regex in the JSON',
        'cmd': (
            """perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST {}"/gm'"""
            """ $TMP/out.json && cat $TMP/out.json""".format(randint(1, 9999))
        ),
        'notes': ['Add CMDLINE TEST to name or url_regex in the JSON file'],
        'file_exist': '$TMP/out.json',
        'tests': 'exitcode, file_exist',
    },
    {
        'name': 'Create a new OBJECTNAME from the modified JSON file',
        'cmd': 'create_OBJECTNAME_from_json.py $API_INFO -j "$TMP/out.json"',
        'precleanup': 'rm -f $TMP/create.out',
        'tests': 'exitcode',
    },
]

object_examples['delete_object'] = [
    {
        'name': 'Delete OBJECTNAME',
        'cmd': 'delete_OBJECTNAME.py $API_INFO --id 123456',
        'notes': ['This example does not actually run'],
        'norun': 'true',
        'tests': '',
    }
]

object_examples['get_object'] = [
    {
        'name': 'Export all OBJECTNAME as JSON',
        'cmd': 'get_OBJECTNAME.py $API_INFO --all --file "$TMP/out.json" json',
        'notes': ['Get all OBJECTNAME objects', 'Save the results to a JSON file'],
        'precleanup': 'rm -f $TMP/out.json',
        'file_exist': '$TMP/out.json',
        'tests': 'exitcode, file_exist',
    },
    {
        'name': 'Export all OBJECTNAME as CSV',
        'cmd': 'get_OBJECTNAME.py $API_INFO --all --file "$TMP/out.csv" csv',
        'notes': ['Get all OBJECTNAME objects', 'Save the results to a csv file'],
        'precleanup': 'rm -f $TMP/out.csv',
        'file_exist': '$TMP/out.csv',
        'tests': 'exitcode, file_exist',
    },
    {
        'name': 'Export all OBJECTNAME as xml',
        'cmd': 'get_OBJECTNAME.py $API_INFO --all --file "$TMP/out.xml" xml',
        'notes': ['Get all OBJECTNAME objects', 'Save the results to a xml file'],
        'precleanup': 'rm -f $TMP/out.xml',
        'file_exist': '$TMP/out.xml',
        'tests': 'exitcode, file_exist',
    },
]
