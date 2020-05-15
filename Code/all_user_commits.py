from github import Github


class AllCommits:
    """Gets all user commits within a single repository.

    This class contains methods and logic related to the obtaining of all user commits of a user within a repository.
    Created with the purpose of performing additional analysis for the 'documentation' label and to investigate if any
    effect existed upon the subsequent commit. Requires mostly manual work, separate from main scripts/program.

    Methods
    -------
    get_all_commits()
        Gets all commits within a repository for the user.
    """

    def get_all_commits():
        # Provide the Github API key to utilize.
        api_key = "af79c9a76fb12207f37a85adf01e8897ce2575ca"

        # Define location of the repository. This should be an https:// link to Github with the .git still on it.
        # This can be obtained by going to a repository's site and selecting the 'clone or download -> https'
        # option.
        repository = "xamarin/Xamarin.Forms"

        # Declare user to find commits of.
        desired_user = "VincentDondain"

        # Get Github access with api key access.
        github_access = Github(api_key)

        # Get repository to analyze as Github object.
        repo = github_access.get_repo(repository)

        # Get all commits of a user and store them.
        user_commits = repo.get_commits(author=desired_user)

        print(user_commits.totalCount)

        # Iterate through all commits and list relevant information.
        for i, commit in enumerate(user_commits):
            print(i + 1, commit.url)


AllCommits.get_all_commits()