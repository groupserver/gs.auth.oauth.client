# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.auth.oauth.client',
    version=version,
    description="outh2 client registration methods",
    long_description=open("README.rst").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.rst")).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='outh2, client, registration',
    author='Richard Waid',
    author_email='richard@onlinegroups.net',
    url='http://groupserver.org',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.auth', 'gs.auth.oauth'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # --=mpj17=-- No, really, that is it.
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
