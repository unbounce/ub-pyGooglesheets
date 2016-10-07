
# Check for existence of R interpreter
R := $(shell command -v R 2> /dev/null)
ifdef R
setup: rlang
endif

# Hook installation
setup: python yaml
	ln -sf ../../githooks/pre-commit.py .git/hooks/pre-commit
	ln -sf ../../githooks/commit-msg.sh .git/hooks/commit-msg
	pip install --upgrade git-lint
	echo "workon ." > .env

# Python lint setup
python:
	pip install --upgrade flake8

# R lint setup
rlang:
	mkdir -p ~/R/libs
	echo 'R_LIBS_USER=~/R/libs' >> ~/.Renviron
	R --slave --no-save --no-restore -e 'install.packages(c("lintr"), lib="~/R/libs", repos="http://cran.us.r-project.org")'

yaml:
	pip install --upgrade yamllint
