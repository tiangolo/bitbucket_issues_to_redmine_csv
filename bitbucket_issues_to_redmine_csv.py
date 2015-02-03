"""
Read a JSON file with issues exported from Bitbucket as in:
https://confluence.atlassian.com/display/BITBUCKET/Export+or+import+issue+data

Export that data to a CSV file formatted according to the plug-in Redmine Importer:
https://github.com/leovitch/redmine_importer/wiki

Use the latest version of the plug-in from: https://github.com/zh/redmine_importer
"""

import json
import csv

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file_in', help='a JSON file with issues exported from Bitbucket.')
    parser.add_argument('file_out', help='a CSV file to write issues in Redmine Import format.')
    parser.add_argument('--user-map', help='a CSV file with two columns, one with a Bitbucket username and another with\
                        the corresponding Redmine username.')

    args = parser.parse_args()

    file_in = args.file_in
    file_out = args.file_out
    user_map = args.user_map

    # TODO remove this, only for debugging
    file_in_ = file_in
    file_out_ = file_out
    user_map_ = user_map

    # Main program
    read_file = open(file_in_)
    json_data = json.load(read_file)
    read_file.close()
    write_file = open(file_out_, 'w')
    csv_writer = csv.writer(write_file, lineterminator='\n')
    user_dict = None
    if user_map_:
        map_file = open(user_map_)
        user_map_reader = csv.reader(map_file)
        user_dict = dict([row for row in user_map_reader])
        map_file.close()

    def get_user(username):
        """
        Convert the username from Bitbucket to a Redmine username. If no user_map was given, return the same username.

        :param username: username to convert.
        :return: Redmine username to use.
        """
        if user_dict is None:
            return username
        else:
            return user_dict[username]

    def none_to_empty(element):
        """
        Convert a data element to an empty string if it is None.

        :param element: element to convert.
        :return: an empty string if element is None, else, the element as is.
        """
        if element is None:
            return ''
        else:
            return element

    header = ['Subject', 'Description', 'Assigned To', 'Fixed version', 'Author', 'Category', 'Priority', 'Tracker',
              'Status', 'Start date', 'Due date', 'Done Ratio', 'Estimated hours', 'Watchers', 'blocked by', 'blocks',
              'duplicated by', 'duplicates', 'follows', 'precedes', 'related to', 'Parent Issue', 'Id']
    dataset = []
    for issue in json_data['issues']:
        watchers = ','.join(map(get_user, issue['watchers']))
        new_row = [issue['title'], issue['content'], get_user(issue['assignee']), issue['version'],
                   get_user(issue['reporter']), None, issue['priority'], issue['kind'], issue['status'],
                   issue['created_on'], None, None, None, watchers, None, None, None, None, None,
                   None, None, None, None]
        unused_data = [issue['component'], issue['content_updated_on'], issue['edited_on'], issue['id'],
                       issue['milestone'], issue['updated_on'], issue['voters']]
        for comment in json_data['comments']:
            if comment['issue'] == issue['id']:
                new_row[1] += '\n\nComment: ' + unicode(comment['created_on']) + ' - ' + unicode(
                    get_user(comment['user'])) + ': ' + unicode(comment['content'])
        no_none_new_row = map(none_to_empty, new_row)
        encoded_new_row = [unicode(el).encode('utf-8') for el in no_none_new_row]

        dataset.append(encoded_new_row)
    csv_writer.writerow(header)
    csv_writer.writerows(dataset)
    write_file.close()
