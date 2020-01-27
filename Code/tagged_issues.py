from github import Github


class TaggedIssues:
    """Handles the fetching and storing of issues tagged with a specific phrase.

    This class contains methods and logic related to the identification and obtaining of issues with a certain tag,
    such as the 'good first issue' tag that is utilized for this research. It obtains these using Github's V3 API.

    Methods
    -------
    get_tagged_issues(repositories: str)
        Gets all issues with the define tag and the given repository reference and stores them in a CSV file.
    """

    def get_tagged_issues(repository: str, tag: str) -> dict:
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
        # Creating a Github object with token for utilization.
        # TODO: Remove this once finished and delete token for history BEFORE making public.
        githubaccess = Github("b7c4b588dd912a79197b60195977b298c4e45e28")

        # Trim given repository string to match PyGithub requirements but not break compatibility with rest of tool.
        name = TaggedIssues.trim_repository_name(repository)

        # Get repository to analyze.
        repo = githubaccess.get_repo(name)

        # Convert the desired tag to a Github compliant tag as per PyGithub's requirements (it was an object, not a
        # string).
        tag_compliant = repo.get_label(tag)

        # Get all issues with the identifier 'tag' as given in the method argument.
        good_first_issues = repo.get_issues(labels=[tag_compliant])

        # TODO: remove debug: print out all found issues.
        for current in good_first_issues:
            print(current)

        # Return the found first issues with the tag.
        return good_first_issues

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
