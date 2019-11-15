from setuptools import setup, find_packages
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"', open("findpi/findpi.py").read(), re.M
).group(1)

setup(
    name="findpi",
    author="James Campbell",
    author_email="james@jamescampbell.us",
    version=version,
    license="GPLv3",
    description="Find pi's on the network fast!",
    packages=["findpi"],
    py_modules=["findpi"],
    keywords=["raspberry", "pi", "network-analysis", "sbc", "nmap"],
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    install_requires=["pprint", ],
    entry_points={"console_scripts": ["findpi = findpi.findpi:main"]},
    url="https://github.com/jamesacampbell/findpi",
    download_url="https://github.com/jamesacampbell/findpi/archive/{}.tar.gz".format(
        version
    ),
)
