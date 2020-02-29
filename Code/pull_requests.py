from github import Github
import csv


class PullRequests:
    """Handles the fetching and storing of pull requests related to tagged issues and commits.

    This class contains methods and logic related to the identification of pull requests that have some relation to
    good first issues and commits identified and passed to it with the goal of identifying and querying related
    pull requests from the Github API.

    Methods
    -------
    get_related_pull_requests(repository: str, api_key: str, commits_found: dict, issues_found: dict)
        Entry point for the class aiming to fetch all pull requests related to the query based on issues and commits.
    """

    def get_related_pull_requests(repository: str, api_key: str, commits_found: dict, issues_found: dict):
        # Creating a Github object with a token for utilization and a greater allowed number of requests to the API.
        github_access = Github(api_key)

        # Trim given repository string to match Github requirements but not break compatibility with rest of tool.
        name = PullRequests.trim_repository_name(repository)

        # Get repository to analyze.
        repo = github_access.get_repo(name)

        # Declare variable to store all pull requests to store and declare logging init for user.
        print('---------- FETCHING PULL REQUESTS THAT MATCH GIVEN ISSUES/COMMITS FROM REPOSITORY ----------')
        relevant_pull_requests = []

        # Get all pull requests for this repository in any state, since default behavior dictates only OPEN pull
        # requests to be returned.
        all_pull_requests = repo.get_pulls(state='all')

        # Filter out pull requests based on passed commits to find matches.
        for request in all_pull_requests:
            for commit in commits_found:
                if commit.author.login in request.user.name:
                    print('  Found a match!!!')


    def trim_repository_name(name: str) -> str:
        """Trims the name of the repository to match Github's API requirements.

        Removes the last 4 characters, containing the git file declaration ('.git'), and removes the initial 19
        characters, which contain the Github referral ('https://github.com/').

        Parameters
        ----------
        repository : str
            The repository whose API compliant name is required.

        Returns
        -------
        str
            A string containing the repository name as required by Github's API mechanism.
        """
        # Strip the last 4 characters, containing '.git'.
        name = name[:-4]

        # Strip the first 19 characters, containing the URL and Github referral (https://github.com/).
        name = name[19:]

        # Return the changed name to the caller.
        return name
