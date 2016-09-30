#!/usr/bin/env python

# pre-commit git hook that runs python and R linters, validates JSON files,
# removes trailing whitespace from lines, and checks for encryption
# secrets, aws keys, and large files which shouldn't be added to git.
# Currently it does not prevent the commit from occuring, it simply warns
# of possible issues.

from __future__ import print_function

import json
import os
import subprocess as sp

red = '\033[1;31;40m'
white = '\033[0m]'


def run_cmd(*args):
    try:
        output = sp.check_output(args)
    except sp.CalledProcessError as e:
        output = e.output
    return output


def git_lint(filenames):
    """Runs git lint against all files in the diff"""
    print(run_cmd("git", "lint"))


def lint_python(filenames, ignores=("E501",)):
    """Runs flake8 against all .py files in the diff"""
    python_files = [name for name in filenames if name.endswith(b'.py')]

    if python_files:
        output = run_cmd("flake8", "--ignore", ",".join(ignores), "--exit-zero", *python_files)
        print(red + output + white, end="")


def lint_r(filenames):
    """Runs flake8 against all .R files in the diff"""
    r_files = [name for name in filenames if name.endswith((b'.R', b'.r'))]

    for filename in r_files:
        output = run_cmd("R", "--slave", "--no-save", "--no-restore", "-e", "lintr::lint('{}')".format(filename))
        print(red + output + white, end="")


def validate_json(filenames):
    """Validates JSON via the Python JSON parser"""
    json_files = [name for name in filenames if name.endswith(b'.json')]
    for filename in json_files:
        with open(filename) as f:
            try:
                json.load(f)
            except ValueError:
                print(red + "Warning: {} is not a valid JSON file.".format(filename) + white)


def remove_trailing_whitespace(filenames):
    """Remove whitespace from lines of code in a file by modifying the file in place"""
    if sp.call(["sed", "-i", ".bak", "s/[[:blank:]]\+$//"] + filenames) == 0:
        for filename in filenames:
            os.remove(filename + ".bak")


def aws_keys(filenames):
    """Examine a list of files for possible AWS keys & secrets"""
    for filename in filenames:
        output = run_cmd("grep", "-nE", "[^A-Z0-9][A-Z0-9]{20}[^A-Z0-9]", filename)
        aws_key = output.strip()

        output = run_cmd("grep", "-nE", "[^A-Za-z0-9/+=][A-Za-z0-9/+=]{40}[^A-Za-z0-9/+=]", filename)
        aws_secret = output.strip()

        if aws_key:
            print(red + "Warning: possible AWS Key committed to {}".format(filename))
            print(aws_key + white)
        if aws_secret:
            print(red + "Warning: possible AWS Secret committed to {}".format(filename))
            print(aws_secret + white)


def secrets(filenames):
    """Examine a list of files for encryption keys"""
    BLACKLIST = (
        "'BEGIN RSA PRIVATE KEY'",
        "'BEGIN DSA PRIVATE KEY'",
        "'BEGIN EC PRIVATE KEY'",
    )
    for filename in filenames:
        for keystring in BLACKLIST:
            output = run_cmd("grep", "-n", keystring, filename)
            key_file = output.strip()
            if key_file:
                print(red + "Warning: possible private key file found: {}".format(filename))
                print(key_file + white)


def large_files(filenames):
    """Check if any files in a list exceed 515 KB in size"""
    for filename in filenames:
        if os.stat(filename).st_size > 512 * 1024:  # 512 KB
            print(red + "Warning: {} filesize exceeds 512 KB.".format(filename) + white)


def main():
    against = "HEAD"
    if sp.call(["git", "rev-parse", "--verify", "HEAD"]) == 1:
        # Initial commit: diff against an empty tree object
        against = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    output = run_cmd("git", "diff-index", "--name-only", "--diff-filter=AM", against)
    commit_files = output.strip().splitlines()

    checks = (
        git_lint,
        lint_python,
        # lint_r,
        validate_json,
        aws_keys,
        secrets,
        large_files,
        # 'remove_trailing_whitespace' is commented out because it modifies
        # files in place and could be potentially damaging to the code.  Not
        # sure if we should enable it or not.
        # remove_trailing_whitespace,
    )

    for check in checks:
        check(commit_files)


if __name__ == '__main__':
    main()
