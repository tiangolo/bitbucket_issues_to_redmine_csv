===============================
Bitbucket Issues to Redmine CSV
===============================

Read a JSON file with issues exported from Bitbucket as in:
https://confluence.atlassian.com/display/BITBUCKET/Export+or+import+issue+data

Export that data to a CSV file formatted according to the plug-in Redmine Importer:
https://github.com/leovitch/redmine_importer/wiki

Use the latest version of the plug-in from: https://github.com/zh/redmine_importer

If the names of the users in Bitbucket are different from the names of the users in Redmine, it can use a mapping file:
a CSV file with one column with the username from Bitbucket and another column with the username from Redmine, for
example:
::
     username, user.name
     anotheruser, redmine_another_user
     sameusername, sameusername
     
     
Usage:
------

* Download a zip file with the issues of a Bitbucket project.
* Unzip that file to some directory.
* Create a mapping CSV file with the syntax described above for your users.
* Download the file ``bitbucket_issues_to_redmine_csv.py`` from this repository.
* Run the program as:
``python download_directory/bitbucket_issues_to_redmine_csv.py json_directory/db-1.0.json csv_output_directory/csv_name.csv --user-map user_map_directory/user_map.csv``

Multiple Bitbucket repositories:
--------------------------------

To convert the issues of many Bitbucket repositories in batch, do the following:

* Download the issues zip files from Bitbucket, from each repository.
* Go to the downloads directory
* Unzip all the zip files, each in its own directory (the CSV issue files will be put inside those directories).
* Download ``process_directory.py`` and ``bitbucket_issues_to_redmine_csv.py`` from this repository.
* Create a mapping CSV file with the syntax described above for your users.
* Run the program as:
``python download_directory/process_directory.py json_root_directory/ csv_output_name.csv --user-map user_map_directory/user_map.csv``

