#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''All the examples for the bin scripts'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '2.1.5'

example_skips = [
    'CONFIG',
]

import os

pytan_user_config_default = os.path.expanduser("~/.pytan_config.json")
examples = {}

# write_pytan_user_config
sname = 'write_pytan_user_config'
examples[sname] = []

e = {}
e['name'] = 'Create a PyTan User Config file at the default location'
e['cmd'] = '''bin/${script_name}.py ${API_INFO}'''
e['notes'] = '''This will take the command line arguments and authenticate with them.
Upon successful authentication, a PyTan User Config file will be written in JSON format to ~/.pytan_config.json
'''
e['precleanup'] = "rm -f {}".format(pytan_user_config_default)
e['file_exist'] = pytan_user_config_default
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Test that the PyTan User Config file that was created above at the default location works for another script without having to supply any credentials on the command line'
e['cmd'] = '''print_sensors.py --name "Installed Applications"'''
e['notes'] = '''The print_sensors script should now successfully authenticate based on the parameters defined in the default location for the PyTan User Config file, and we no longer need to supply the parameters on the command line
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Create a PyTan User Config file at a custom location'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --file ${TMPDIR}/custom.json'''
e['notes'] = '''This will take the command line arguments and authenticate with them.
Upon successful authentication, a PyTan User Config file will be written in JSON format to ${TMPDIR}/custom.sjon
'''
e['precleanup'] = "rm -f ${TMPDIR}/custom.json"
e['file_exist'] = '${TMPDIR}/custom.json'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Test that the PyTan User Config file that was created above at the custom location works for another script without having to supply any credentials on the command line'
e['cmd'] = '''print_sensors.py --name "Installed Applications" --pytan_user_config ${TMPDIR}/custom.json'''
e['notes'] = '''The print_sensors script should now successfully authenticate based on the parameters defined in the custom location for the PyTan User Config
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Manually create a PyTan User Config file in JSON format with only two parameters'
e['cmd'] = '''print_sensors.py --name "Installed Applications" --pytan_user_config ${TMPDIR}/manualcustom.json --host ${TANIUM_HOST}'''
e['notes'] = '''First we create ${TMPDIR}/manualcustom.json with just username and password
Next we run print_sensors script and supply host on the command line.
Note: Command line supplied arguments will always over ride arguments supplied in the PyTan User Config file
'''
e['contentfilename1'] = '${TMPDIR}/manualcustom.json'
e['contenttype1'] = 'json'
e['contenttext1'] = '''{
      "username": "${TANIUM_USERNAME}",
      "password": "${TANIUM_PASSWORD}"
    }
