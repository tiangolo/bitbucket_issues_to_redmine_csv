"""
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
"""

import json
import csv


def get_json_data(file_in_):
    """
    Return a json dict / list from a file path.

    :param file_in_: file path to JSON file.
    :return: json dict / list
    """
    read_file = open(file_in_)
    json_data = json.load(read_file)
    read_file.close()
    return json_data


def get_user_dict_function(user_map_):
    """
    Return a function that converts a username from Bitbucket to Redmine, using a user_map_, if no user_map_ is given,
    the function returns the same username.

    :param user_map_: CSV file path of the user mapping.
    :return: function that converts usernames
    """
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
            return user_dict.get(username, '')

    return get_user


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


def json_to_list(json_data, get_user, include_relations_):
    """
    Convert a json of Bitbucket issues to Redmine CSV.

    :param json_data: the json dict / list
    :param get_user: a function that converts usernames from Bitbucket to Redmine
    :param include_relations_: if set to True, use the full header and fields for each column.
    :return: a dataset of row issues without header
    :rtype: list
    """
    dataset = []
    if include_relations_:
        header = ['Subject', 'Description', 'Assigned To', 'Fixed version', 'Author', 'Category', 'Priority', 'Tracker',
                  'Status', 'Start date', 'Due date', 'Done Ratio', 'Estimated hours', 'Watchers', 'blocked by',
                  'blocks',
                  'duplicated by', 'duplicates', 'follows', 'precedes', 'related to', 'Parent Issue', 'Id']
    else:
        header = ['Subject', 'Description', 'Assigned To', 'Fixed version', 'Author', 'Category', 'Priority', 'Tracker',
                  'Status', 'Start date', 'Due date', 'Done Ratio', 'Estimated hours', 'Watchers']
    for issue in json_data['issues']:
        watchers = ','.join(map(get_user, issue['watchers']))
        kind = convert_kind(issue['kind'])
        priority = convert_priority(issue['priority'])
        status = convert_status(issue['status'])
        if include_relations_:
            new_row = [issue['title'], issue['content'], get_user(issue['assignee']), issue['version'],
                       get_user(issue['reporter']), None, priority, kind, status,
                       issue['created_on'], None, None, None, watchers, None, None, None, None, None,
                       None, None, None, None]
        else:
            new_row = [issue['title'], issue['content'], get_user(issue['assignee']), issue['version'],
                       get_user(issue['reporter']), None, priority, kind, status,
                       issue['created_on'], None, None, None, watchers]
        unused_data = [issue['component'], issue['content_updated_on'], issue['edited_on'], issue['id'],
                       issue['milestone'], issue['updated_on'], issue['voters']]
        for comment in json_data['comments']:
            if comment['issue'] == issue['id']:
                new_row[1] += '\n\nComment: ' + unicode(comment['created_on']) + ' - ' + unicode(
                    get_user(comment['user'])) + ': ' + unicode(comment['content'])
        no_none_new_row = map(none_to_empty, new_row)
        encoded_new_row = [unicode(el).encode('utf-8') for el in no_none_new_row]
        dataset.append(encoded_new_row)
    dataset.insert(0, header)
    return dataset


def save_issues_csv(file_out_, dataset):
    """
    Write a CSV file with a header and a dataset (a list of lists).

    :param file_out_: path to file to write.
    :param dataset: a list of lists of elements, to use as the content of the CSV file, including a header.
    :return:
    """
    write_file = open(file_out_, 'w')
    csv_writer = csv.writer(write_file, lineterminator='\n')
    csv_writer.writerows(dataset)
    write_file.close()


def convert_priority(bitbucket_priority):
    """
    Convert a Bitbucket priority to a Redmine priority.

    :param bitbucket_priority: string with the priority to convert.
    :return: the new Redmine priority.
    :rtype: str
    """
    items = {'trivial': 'Low',
             'minor': 'Normal',
             'major': 'High',
             'critical': 'Urgent',
             'blocker': 'Immediate'}
    return items.get(bitbucket_priority, '')


def convert_kind(bitbucket_kind):
    """
    Convert a Bitbucket Kind to a Redmine Tracker.

    :param bitbucket_kind: string with the kind to convert.
    :return: the new Redmine tracker.
    :rtype: str
    """
    items = {'bug': 'Bug',
             'enhancement': 'Feature',
             'proposal': 'Feature',
             'task': 'Task'}
    return items.get(bitbucket_kind, '')


def convert_status(bitbucket_status):
    """
    Convert a Bitbucket status to a Redmine status.

    :param bitbucket_status: string with the status to convert.
    :return: the new Redmine status.
    :rtype: str
    """
    items = {'new': 'New',
             'open': 'In Progress',
             'on hold': 'New',
             'resolved': 'Resolved',
             'duplicate': 'Rejected',
             'invalid': 'Rejected',
             'wontfix': 'Rejected',
             'closed': 'Closed'}
    return items.get(bitbucket_status, '')


def main(file_in_, file_out_, user_map_, include_relations_):
    """
    Main execution of the program, calling external functions.

    :param file_in_: file path to a JSON file to read.
    :param file_out_: file path to a CSV file to write.
    :param user_map_: file path to a CSV file with a mapping of users or None.
    :return:
    """
    json_data = get_json_data(file_in_)
    get_user = get_user_dict_function(user_map_)
    dataset = json_to_list(json_data, get_user, include_relations_)
    save_issues_csv(file_out_, dataset)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file_in', help='a JSON file with issues exported from Bitbucket.')
    parser.add_argument('file_out', help='a CSV file to write issues in Redmine Import format.')
    parser.add_argument('--user-map', help='a CSV file with two columns, one with a Bitbucket username and another with\
                        the corresponding Redmine username.')
    parser.add_argument('--include-relations', help='set this flag if the output CSV should include relations between\
                        issues (which is currently not implemented).', action='store_true')
    args = parser.parse_args()

    file_in = args.file_in
    file_out = args.file_out
    user_map = args.user_map
    include_relations = args.include_relations

    # Main program
    main(file_in, file_out, user_map, include_relations)