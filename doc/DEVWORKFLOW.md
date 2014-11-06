# Using git flow to maintain pytan

## Install git flow

```
cd /tmp
wget --no-check-certificate -q -O - https://github.com/nvie/gitflow/raw/develop/contrib/gitflow-installer.sh | sudo bash
```

## Get initial copy of pytan repo

Generate SSH keys:
  * See https://help.github.com/articles/generating-ssh-keys/

Use clone to copy the repo locally:
```
mkdir ~/gh ; cd ~/gh
git clone git@github.com:tanium/pytan.git
```

Init git flow in the repo
```
cd ~/gh/pytan
git flow init -d
```

## Make the develop branch available locally

List all the branches:

```
git branch -vva
```

output:
```
* master                 b0ebdc6 [origin/master] Merge pull request #2 from tanium/develop
  remotes/origin/HEAD    -> origin/master
  remotes/origin/develop 1cf838b Merge branch 'feature/ddt' into develop
  remotes/origin/master  b0ebdc6 Merge pull request #2 from tanium/develop
```

Checkout the develop branch from origin:

```
git checkout -b develop origin/develop
```

output:
```
Branch develop set up to track remote branch develop from origin.
Switched to a new branch 'develop'
```

Re-list all the branches:

```
git branch -vva
```

output:
```
* develop                1cf838b [origin/develop] Merge branch 'feature/ddt' into develop
  master                 b0ebdc6 [origin/master] Merge pull request #2 from tanium/develop
  remotes/origin/HEAD    -> origin/master
  remotes/origin/develop 1cf838b Merge branch 'feature/ddt' into develop
  remotes/origin/master  b0ebdc6 Merge pull request #2 from tanium/develop
```

## Add new feature

N.B. Git flow branches features off of develop by default. Master is only touched for releases.

Start a feature branch using git flow:
```
cd ~/gh/pytan
git flow feature start add_support_for_widget
```

Publish the feature branch to origin (so other people can see it):
```
git flow feature publish add_support_for_widget
```

All of your commits should go into the branch that gets created by git flow called feature/add_support_for_widget

Once you are done with your set of commits for this feature, finish the feature branch using git flow:
```
cd ~/gh/pytan
git flow feature finish add_support_for_widget
```

## See the commit log history

Switch to master branch and view the log
```
cd ~/gh/pytan
git checkout master
git log --oneline --graph
```

output:
```
Casus-Belli:pytan jolsen$ git log --oneline --graph
*   b0ebdc6 Merge pull request #2 from tanium/develop
|\
| *   49cd62a Merge branch 'release/0.5.0' into develop
| |\
* | \   ffefdb3 Merge branch 'release/0.5.0'
|\ \ \
| | |/
| |/|
| * | fde933b version bump to 0.5.0
| |/
| *   9211796 Merge branch 'subbranch1' into develop
| |\
| | * d0bf8b5 subbranch1
| |/
| * d4ab5fa m1
| *   ef23193 Merge pull request #1 from tanium/test-feature
| |\
|/ /
| * 7d53fe7 Update README.md
|/
* 688c1f5 Update TODO
* ec92f93 Update README.md
* 75bcc33 generalize username/password in test/example cases
* 35b65f5 update README
```

Switch to develop branch and view the log
```
cd ~/gh/pytan
git checkout master
git log --oneline --graph
```

output:
```
*   1cf838b Merge branch 'feature/ddt' into develop
|\
| * 342e28e Finishing up unittest refactoring
| * 1bfdc2a More data driven tests
| * bc28f76 More data driven tests
| * ff5d1d8 Converting unit tests to use DDT
|/
*   49cd62a Merge branch 'release/0.5.0' into develop
|\
| * fde933b version bump to 0.5.0
|/
*   9211796 Merge branch 'subbranch1' into develop
|\
| * d0bf8b5 subbranch1
|/
* d4ab5fa m1
*   ef23193 Merge pull request #1 from tanium/test-feature
|\
| * 7d53fe7 Update README.md
|/
* 688c1f5 Update TODO
* ec92f93 Update README.md
* 75bcc33 generalize username/password in test/example cases
* 35b65f5 update README
```
