"""
Convert the issues of many Bitbucket repositories in batch.
"""
import os
import os.path

import bitbucket_issues_to_redmine_csv

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root_directory', help='root directory with directories inside with Bitbucket\'s JSON files \
                        with issues.')
    parser.add_argument('--user-map', help='a CSV file with two columns, one with a Bitbucket username and another with\
                        the corresponding Redmine username.')
    parser.add_argument('--include-relations', help='set this flag if the output CSV should include relations between\
                        issues (which is currently not implemented).', action='store_true')
    args = parser.parse_args()

    root_directory = args.root_directory
    user_map = args.user_map
    include_relations = args.include_relations

    # TODO remove this, only for debugging
    root_directory_ = root_directory
    user_map_ = user_map
    include_relations_ = include_relations

    # Main execution
    directories_to_process = os.listdir(root_directory_)
    directories_to_process = [os.path.join(root_directory_, dir_name) for dir_name in
                              directories_to_process]
    directories_to_process = [use_dir for use_dir in directories_to_process if os.path.isdir(use_dir)]
    for use_dir in directories_to_process:
        files_list = os.listdir(use_dir)
        json_files = [use_file for use_file in files_list if use_file.lower().endswith('.json')]
        files_paths = [os.path.join(use_dir, use_file) for use_file in json_files]
        files_out_paths = [os.path.join(use_dir, os.path.basename(os.path.splitext(use_file)[0])) + '.csv' for use_file
                           in json_files]
        for read_path, write_path in zip(files_paths, files_out_paths):
            bitbucket_issues_to_redmine_csv.main(read_path, write_path, user_map_, include_relations_)



