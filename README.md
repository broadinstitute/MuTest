# SomaticDB

========
Overview
========

The SomaticDB is a python package for interacting with a mongo database that stores
somatic variants. It provides a centralized way of benchmarking the perfomance of
algorithms which either generate or refine somatic variant calls.


Requirements
============

Software
--------

The package requires python 2.7.x to be installed and can be run locally on a labtop.
On the Broad cluster, use the following dotkit::

    use .python-2.7.6-sqlite3-rtrees-vanilla

Other
-----

The computer on which this code is run must have access to _Broad internal_, as this
is where the ip for the database is accessible.


Using SomaticDB
===============

Installation of the SomaticDB is very simple, just run the _installation script_::

./install.sh

The script also functions as a reinstallation script. If any modifications or updates to
the somaticDB occur, simply run the installation script to install the latest version.

After installation, the command _somaticdb_ will now be available. To get help, you can
type::

somaticdb -h
