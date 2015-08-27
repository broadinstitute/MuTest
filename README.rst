# Mutest

======
MuTest
======

INTRODUCTION
============

[WHAT THE SOFTWARE IS. SHORT DESCRIPTION OF WHAT IS SPECIAL ABOUT THIS PARTICULAR DATABASE]
[OVERVIEW OF BASIC CONCEPTS]
[NAME SECTION YOU NEED TO GET STARTED IMMEDIATELY]

Mutest is a python package for testing Mutect. It enables a centralized way of benchmarking the perfomance of Mutect (both M1 and M2).

The curated database contains projects. Projects are collections of datasets and datasets are collections of samples. Each sample is a collection of mutation calls.  Projects are meant to be datasets that have all been processed in a similar way to produce truth sets. Within projects, there can be different datasets which ideally have some biological reason for being grouped together. For instance, datasets might include all LUAD or GBM samples.

If you are new to MuTest and wish to get started immediately with using it for assessment, please look the sections on the prerequisites and installation, and then proceed to the section on automated assessment.

PREREQUISITES
=============

[OUTLINE OF PYTHON PACKAGES NEEDED]

The package requires python 2.7.x to be installed and can be run locally on a labtop.
Broad users must use the following dotkit::

    use .python-2.7.6-sqlite3-rtrees-vanilla

The computer on which this code is run must have access to _Broad internal_, as this
is where the ip for the database is accessible and jobs must be submitted from a host that can submit SGE jobs.

Please install the python packages _numpy_ , _pyvcf_ , _pandas_ and _pymongo_ locally using::
	pip install numpy --user
	pip install pandas --user
	pip install pymongo --user
	pip install pyvcf --user

The raw data for the database is stored at _/dsde/working/somaticDB/master_.

INSTALLATION
============

Installation of the Mutest is very simple, just run the _installation script_::

./install.sh

The script also functions as a reinstallation script. If any modifications or updates to Mutest occur, simply run the installation script to install the latest version.

After installation, the command _somaticdb_ will now be available. To get help, you can
type::

mutest -h

RUNNING MUTEST
==============

SUBMITTING FILES TO THE DATABASE
--------------------------------

All users of MuTest can submit files to MuTect database for their own use and the benefit of other users. There are two types of submissions, normal-normal submissions, lists of normal bams which represent a sample that has been resequenced multiple times. These are useful for computing specificity. The command for doing this is as follows::

mutest normal_normal_uploader -t <tsv>


 The second type of submission are curated files containing true positive datasets composed of mafs or vcfs. The command is::

mutest variant_upload -t <tsv>

There format for submission is a tsv with the following fields: tumor_bam, normal_bam, data_filename, project, dataset, sample, evidence_type and author.


USING THE DATABASE FOR ASSESSMENT
---------------------------------

