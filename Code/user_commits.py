from pydriller import RepositoryMining, GitRepository
import csv
import git


class UserCommits:
    """Handles all data related to user commits

    This class contains methods and logic related to the identification of the first commits for user within a
    repository, and the storing of this data in a CSV file. A single or multiple repositories can be analyzed at
    once by calling the get_first_commits method with your repository URL or location as an argument.

    Methods
    -------
    get_first_commits(repositories: dict)
        Gets all first commits of all users for all the given repositories in the dict, and stores them each in a CSV.
    get_first_commits(repository: str)
        Gets all first commits of all users for the given repository location, and stores them each in a CSV.
    """

    def get_first_commits(repositories: dict) -> dict:
        """Obtains the first commits per user for the given repositories in the argument.

        Achieves this by making multiple calls to the string-based get_first_commits method of this class, and the
        same functionality can be achieved by making multiple calls to that method as calling this method.

        Parameters
        ----------
        repositories : dict
            The list of repositories that require the first commits per user to be obtained.

        Returns
        -------
        dict
            A dictionary containing all the first commits found for all repositories.
        """
        for repository in repositories:
            UserCommits.get_first_commits(repository)

    def get_first_commits(repository: str) -> dict:
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

        # Obtain all initial / first commits by iterating through desired repository and comparing the names to the
        # already seen commits.
        for commit in RepositoryMining(repository).traverse_commits():
            if commit.committer.name not in users_tracked:
                users_tracked.append(commit.committer.name)
                initial_commit.append(commit)

        # Write results to CSV for storage and later use/validation by user.
        UserCommits.write_first_commit_results_to_csv(initial_commit)

    # TODO: obtain Github URL for commits to associate in file.
    # TODO: set file name to project repo name.
    def write_first_commit_results_to_csv(results: dict):
        """Writes the found results for first commits by a user to a CSV file.

        Parameters
        ----------
        results : dict
            The list of commits that must be stored.
        """
        # Define location to store results for current repository.
        location = "results_first_commit_.csv"

        with open(location, mode='w') as csv_file:
            # Set CSV writer properties to account for possible quoted usernames and properties.
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['First Commit Hash', 'Git Identification / Name'])

            # Iterate through all found commits, and put them into the CSV file with the CSV writer.
            for current in results:
                csv_writer.writerow([current.hash, current.committer.name])
