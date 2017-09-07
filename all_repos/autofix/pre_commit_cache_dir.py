import argparse
import os.path

from all_repos import autofix_lib
from all_repos import cli
from all_repos.grep import repos_matching


APPVEYOR = 'appveyor.yml'
TRAVIS = '.travis.yml'


def find_repos(config):
    return (
        repos_matching(config, ('$HOME/.pre-commit', '--', TRAVIS)) |
        repos_matching(config, (r'%USERPROFILE%\\.pre-commit', '--', APPVEYOR))
    )


def _replace_if_exists(filename, s1, s2):
    if os.path.exists(filename):
        with open(filename) as f:
            contents = f.read()
        contents = contents.replace(s1, s2)
        with open(filename, 'w') as f:
            f.write(contents)


def apply_fix():
    _replace_if_exists(TRAVIS, '$HOME/.pre-commit', '$HOME/.cache/pre-commit')
    _replace_if_exists(
        APPVEYOR,
        r'%USERPROFILE%\.pre-commit', r'%USERPROFILE%\.cache\pre-commit',
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    cli.add_fixer_args(parser)
    args = parser.parse_args(argv)

    repos, config, commit, autofix_settings = autofix_lib.from_cli(
        args,
        find_repos=find_repos,
        msg='Update pre-commit cache directory.',
        branch_name='pre-commit-cache-dir',
    )

    autofix_lib.fix(
        repos,
        apply_fix=apply_fix,
        config=config,
        commit=commit,
        autofix_settings=autofix_settings,
    )


if __name__ == '__main__':
    exit(main())
