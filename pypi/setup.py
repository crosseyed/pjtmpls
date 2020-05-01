# prj:render
#!/usr/bin/env python

from setuptools import setup

setup(package_dir={"": "src"},
      scripts=["scripts/{{.Project.NAME}}"],
      packages=['{{.Project.NAME}}'],
      install_requires=open("requirements.txt").read().splitlines(),
      )
