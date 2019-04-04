# -*- coding: utf-8 -*-

import codecs
from setuptools import setup

__version__ = "0.5.0"

packages = ["pylibmodbus"]


def file_content(filename):
    return codecs.open(filename, "r", "utf-8").read()


setup(
    name="pylibmodbus",
    version=__version__,
    description="Python wrapper for libmodbus",
    long_description=file_content("README.rst"),
    author="Stéphane Raimbault",
    author_email="stephane.raimbault@gmail.com",
    url="http://libmodbus.org",
    keywords="python libmodbus",
    packages=packages,
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    install_requires=["cffi>=1.12.2"],
    license=file_content("LICENSE"),
    zip_safe=False,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
)
