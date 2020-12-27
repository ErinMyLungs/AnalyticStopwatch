import ast
import io
import os
import re

from setuptools import find_packages, setup

DEPENDENCIES = ["dataset", "dearpygui", "pandas"]
EXCLUDE_FROM_PACKAGES = ["tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

README_PATH = os.path.join(CURDIR, "README.md")
with io.open(README_PATH, "r", encoding="utf-8") as f:
    README = f.read()


setup(
    name="clockpuncher",
    version="0.1.1",
    author="Erin Maestas",
    author_email="ErinLMaestas@gmail.com",
    description="A hackable GUI time tracker designed to be easily modified for user-centric automation.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ErinMyLungs/AnalyticStopwatch",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=[],
    scripts=[],
    entry_points={"console_scripts": ["clockpuncher=clockpuncher.main:main"]},
    zip_safe=False,
    install_requires=DEPENDENCIES,
    test_suite="tests.test_project",
    python_requires=">=3.6",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    license="License :: OSI Approved :: MIT License",
    classifiers=["Programming Language :: Python"],
)
