Get Results Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Get Results Help](#user-content-get-results-help)
  * [Ask a question](#user-content-ask-a-question)
  * [Wait 30 seconds](#user-content-wait-30-seconds)
  * [Get the results for a question](#user-content-get-the-results-for-a-question)

---------------------------

# Get Results Help

  * Get results from a deploy action, saved question, or question

```bash
get_results.py -h
```

```
usage: get_results.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                      [--port PORT] [-l LOGLEVEL] -o
                      {saved_question,question,action} -i OBJECT_ID
                      [--file REPORT_FILE] [--dir REPORT_DIR]
                      {csv,json} ...

Get results from a deploy action, saved question, or question

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        444)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Get Result Options:
  -o {saved_question,question,action}, --object {saved_question,question,action}
                        Type of object to get results for (default: )
  -i OBJECT_ID, --id OBJECT_ID
                        id of object to get results for (default: )

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Export Formats:
  {csv,json}            Export Format choices
    csv                 Produce a CSV report, supply "csv -h" to see CSV
                        options
    json                Produce a JSON report, supply "json -h" to see JSON
                        options

usage: get_results.py csv [-h] [--sort HEADER_SORT | --no-sort | --auto_sort]
                          [--add-sensor | --no-add-sensor]
                          [--add-type | --no-add-type]
                          [--expand-columns | --no-columns]

CSV Export Options

optional arguments:
  -h, --help          show this help message and exit
  --sort HEADER_SORT  Sort headers by given names (default: [])
  --no-sort           Do not sort the headers at all
  --auto_sort         Sort the headers with a basic alphanumeric sort
                      (default)
  --add-sensor        Add the sensor names to each header
  --no-add-sensor     Do not add the sensor names to each header (default)
  --add-type          Add the result type to each header
  --no-add-type       Do not add the result type to each header (default)
  --expand-columns    Expand multi-line cells into their own rows that have
                      sensor correlated columns in the new rows
  --no-columns        Do not add expand multi-line cells into their own rows
                      (default)

usage: get_results.py json [-h]

JSON Export Options

optional arguments:
  -h, --help  show this help message and exit
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Ask a question

  * Ask a question without getting the results, save stdout to ask.out

```bash
ask_manual_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --no-results --sensor "Computer Name" csv | tee /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/ask.out
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": false, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Computer Name"
  ], 
  "sensors_help": false
}
++ Asked Question 'Get Computer Name from all machines' ID: 11477
++ No action results returned, run get_results.py to get the results
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/ask.out exists, content:

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Asking manual question:
{
  "filters_help": false, 
  "get_results": false, 
  "options_help": false, 
  "question_filters": [], 
  "question_options": [], 
  "sensors": [
    "Computer Name"
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Wait 30 seconds

  * Wait 30 seconds for data for the previously asked question to be available

```bash
sleep 15
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Get the results for a question

  * Get the results for the question ID asked previously
  * Save the results to a CSV file

```bash
get_results.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -o "question" --id `cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/ask.out | grep ID| cut -d: -f2 | tr -d " "` --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3258
++ Found object: Question, id: 11477
++ Found results for object: ResultSet for 11477, ColumnSet: Computer Name, Count
++ Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 56 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Computer Name
Casus-Belli.local
jtanium1.localdomain
```



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Wed Feb 11 17:17:52 2015 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**