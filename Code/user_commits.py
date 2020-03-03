from github import Github
import csv


class UserCommits:
    """Handles all data related to user commits

    This class contains methods and logic related to the identification of the first commits for user within a
    repository, and the storing of this data in a CSV file. A single repository can be analyzed at
    once by calling the get_first_commits method with your repository URL or location as an argument.

    Methods
    -------
    get_first_commits(repository: str)
        Gets all first commits of all users for the given repository location, and stores them each in a CSV.
    """

    def get_first_commits(repository: str, api_key: str) -> dict:
        """Obtains the first commits per user for the given repository in the argument.

        Employs PyDriller to iterate over all commits and identifies all first commits by iterating over all existing
        commits. Also order a write to be done of the identified commits for validation purposes.

        Parameters
        ----------
        repository : str
            The repository that requires the first commits per user to be obtained.

        Returns
        -------
        dict
            A dictionary containing all the first commits found for the repository.
        """

        # Variable to obtain / track the first commit to a project by users, and to track found users.
        initial_commit = []
        users_tracked = []

        # Creating a Github object with a token for utilization and a greater allowed number of requests to the API.
        github_access = Github(api_key)

        # Trim given repository string to match PyGithub requirements but not break compatibility with rest of tool.
        name = UserCommits.trim_repository_name(repository)

        # Get repository to analyze.
        repo = github_access.get_repo(name)

        # Store all commits found within the repository. This needs to be done because doing it within the for-loop
        # causes fetching of infinite commits, thereby causing an infinite loop AND using a TON all Github API requests.
        # The order is reversed because the Github API returns commits as last to first, but we need first to last.
        total_commits = repo.get_commits().reversed

        # Notifying user that commit identification is starting.
        print('---------- FETCHING FIRST COMMIT FOR EACH USER IN THE REPOSITORY ----------')

        # Obtain all initial / first commits by iterating through desired repository and comparing the names to the
        # already seen commits.
        for commit in total_commits:
            # Filtering out NoneType users (who deleted their account) to prevent errors.
            if commit.author is not None:
                # Filtering out empty URLs from old/deleted accounts.
                if commit.url is not None:
                    print(f'Commit found created by {commit.author.login}.')
                    if commit.author.login not in users_tracked:
                        users_tracked.append(commit.author.login)
                        initial_commit.append(commit)
                        print(f'+++ Identified first commit by {commit.author.login}.')

        # Write results to CSV for storage and later use/validation by user.
        print('Writing identified first commits to a CSV...')
        UserCommits.write_first_commit_results_to_csv(initial_commit, repository)

        # Return initial commits found.
        return initial_commit

    def trim_repository_name(name: str) -> str:
        """Trims the name of the repository to match (Py)Github's API requirements.

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

    def write_first_commit_results_to_csv(results: dict, name: str):
        """Writes the found results for first commits by a user to a CSV file. Also handles trimming of the file such
        that the git and slash information is removed for file storage.

        Parameters
        ----------
        results : dict
            The list of commits that must be stored.
        name : str
            The name of the repository.
        """
        # Obtain positions of slashes and git extension for later removal.
        last_slash_index = name.rfind("/")
        last_suffix_index = name.rfind(".git")

        # Identify last index of a non-name component of the repository URL/location.
        if last_suffix_index < 0:
            last_suffix_index = len(name)

        # Validate slash position and last suffix position, and throw an error if they are invalid.
        if last_slash_index < 0 or last_suffix_index <= last_slash_index:
            raise Exception(f"Badly formatted Git URL for the {name} repository...")

        # Set name to the new name without slashes or issues and to represent the repository name.
        location = name[last_slash_index + 1:last_suffix_index]

        # Trim the .git off of the name to use for link identification.
        name = name.rstrip('.git')

        # Create CSV file and write data to file in UTF-8 format for possible non-Western characters.
        with open(f"results_first_commit_{location}.csv", mode='w', encoding="utf-8") as csv_file:
            # Set CSV writer properties to account for possible quoted usernames and properties.
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['First Commit Hash (SHA)',
                                 'Commit Message',
                                 'Author (Github Name)',
                                 'Link to Commit'])

            # Iterate through all found commits, and put them into the CSV file with the CSV writer with additionally
            # related aspects of the commit.
            for current in results:
                # Consider case where no URL exists due to outdated elements in the API and catch it if needed.
                url_to_use = ''

                # Handle lack of URL exception.
                try:
                    url_to_use = current.commit.url
                except:
                    url_to_use = 'URL ERROR - API FAULT.'

                # Write current commit found to CSV.
                csv_writer.writerow([current.sha,
                                     current.commit.message,
                                     current.author.login,
                                     url_to_use])

        # Notify user that process regarding commits is done.
        print('Finished writing to CSV...')
