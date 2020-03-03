from pull_requests import PullRequests
from tagged_issues import TaggedIssues
from user_commits import UserCommits


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
        # Provide the Github API key to utilize.
        api_key = "34b8204b93e9ac470e5f34f55fe3f780a1a71c45"

        # Define location of the repository. This should be an https:// link to Github with the .git still on it. This
        # can be obtained by going to a repository's site and selecting the 'clone or download -> https' option.
        repository = "https://github.com/microsoft/DeepSpeed.git"

        # Define the name of the good-first-issue tag used in the repository to analyze.
        first_issue_tag = "good first issue"

        # Get first commits for each user in the repository.
        user_commits = UserCommits.get_first_commits(repository, api_key)

        # Get all tagged issues within the repository.
        tagged_issues = TaggedIssues.get_tagged_issues(repository, api_key, first_issue_tag)

        # Get all pull requests in a repository. NOTE: DOESN'T WORK BECAUSE API LIMITS DON'T SUPPORT USEFULNESS.
        #pull_requests = PullRequests.get_related_pull_requests(repository, api_key, user_commits, tagged_issues)

# Main method call for program execution.
GoodFirstIssue.main()