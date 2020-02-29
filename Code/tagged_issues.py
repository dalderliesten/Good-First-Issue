from github import Github
import csv


class TaggedIssues:
    """Handles the fetching and storing of issues tagged with a specific phrase.

    This class contains methods and logic related to the identification and obtaining of issues with a certain tag,
    such as the 'good first issue' tag that is utilized for this research. It obtains these using Github's V3 API.

    Methods
    -------
    get_tagged_issues(repositories: str)
        Gets all issues with the define tag and the given repository reference and stores them in a CSV file.
    """

    def get_tagged_issues(repository: str, api_key: str, tag: str) -> dict:
        """Gets all the tagged issues with the desired tag and returns a dict containing them.

        Utilizing Github's API, the given repository string is trimmed to match Github's API requirements, after which
        the given tag is converted to a Github label object and searched for within the given repository. This list is
        then returned as a dict object.

        Parameters
        ----------
        repository : str
            The repository for which the tagged issues must be found.
        tag : str
            The tag which must be identified. NOTE: must be singular!

        Returns
        -------
        dict
            A dict containing all issues with the given tag within the given repository.
        """
        # Creating a Github object with a token for utilization and a greater allowed number of requests to the API.
        github_access = Github(api_key)

        # Trim given repository string to match PyGithub requirements but not break compatibility with rest of tool.
        name = TaggedIssues.trim_repository_name(repository)

        # Get repository to analyze.
        repo = github_access.get_repo(name)

        # Informing user that issue fetching is beginning for logging purposes.
        print(f'---------- FETCHING ISSUES TAGGED WITH {tag} FROM REPOSITORY ----------')

        # Convert the desired tag to a Github compliant tag as per PyGithub's requirements (it was an object, not a
        # string).
        tag_compliant = repo.get_label(tag)

        # Get all issues with the identifier 'tag' as given in the method argument. Also indicates all issues are
        # wanted, and not only 'open' issues, which is the default API behavior if left undeclared.
        print('Getting issues from Github API...')
        good_first_issues = repo.get_issues(labels=[tag_compliant], state='all')

        # Store found issues in a CSV for validation.
        print('Writing found issues to CSV...')
        TaggedIssues.write_issue_results_to_csv(good_first_issues, repository)

        # Return the found first issues with the tag.
        return good_first_issues

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

    def write_issue_results_to_csv(results: dict, name: str):
        """Writes the found issues and their associated relevant data to a CSV file. Also handles trimming of the file
        such that the git and slash information is removed for file storage.

        Parameters
        ----------
        results : dict
            The list of issues and associated data that must be stored.
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

        # Create CSV file and write data to file in UTF-8 format for possible non-Western characters.
        with open(f"results_good_first_issues_{location}.csv", mode='w', encoding="utf-8") as csv_file:
            # Set CSV writer properties to account for possible quoted usernames, characters, and/or properties.
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Issue Description', 'Assignees to the Issue', 'Link'])

            # Iterate through all found issues and store them within a CSV file along with relevant information.
            for current in results:
                # Isolate a single string with all assignee due to the possibilities of there being multiple users.
                assigned_users = ''

                # Get user login display name on Github for assignee string.
                for user in current.assignees:
                    assigned_users + user.login

                # Write row itself to CSV.
                csv_writer.writerow([current.title,
                                     assigned_users,
                                     current.html_url])

        # Log termination for tracking and logging uses.
        print('Finished writing to CSV...')