'''
e['precleanup'] = "rm -f ${TMPDIR}/manualcustom.json"
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)


# get_saved_question_history
sname = 'get_saved_question_history'
examples[sname] = []

e = {}
e['name'] = 'Get the details about all questions that have data that have been asked because of the Saved Question named "Installed Applications"'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "Installed Applications" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Will produce a CSV file with the details for each question that has data asked because of the Saved Question named "Installed Applications"
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Get the details about all questions, whether they have data or not, that have been asked because of the Saved Question named "Installed Applications"'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "Installed Applications" --empty_results --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Will produce a CSV file with the details for each question asked because of the Saved Question named "Installed Applications"
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Get the details about all questions that have data'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all_questions --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Will produce a CSV file with the details for each question with data
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Get the details about all questions, whether they have data or not'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all_questions --empty_results --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Will produce a CSV file with the details for each question
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

# ask_parsed
sname = 'ask_parsed'
examples[sname] = []

e = {}
e['name'] = 'Ask a parsed question example 1'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -q "get computer name"'''
e['notes'] = '''Ask a simple question in english with just one sensor
Since --picker is not provided, this will exit with an error and print all of the results that the english form was parsed into, prepended with an index. This should be re-run with --picker INDEX_NUMBER, as seen in the rest of these examples.
'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a parsed question example 2'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -q "get computer name" --picker 1 --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a simple question in english with just one sensor
Pick the first match that the english form gets parsed into
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a parsed question example 3'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -q "get computer name and ip route details" --picker 1 --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a more complex question in english with two sensors
Pick the first match that the english form gets parsed into
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a parsed question example 4'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -q "get computer name and ip route details" --picker 1 --no-results'''
e['notes'] = '''Ask a more complex question in english with two sensors
Pick the first match that the english form gets parsed into
Do not wait for results, just ask the question and return right away. In this use case, you would want to use get_results.py to get the results for this question later.
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

sname = 'ask_manual'
examples[sname] = []

e = {}
e['name'] = 'Ask a question example 1'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --sensor "Computer Name" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a question with a single sensor
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a question example 2'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --sensor "id:1" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a question with a single sensor by id
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a question example 3'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --sensor "Computer Name" --sensor "Installed Applications" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a question with two sensors
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a question example 4'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --sensor "Folder Contents{folderPath=C:\Program Files}" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a question with a sensor that requires parameters
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a question example 5'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --sensor "Operating System, that contains:Windows, opt:ignore_case, opt:max_data_age:60" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a question with a single sensor
Supply a filter in the sensor that limits the column data to .*Windows.* matches
Supply an option in the sensor that ignores case in the filter
Supply an option in the sensor that re-fetches cached data older than 1 minute
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a question example 6'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -s "Computer Name" -s "Folder Contents{folderPath=C:\Program Files, invalidparam=test}, that regex match:.*Shared.*, opt:max_data_age:3600" -f "Operating System, that contains:Windows" -f "IP Address, that not equals:10.10.10.10" -o "or" -o "ignore_case" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Ask a question with two sensors
Supply parameters to the 2nd sensor
Supply a filter in the 2nd sensor that limits the column data to .*Shared.*
Supply an option in the 2nd sensor that re-fetches cached data older than 1 minute
Supply a question filter that limits the rows returned to machines whose Operating System sensor match .*Windows.*
Supply a question filter that limits the rows returned to machines whose IP Address filter does not equal 10.10.10.10
Supply two question options, one to OR the question filters supplied, and another to ignore the case while matching the question filters
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a question example 7'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -s "Computer Name" -s "Last Logged In User" -s "Installed Applications, that contains:Google" -f "Installed Applications, that contains:Google" -f "Installed Applications, that contains:Chrome" -o "or" -o "ignore_case" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''
Ask a question with 4 sensors
Use filters on 3rd and 4th sensor to limit the column data to only show certain apps
Use 2 question filters to limit the row data to only show the same apps used in the sensor filters
Supply two question options, one to OR the question filters supplied, and another to ignore the case while matching the question filters
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for sensors'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --sensors-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for filters'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --filters-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for options'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --options-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

# ask_saved_question
sname = 'ask_saved'
examples[sname] = []

e = {}
e['name'] = 'Ask a saved question'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "Installed Applications" --file "${TMPDIR}/out.csv"'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Ask a saved question and refresh the data available before fetching the data'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "Installed Applications" --file "${TMPDIR}/out.csv" --refresh_data'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

# create_whitelisted_url
sname = 'create_whitelisted_url'
examples[sname] = []

e = {}
e['name'] = 'Create a whitelisted URL'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --url "https://testing.com/${RANDINT}" --regex --download 3600 --property "property name" "property value"'''
e['notes'] = '''Create a whitelisted_url for https://testing.com
Set the new URL as a regex pattern
Set thew new URL to be re-downloaded every 3600 seconds
Create a property named property name with the value property value on the new URL
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# create_package
sname = 'create_package'
examples[sname] = []

e = {}
e['name'] = 'Create a new package'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "1234 CMDLINE TEST package" --display-name "1234 CMDLINE TEST package display name" --command "testing.vbs \\$1 \\$2 \\$3 \\$4 \\$5 \\$6 \\$7 \\$8" --expire-seconds 1500 --file-url "3600::testing.vbs||https://testing.com/testing.vbs" --file-url "https://testing.com/another_testing.vbs" --parameters-file "doc/example_of_all_package_parameters.json" --verify-expire-seconds 3600 --verify-filter "Custom Tags, that contains:tag" --verify-option "ignore_case" --command-timeout 600'''
e['notes'] = '''
Create a package named 1234 CMDLINE TEST package
Set the display name in the console for the new package to 1234 CMDLINE TEST package display name
When this package is deployed, run the command testing.vbs and expect 8 arguments
When this package is deployed as part of an action, default the action to expire after 3600 seconds
Add a file to this package that will be redownloaded every 3600 seconds, named testing.vbs in Tanium, and downloaded from testing.com/testing.vbs
Add another file to this package that will be downloaded once, extract the file name from the URL, and downloaded from testing.com/another_testing.vbs
Add all the parameters defined in doc/example_of_all_package_parameters.json
Expire the verification filter after 3600 seconds
Expire the command if it takes longer than 600 seconds to run
Supply a verification filter that will be used when this package is deployed as part of an action
Supply an option for the verification filter that ignores case
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Delete the recently created package'
e['cmd'] = '''bin/delete_package.py ${API_INFO} --name "1234 CMDLINE TEST package"'''
e['notes'] = '''Delete the package named 1234 CMDLINE TEST package
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# create_group
sname = 'create_group'
examples[sname] = []

