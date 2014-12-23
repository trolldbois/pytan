Delete Saved Question Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Delete Saved Question Help](#user-content-delete-saved-question-help)
  * [Delete saved_question](#user-content-delete-saved_question)

---------------------------

# Delete Saved Question Help

  * Delete a saved_question object

```bash
delete_saved_question.py -h
```

```
usage: delete_saved_question.py [-h] -u USERNAME -p PASSWORD --host HOST
                                [--port PORT] [-l LOGLEVEL] [--id ID]
                                [--name NAME]

Delete a saved_question object

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

Delete Saved question Options:
  --id ID               id of saved_question to get (default: [])
  --name NAME           name of saved_question to get (default: [])
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Delete saved_question

  * This example does not actually run

```bash
delete_saved_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 123456
```



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Mon Dec  8 15:34:10 2014 EST, Contact info: **Jim Olsen <jim.olsen@tanium.com>**