#!/bin/sh

# regex to validate in commit msg
commit_regex='(^\w+[-_]\d+|merge)'
error_msg="$(tput setaf 1)Warning: Your commit message is missing either a work item issue code or 'Merge'$(tput sgr0)"

if ! grep -iqE "$commit_regex" "$1"; then
	echo "$error_msg" >&2
	exit 0 # Change this to 1 if we want to enforce this.
fi
