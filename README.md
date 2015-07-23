# SomaticDB

===========================
The Somatic DB: An Overview
===========================

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