e = {}
e['name'] = 'Delete the group we want to create to ensure it does not pre-exist'
e['cmd'] = '''bin/delete_group.py ${API_INFO} --name "All Windows Computers CMDLINE TEST GROUP"'''
e['notes'] = '''Delete the group named All Windows Computers CMDLINE TEST GROUP
This may or may not fail -- thats fine!
'''
e['errormatch'] = 'no_match_test'
e['tests'] = 'noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Create a new group'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "All Windows Computers CMDLINE TEST GROUP" -f "Operating System, that contains:Windows" -f "IP Address, that not equals:10.10.10.10" -o "and" -o "ignore_case"'''
e['notes'] = '''
Create a group named All Windows Computers CMDLINE TEST GROUP
Supply a filter that limits the group members to machines that match .*Windows.* for the Operating System sensor
Supply a filter that limits the group members to machines that do not equal 10.10.10.10 for the IP Address sensor
Supply two options, one to AND the filters supplied, and another to ignore the case while matching the filters
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Delete the recently created group'
e['cmd'] = '''bin/delete_group.py ${API_INFO} --name "All Windows Computers CMDLINE TEST GROUP"'''
e['notes'] = '''Delete the group named All Windows Computers CMDLINE TEST GROUP
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for filters'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --filters-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for options'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --options-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

# deploy_action
sname = 'deploy_action'
examples[sname] = []

e = {}
e['name'] = 'Print the help for package'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --package-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for filters'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --filters-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Print the help for options'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --options-help'''
e['tests'] = 'notexitcode'
examples[sname].append(e)

