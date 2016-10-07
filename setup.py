import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTestModels(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests/model']

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

class PyTestAll(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests/']

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name='pygooglesheets',
      version='0.1',
      description='Write data to a googlesheet',
      url='http://github.com/unbounce/ub-pyGooglesheets',
      author='Yosem Sweet',
      author_email='yosem.sweet@unbounce.com',
      license='MIT',
      packages=['pygooglesheets'],
      install_requires=[
          'google-api-python-client',
          'httplib2',
          'oauth2client'
      ],
      cmdclass = { 'test': PyTestModels, 'testall': PyTestAll },
      tests_require=['pytest', 'pytest-mock'],
      zip_safe=False)
