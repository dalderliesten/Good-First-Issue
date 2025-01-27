from tagged_issues import TaggedIssues
from user_commits import UserCommits

import socket


class GoodFirstIssue:
    """Handles main application logic and does all tasks.

    This class is responsible for the aggregation of all data required and utilized in the repository mining, and
    dictates tasks to all sub-components of the program.

    Methods
    -------
    main()
        Entry point for the application which dictates all behavior.
    """

    @staticmethod
    def main():
        """Performs all program logic and dictates all behavior, entry point for the program.

        Requires the manual entry of Github API key on line 24, repository link as described above the declaration on
        line 28, and the manual entry of the desired tag to analyze on line 31.
        """
        try:
            # Provide the Github API key to utilize.
            api_key = "ADD API KEY"

            # Define location of the repository. This should be an https:// link to Github with the .git still on it.
            # This can be obtained by going to a repository's site and selecting the 'clone or download -> https'
            # option.
            repository = "ADD REPO .git LOCATION"

            # Define the name of the good-first-issue tag used in the repository to analyze.
            first_issue_tag = "good first issue"

            # Get first commits for each user in the repository.
            user_commits = UserCommits.get_first_commits(repository, api_key)

            # Get all tagged issues within the repository.
            tagged_issues = TaggedIssues.get_tagged_issues(repository, api_key, first_issue_tag)
        except socket.timeout:
            print('Timeout took place, repository should be re-run. Catch hopefully saves part of data.')


# Main method call for program execution.
GoodFirstIssue.main()
