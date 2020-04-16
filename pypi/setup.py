# prj:render
#!/usr/bin/env python

from {{.Project.NAME}} import metadata
from setuptools import setup

setup(name=metadata.__project__,
      version=metadata.__version__,
      description=metadata.__description__,
      author=metadata.__author__,
      author_email=metadata.__email__,
      url=metadata.__url__,
      scripts=["scripts/{{.Project.NAME}}"],
      packages=['{{.Project.NAME}}'],
      install_requires=open("requirements.txt").read().splitlines(),
      )