e = {}
e['name'] = 'Deploy an action example 1'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --package "Distribute Tanium Standard Utilities" --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Deploys an action using the package Distribute Tanium Standard Utilities
Since --run was not supplied, the results of the question for the filters of this action will be written to a CSV file for verification, and the deploy action will NOT be run
'''
e['precleanup'] = 'rm -f ${TMPDIR}/VERIFY_BEFORE_DEPLOY_ACTION_out.csv'
e['file_exist'] = '${TMPDIR}/VERIFY_BEFORE_DEPLOY_ACTION_out.csv'
e['tests'] = 'notexitcode, file_exist_contents'
examples[sname].append(e)

e = {}
e['name'] = 'Deploy an action example 2'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --package "Distribute Tanium Standard Utilities" --run --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Deploys an action using the package Distribute Tanium Standard Utilities
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Deploy an action example 3'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --package "Custom Tagging - Add Tags{\\$1=new_tag}" --filter "Operating System, that contains:Windows" --run --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Deploys an action using the package "Custom Tagging - Add Tags", passing in a parameter for the tag to be added
Uses a filter to only deploy the action agains machines that match .*Windows.* for the Operating System sensor
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

# get_results
sname = 'get_results'
examples[sname] = []

e = {}
e['name'] = 'Ask a question'
e['cmd'] = '''bin/ask_manual.py ${API_INFO} --no-results --sensor "Computer Name" | tee ${TMPDIR}/ask.out'''
e['notes'] = '''Ask a question without getting the results, save stdout to ask.out
'''
e['precleanup'] = 'rm -f ${TMPDIR}/ask.out'
e['file_exist'] = '${TMPDIR}/ask.out'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Wait 30 seconds'
e['cmd'] = '''sleep 15'''
e['notes'] = '''Wait 30 seconds for data for the previously asked question to be available
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Get the results for a question'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -o "question" --id `cat ${TMPDIR}/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Get the results for the question ID asked previously
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Get the results for a question via a server side export'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -o "question" --id `cat ${TMPDIR}/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "${TMPDIR}/out.csv" --enable_sse'''
e['notes'] = '''Get the results for the question ID asked previously using a server side export
Save the results to a CSV file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

# create_user
sname = 'create_user'
examples[sname] = []

e = {}
e['name'] = 'Example 1: Delete the user we want to create to ensure it does not pre-exist'
e['cmd'] = '''bin/delete_user.py ${API_INFO} --name "CMDLINE TEST user"'''
e['notes'] = '''Delete the user named "CMDLINE TEST user"
This may or may not fail -- thats fine!
'''
e['errormatch'] = 'no_match_test'
e['tests'] = 'noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Example 1: Create a new user'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "CMDLINE TEST user" --rolename "Administrator" --property "property name" "property value"'''
e['notes'] = '''Create a user named CMDLINE TEST user
Assign the Administrator role to the new user
Create a property named property name with the value property value on the new user
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Example 1: Delete the recently created user'
e['cmd'] = '''bin/delete_user.py ${API_INFO} --name "CMDLINE TEST user"'''
e['notes'] = '''Delete the user by name
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Example 2: Delete the user we want to create to ensure it does not pre-exist'
e['cmd'] = '''bin/delete_user.py ${API_INFO} --name "CMDLINE TEST user"'''
e['notes'] = '''Delete the user named "CMDLINE TEST user"
This may or may not fail -- thats fine!
'''
e['errormatch'] = 'no_match_test'
e['tests'] = 'noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Example 2: Create a new user with a group specificied'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --name "CMDLINE TEST user" --rolename "Administrator" --property "property name" "property value" -g "All Computers"'''
e['notes'] = '''Create a user named CMDLINE TEST user and allow it only access to users in the "All Computers" group name
Assign the Administrator role to the new user
Create a property named property name with the value property value on the new user
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Example 2: Delete the recently created user'
e['cmd'] = '''bin/delete_user.py ${API_INFO} --name "CMDLINE TEST user"'''
e['notes'] = '''Delete the user by name
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# print_sensors
sname = 'print_sensors'
examples[sname] = []

e = {}
e['name'] = 'Print all sensors'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Print all Linux sensors'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all --platform Linux'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Print all Linux sensors that fall under the category "Operating System"'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all --platform Linux --category "Operating System"'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Print all Mac and Windows sensors that fall under the category "User"'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all --platform Mac --platform Windows --category "User"'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# print_server_info
sname = 'print_server_info'
examples[sname] = []

e = {}
e['name'] = 'Print the server info in JSON format'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --json'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# stop_action
sname = 'stop_action'
examples[sname] = []

e = {}
e['name'] = 'Stop a deploy action'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --id 1'''
e['notes'] = '''This will stop the action ID 1
This is essentially a no-op if the action has already expired/finished
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# approve_saved_action
sname = 'approve_saved_action'
examples[sname] = []

e = {}
e['name'] = 'Approve a saved action '
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --id 1'''
e['notes'] = '''This will approve the saved action ID 1
This is essentially a no-op if the Global Setting "require_action_approval" is not set to 1 or if the saved action is already approved
'''
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# # create_sensor
# sname = 'stop_action'
# examples[sname] = []

