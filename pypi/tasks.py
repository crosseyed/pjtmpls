# prj:render
import os
import configparser
import subprocess
import platform
import webbrowser

from dotenv import load_dotenv
from invoke import task
from os import getenv
from os.path import abspath, dirname, getctime, join
from pathlib import Path
from glob import glob
from sys import version_info


#
# Vars
#
root = dirname(__file__)


project_dotenv = join(root, '.env')
load_dotenv(project_dotenv)

home_dotenv = join(getenv('HOME'), '.env')
if os.path.exists(home_dotenv):
    load_dotenv(home_dotenv)

config = configparser.ConfigParser()
config.read(join(dirname(__file__), 'setup.cfg'))

PYPI_REPO = os.getenv('PYPI_REPO')

#
# Required tasks - All builds must always have these tasks. Or tasks with these names that do the same work.
#
@task
def clean(c):
    """
    Return project to original state
    """
    c.run("python setup.py clean")
    safe_rm_rf(c, ".eggs")
    safe_rm_rf(c, "build")
    safe_rm_rf(c, "dist")
    safe_rm_rf(c, "reports")
    safe_rm_rf(c, "htmlcov")
    safe_rm_rf(c, "*.egg-info")
    safe_rm_rf(c, slash("{{.Project.NAME}}/*.pyc"))


@task(aliases=['pip'])
def deps(c):
    """
    Lock packages to a version using pip compile
    """
    if getctime("requirements-setup.in") > getctime("requirements-setup.txt"):
        c.run("pip-compile --output-file=requirements-setup.txt requirements-setup.in")
    if getctime("requirements.in") > getctime("requirements.txt"):
        c.run("pip-compile --output-file=requirements.txt requirements.in")
    c.run("pip install --quiet --requirement requirements-setup.txt")
    c.run("pip install --quiet --requirement requirements.txt")


@task(post=[deps])
def deps_compile(c):
    """
    Update dependency requirements if any
    """

    def touch(fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    touch("requirements-setup.in")
    touch("requirements.in")


@task(pre=[deps])
def build(c):
    """
    Build package
    """
    # Create python distribution
    c.run("python setup.py sdist")
    c.run("python setup.py bdist_wheel")
    c.run( slash( "mkdir -p build/{version}".format(**_vars()) ) )
    c.run("mkdir -p dist")


@task()
def install(c):
    """
    Install Package(s)
    """
    c.run(slash("pip install -q dist/{project}-{version}*.whl").format(**_vars()))


@task(aliases=['upload'])
def deploy(c, rel=False):
    """
    Upload package to a PyPi server
    """
    if PYPI_REPO:
        c.run(
            "python setup.py sdist bdist_wheel upload -r {PYPI_REPO}".format(**_vars(rel)))


@task
def test(c):
    """
    Testing
    """
    print(getenv("BROWSE_REPORT"))
    print(home_dotenv)
    radon_txt = slash("reports/radon.txt")
    complexity_html = slash("reports/complexity.html")
    c.run(slash("pytest -c {root}/.pytest.ini".format(root=root)))
    c.run("radon cc --total-average -s -o SCORE src -O {radon}; cat {radon}".format(radon=radon_txt))
    c.run("ansi2html -t 'Cyclomatic Complexity' < {radon} > {complexity}".format(radon=radon_txt, complexity=complexity_html))
    if getenv("BROWSE_REPORT") == "true":
        c.run("inv reports")


@task
def reports(c):
    """
    Open reports
    """
    cov = abspath(slash("reports/htmlcov/index.html"))
    complexity = abspath(slash("reports/complexity.html"))
    unit = abspath(slash("reports/unit/index.html"))
    new = 1
    for report in [cov, complexity, unit]:
        webbrowser.open("file://" + report, new=new)
        if new > 0:
            new = 0


@task
def version(c):
    """
    Get current version
    """
    config["metadata'"]

#
# Utilities
#


def git_branch():
    """
    Git return current branch
    """
    try:
        cur_branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        return cur_branch.rstrip('\n')
    except subprocess.CalledProcessError:
        return None


def git_has_version(tag):
    """
    :param tag: Tag string
    :rtype: bool
    """
    subprocess.call(['git', 'pull', '--tags'])

    try:
        # Check tag
        subprocess.check_output(['git', 'rev-parse', tag])
        return True
    except subprocess.CalledProcessError:
        return False


def safe_rm_rf(c, pattern):
    """
    Safely delete files
    """
    projdir = abspath(dirname(__file__))
    for f in glob(pattern):
        fullpath = abspath(f)
        if not fullpath.startswith(projdir):
            msg = "File {} is not a project file".format(fullpath)
            raise Exception(msg)

        c.run("rm -rf {}".format(fullpath))

def slash(text: str) -> str:
    """
    Replace slashes to backslashes on windows
    """
    return str(Path(text))

def _vars(rel=False):
    fmt_vars = {
        'PYPI_REPO': PYPI_REPO,
        'project': config["metadata"]["name"],
        'version': config["metadata"]["version"],
        'root': root,
    }
    return fmt_vars
