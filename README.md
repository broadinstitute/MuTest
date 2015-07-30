# Mutest

========
Overview
========

Mutest is a python package for testing Mutect. It provides commands for interacting with a mongo database that stores somatic variants. Most importantly, it enables a centralized way of benchmarking the perfomance of Mutect.

The curated database contains projects. Projects are collections of datasets and datasets are collections of samples. Each sample is a collection of mutation calls.  Projects are meant to be datasets that have all been processed in a similar way to produce truth sets. Within projects, there can be different datasets which ideally have some biological reason for being grouped together. For instance, datasets might include all LUAD or GBM samples.


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


Installing Mutest
=================

Installation of the Mutest is very simple, just run the _installation script_::

./install.sh

The script also functions as a reinstallation script. If any modifications or updates to
the Mutest occur, simply run the installation script to install the latest version.

After installation, the command _somaticdb_ will now be available. To get help, you can
type::

mutest -h


Using Mutest
============

Assessing Mutect
----------------


The most common workflow will probably be assessing mutect on a list of datasets. In order, to do that one needs to specify a _query_. The queryis written using the mongo query syntax.  For instance, to query the tcga project and the luad dataset use::

{'project':'tcga','dataset':'luad'}

The

mutest bam_aggregate -q <query> -n <normal_bam_list> -t <tumor_bam_list>
                     -i <interval_list> -f <folder> -m <metadata_list>



Interacting with the database
-----------------------------

It's important to be careful about these commands as they have the potential to affect other users negatively.

