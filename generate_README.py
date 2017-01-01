#!/usr/bin/env python

import os
from textwrap import dedent
import subprocess

"""
This script can be launched to generate the README.md file. This script is a useful way of ensuring that your README
document is up to date and the relevant examples still work as intended.

```
$ ./generate_README.py -o
or
$ ./generate_README.py > README.md
```
"""

# the file that will be written
PROJECT_DIRECTORY = os.path.dirname(__file__)


class Generator(object):
    def __init__(self):
        self.lines = []

    def heading(self, text, level):
        self.lines.append('#' * level + " " + text)
        self.lines.append("")

    def h1(self, text):
        return self.heading(text, 1)

    def h2(self, text):
        return self.heading(text, 2)

    def h3(self, text):
        return self.heading(text, 3)

    def h4(self, text):
        return self.heading(text, 4)

    def paragraph(self, text):
        text = text.rstrip()
        self.lines.append(dedent(text))
        self.lines.append("")

    def command_example(self, command):
        self.lines.append("```")
        self.lines.append("$ {}".format(command))

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, cwd=PROJECT_DIRECTORY)
        except subprocess.CalledProcessError as e:
            output = e.output

        self.lines.append(output.strip())
        self.lines.append("```")
        self.lines.append("")

    def __str__(self):
        text = "\n".join(self.lines)
        if not text.endswith("\n"):
            text += "\n"
        return text


def main():
    g = Generator()
    g.h1("`go-cli-template` - an example Go CLI application")
    g.paragraph("""\
    This is an example repository that can be cloned and adapted for a new application. It contains useful scripts and
    automation that I have found useful while building simple CLI-based applications.
    """)

    g.h3("Example usage:")
    g.command_example("./go-cli-template -version")
    g.command_example("./go-cli-template -help")

    g.h3("Steps for setting up a new project from this template")
    g.paragraph("""\
    1. Clone the repository

    ```
    $ git clone https://github.com/AstromechZA/go-cli-template.git
    ```

    2. Rename all references to `go-cli-template` and the project url

    There is a provided script `rename_everything.py` that will run through the relevant files and rename the 
    references to the project name and import path. You will still need to rename the directory structure yourself.

    ```
    $ ./rename_everything.py github.com/myuser/myrepo
    ```

    The script will also delete itself after being run.

    3. Tweak the git repo

    You can either delete the `.git` directory and re-run `git init` or you can
    just change the push/pull remotes and continue from there.
    """)

    g.h3("Using the `vendor` folder and govendor")
    g.paragraph("""\
    The `vendor.json` file in the vendor folder holds a anchored list of the project dependencies. This file and the
    vendor folder are managed by the `govendor` tool. 

    Install it using:

    ```
    $ go get -u github.com/kardianos/govendor
    ```

    And pull all the dependencies using:

    ```
    $ govendor sync
    ```

    (You might need to add $GOPATH/bin to your $PATH in order to run it)

    New dependencies can be added using `govendor fetch ...`.
    """)

    g.h3("Building your project")
    g.command_example("go build -v github.com/AstromechZA/go-cli-template")

    g.h3("Official Builds")
    g.paragraph("""\
    The provided `make_official.sh` script will build official builds for both Linux and OSX with an official version
    number baked in. It also compresses a `tgz` archive containing the built binaries for upload to Github or
    whatever release mechanism is being used.
    """)
    g.command_example("./make_official.sh")

    g.h3("Official Releases")
    g.paragraph("""\
    When releasing a new version to github or something do the following:

    1. change the version number in `make_official.sh`
    2. run `make_official.sh` and ensure it succeeds
    3. run `generate_README.md > README.md` to reflect the new version number
    4. commit the changed readme and version number in git
    5. tag the commit with the same version number
    6. push everything to origin and upload the `tgz` file
    """)

    print str(g)


if __name__ == '__main__':
    main()