# e = {}
# e['name'] = 'Create a sensor'
# e['cmd'] = '''bin/${script_name}.py ${API_INFO} --unsupported True'''
# e['notes'] = '''This script is just a placeholder -- it does not actually work yet
# '''
# e['tests'] = 'notexitcode, noerror'
# examples[sname].append(e)

# create_json_object
sname = 'create_json_object'
examples[sname] = []

e = {}
e['name'] = 'Export ${objname} id 1 as JSON'
e['cmd'] = '''bin/get_${objname}.py ${API_INFO} --id 1 --file "${TMPDIR}/out.json" --export_format json'''
e['notes'] = '''Get the first ${objname} object
Save the results to a JSON file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.json'
e['file_exist'] = '${TMPDIR}/out.json'
e['tests'] = 'exitcode, file_exist_contents, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Change name or url_regex in the JSON'
e['cmd'] = '''perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST ${RANDINT}"/gm' ${TMPDIR}/out.json && cat ${TMPDIR}/out.json'''
e['notes'] = '''Add CMDLINE TEST to name or url_regex in the JSON file
'''
e['file_exist'] = '${TMPDIR}/out.json'
e['tests'] = 'exitcode, file_exist, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Create a new ${objname} from the modified JSON file'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} -j "${TMPDIR}/out.json"'''
e['precleanup'] = 'rm -f ${TMPDIR}/create.out'
e['tests'] = 'exitcode, noerror'
examples[sname].append(e)

# delete_object
sname = 'delete_object'
examples[sname] = []

e = {}
e['name'] = 'Delete ${objname}'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --id 123456'''
e['notes'] = '''This example does not actually run
'''
e['norun'] = 'true'
e['tests'] = 'noerror'
examples[sname].append(e)

# get_object
sname = 'get_object'
examples[sname] = []

e = {}
e['name'] = 'Export all ${objname} objects as JSON'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all --file "${TMPDIR}/out.json" --export_format json'''
e['notes'] = '''Get all ${objname} objects
Save the results to a JSON file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.json'
e['file_exist'] = '${TMPDIR}/out.json'
e['tests'] = 'exitcode, file_exist, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Export all ${objname} objects as CSV'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all --file "${TMPDIR}/out.csv"'''
e['notes'] = '''Get all ${objname} objects
Save the results to a csv file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.csv'
e['file_exist'] = '${TMPDIR}/out.csv'
e['tests'] = 'exitcode, file_exist, noerror'
examples[sname].append(e)

e = {}
e['name'] = 'Export all ${objname} objects as xml'
e['cmd'] = '''bin/${script_name}.py ${API_INFO} --all --file "${TMPDIR}/out.xml"'''
e['notes'] = '''Get all ${objname} objects
Save the results to a xml file
'''
e['precleanup'] = 'rm -f ${TMPDIR}/out.xml'
e['file_exist'] = '${TMPDIR}/out.xml'
e['tests'] = 'exitcode, file_exist, noerror'
examples[sname].append(e)


help_example = {}
help_example['name'] = 'Help for ${title_name}'
help_example['cmd'] = "${script_name}.py -h"
help_example['depth'] = '1'
help_example['notes'] = '''Print the help for ${script_name}.py
All scripts in bin/ will supply help if -h is on the command line
If passing in a parameter with a space or a special character, you need to surround it with quotes properly. On Windows this means double quotes. On Linux/Mac, this means single or double quotes, depending on what kind of character escaping you need.
If running this script on Linux or Mac, use the python scripts directly as the bin/${script_name}.py
If running this script on Windows, use the batch script in the winbin/${script_name}.bat so that python is called correctly.
'''
help_example['tests'] = 'exitcode, noerror'
