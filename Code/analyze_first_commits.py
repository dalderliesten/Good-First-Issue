from pydriller import RepositoryMining

# Variable indicating which repositories should be mined. More can be added by adding a comma (',')
# between each desired repository. Can be either local or remote using an URL.
repositories = ["https://github.com/getify/You-Dont-Know-JS"]

# Variable to obtain / track the first commit to a project by users, and to track found users.
initial_commit = []
users_tracked = []

# Obtaining all initial / first commits by iterating through desired repositories and comparing the
# names to the already seen commits.
for commit in RepositoryMining(repositories).traverse_commits():
    if commit.committer.name not in users_tracked:
        users_tracked.append(commit.committer.name)
        initial_commit.append(commit)

# Display the unique hashes for the first commits and name of the associated user.
# TODO: automatically obtain hash as 'git hash' command? Track repository commit origin for this.
# TODO 2: cross reference with issues of user / exist?
for current in initial_commit:
    print(current.hash + '          (First from contributor: ' + current.committer.name + ')')