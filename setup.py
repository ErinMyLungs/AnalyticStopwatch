import ast
import io
import os
import re

from setuptools import find_packages, setup

DEPENDENCIES = ["dataset", "dearpygui", "pandas"]
EXCLUDE_FROM_PACKAGES = ["tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version():
    main_file = os.path.join(CURDIR, "clockpuncher", "main.py")
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="pycowsay",
    version="0.1.0",
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
    classifiers=[
        "Programming Language :: Python",
        # "Programming Language :: Python :: 3",
        # "Operating System :: OS Independent",
        # "Private :: Do Not Upload"
    ],
)
