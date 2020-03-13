from setuptools import setup, find_packages
from findpi.__version__ import __version__


setup(
    name="findpi",
    author="James Campbell",
    author_email="james@jamescampbell.us",
    version=__version__,
    license="MIT",
    description="Find pi's on the network faster than nmap!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["findpi"],
    py_modules=["findpi"],
    keywords=["raspberry", "pi", "network-analysis", "sbc", "nmap"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["pprint", ],
    entry_points={"console_scripts": ["findpi = findpi.findpi:main"]},
    url="https://github.com/jamesacampbell/findpi",
    download_url="https://github.com/jamesacampbell/findpi/archive/{}.tar.gz".format(
        __version__
    ),
)
