<figure>
  <img src="docs/pyrene.png"/>
  <figcaption>Pyrene</figcaption>
</figure>

a _Py_ thon _Re_ pository _Ne_ twork tool
=========================================

I am a tool to help your interactions with Python package repositories.

For example I can copy packages between repos.

I provide a shell-like environment as primary interface - with help and completion for commands and attributes, but I can be used as a command-line tool as well.

There are two types of repos I support:

- http repos, e.g.
    - https://pypi.python.org - the global python public package repo
    - project specific PyPI server - defined by you or your company, for deployment
- directory repos, that is
    - a directory with package files, for fast/offline development
    - `~/.pip/local` - one such directory


Installation
============

From PyPI:

```
mkvirtualenv sys-pyrene
pip install pyrene
```

Directly from GitHub:

`master` branch is always the latest release, so it is safe to install with

```shell
mkvirtualenv sys-pyrene
pip install git+https://github.com/krisztianfekete/pyrene.git
```

As an extra, in order to have `pyrene` without activating its `virtualenv` I do the following:

```shell
ln -s ~/.virtualenvs/sys-pyrene/bin/pyrene ~/bin
```

Usage
=====

My state consists of:
- set of repositories
- an active repository (initially None)

I support the following commands:

copy
----

Copy packages with the same ease like local files with `cp` (or remote with `rsync`!).

```
Pyrene: copy SOURCE DESTINATION
```

Where `SOURCE` can be either `LOCAL-FILE` or `REPO:PACKAGE-SPEC`,
`DESTINATION` can be either a `REPO:` or a `LOCAL-DIRECTORY`

list
----

Lists known repositories.

show
----

Shows repository attributes

```
Pyrene: show repo
```

directory_repo
--------------

Defines a new `directory` repository or change an existing repo's the type to `directory`.

```
Pyrene: directory_repo repo
Pyrene[repo]: list
  repo
```

http_repo
---------

Defines a new `http` repository or change an existing repo's the type to `http`.

```
Pyrene: http_repo repo
Pyrene[repo]: list
  repo
```

set
---

Sets a repository attribute.

```
Pyrene: work_on repo
Pyrene[repo]: set attribute=value
Pyrene[repo]: show
  attribute: value
```

unset
-----

Removes a repository attribute

```
Pyrene: show repo
  attribute: value
Pyrene: work_on repo
Pyrene[repo]: unset attribute
Pyrene[repo]: show
```

forget
------

Makes a known repository unknown.

```
Pyrene: forget repo
Pyrene: list
```

setup_for_pypi_python_org
-------------------------

Configures repo to point to the default package index https://pypi.python.org.

```
Pyrene: setup_for_pip_local pypi
Pyrene: show pypi
  upload_url: https://pypi.python.org/
  type: http
  download_url: https://pypi.python.org/simple/
```

setup_for_pip_local
-------------------

Configures repo to be directory based and sets directory to `~/.pip/local`.
Also makes that directory if needed.

```
Pyrene: setup_for_pip_local local
Pyrene: show local
  directory: /home/user/.pip/local
  type: directory
```

use
---

How `pip` works can be greatly influenced by the `~/.pip/pip.conf` configuration file: it defines which repo is used to download from (`index-url` or `find-links`) and how (`no-use-wheels`, etc.)

When you say `use` I'll create a minimal `pip.conf` config file (*or overwrite silently the existing one!!!*) so that `pip` will use the given repo outside of `Pyrene` for downloads: 

```
Pyrene: use repo
```


Development
===========

Fork the [repo](https://github.com/krisztianfekete/pyrene) and create a pull request against the `develop` branch.

The reason is: I am being developed using `git flow` on branch `develop`.
`master` is the release branch.

`Pyrene` is a work in progress, with lots of sharp edges, miswordings, etc.

So

contributions
-------------

- reporting issues
- improving documentation
- improving on the simplicity and clarity of the code/interface
- adding relevant tests
- providing new badly missing features (preferably with tests)
- showing alternatives of me

are welcome.

Guidelines:
-----------

- all code should be extremely simple and clear, including tests
- all features require unit tests
- zero messages from flake8
- usability, simplicity wins over feature completeness
- the smallest the change, the better

The current code might violate these, but it is then considered a bug.
Fixing any of these violations - even if it looks trivial is welcome!

External packages/tools:
------------------------

- packages are downloaded with [pip](http://www.pip-installer.org).
- packages are uploaded with code adopted from [twine](https://pypi.python.org/pypi/twine), unfortunately `twine` is not used directly.
- local packages are served with [pypi-server](https://pypi.python.org/pypi/pypiserver)
