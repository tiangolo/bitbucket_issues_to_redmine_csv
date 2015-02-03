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

