======
MuTest
======

INTRODUCTION
============

Mutest is a python package for testing Mutect. It enables a centralized way of benchmarking the perfomance of Mutect (both M1 and M2).

One of the most important components of MuTest is a curated database. The database contains projects. Projects are collections of datasets; and datasets are collections of samples. Each sample is  collection of mutation calls stored in a single maf or vcf file.  Projects are meant to be collections of datasets that have all been processed in a similar way to produce truth sets.  . Within projects, there can be different datasets which ideally have some biological reason for being grouped together. For instance, a dataset might include all LUAD samples.

If you are new to MuTest and wish to get started immediately with using it for assessment, please look at the sections on the prerequisites and installation, and then proceed to the section on automated assessment.

The raw data for the database is stored at /dsde/working/somaticDB/master.  As of the writing of this guide, the ip address of the mongo server that stores the results of MuTest is

PREREQUISITES
=============

The MuTest package requires python 2.7.x to be installed and can be run locally on a labtop.
The following document is recommend for Broad users::

    use .python-2.7.6-sqlite3-rtrees-vanilla

In order to connect to the database, the system on which MuTest is run must access to _Broad internal_, as this is where the ip for the database is accessible and jobs must be submitted from a host that can submit SGE jobs.

Please install the python packages *numpy* , *pyvcf* , *pandas* and *pymongo* locally using::

    pip install numpy --user
    pip install pandas --user
    pip install pymongo --user
    pip install pyvcf --user

INSTALLATION
============

Installation of the Mutest is very simple, just run the _installation script_::

    ./install.sh

The script also functions as a reinstallation script. If any modifications or updates to Mutest occur, simply run the installation script to install the latest version.  There is a version of install which installs MuTest to the local version of python, install_local.sh. This can be used if it's not possible to access the system python installation.

After installation, the command _mutest_ will now be available. To get help, you can type::

    mutest -h

RUNNING MUTEST
==============

SUBMITTING FILES TO THE DATABASE
--------------------------------

All users of MuTest can submit files to MuTect database for their own use and the benefit of other users. There are two types of submissions, normal-normal submissions, lists of normal bams which represent a sample that has been resequenced multiple times. These are useful for computing specificity. The command for doing this is as follows::

mutest normal_normal_uploader -t <tsv>

The second type of submission are curated files containing true positive datasets composed of mafs or vcfs. The command is::

mutest variant_upload -t <tsv>

The format for submission is a tsv with the following fields: tumor_bam, normal_bam, data_filename, project, dataset, sample, evidence_type and author.


USING THE DATABASE FOR ASSESSMENT
---------------------------------

AUTOMATED ASSESSMENT
~~~~~~~~~~~~~~~~~~~~

The most common workflow is assessing mutect on a list of datasets. In order, to do that one needs to specify a _query_. The query is written using the mongo query syntax.  For instance, to assess MuTect on the tcga project and the luad dataset one needs the following query::

    "{'project':'tcga','dataset':'luad'}"

There are two assessments that can be performed. One can measure performance on known true positive results using the following command::

    java -jar <Queue jar> -qsub -jobQueue gsa -S <scala script> -project_name <project> -query <query> -evaluation_rules <evaluation rules> -sc <scatter number> -pd <padding> -run

If one wants to measure specificity, this command is used:

java -jar <Queue jar> -qsub -jobQueue gsa -S <scala script> -project_name <project> -query <evaluation rules> -sc <scatter number> -pd <padding> -run

One also needs to provide the evaluation rules. This is a feature that will be removed, but is currently required.  For each project list the type of evaluation needed. It should either be CM for confusion matrix or NN for normal-normal called.  The evaluation rule is specified in this way "tcga:CM, hcc:NN".



ASSESSMENT BY HAND
~~~~~~~~~~~~~~~~~~

The scala script provides an automated way of doing the following: gathering bams lists, running mutest on those bam lists, incorporating the results into a submission file and assessing that submission file with MuTest.

The first command does the collection step::

    mutest bam_aggregate -q <query> -n <normal_bam_list> -t <tumor_bam_list> -i <interval_list> -f <folder> -m <metadata_list>

Assuming that a list of result files has been created and is called results.list. The format of this list is just a series of output files (without a column name) in the corresponding order to the bam lists which contains the output files::

    mutest assessment_file_create -t <metadata_list> -r <results list> -o <submssion file> -e <evaluation_rules>

The results of the prior command should be a submission file which contains all the information the database needs to perform an assessment::

    mutest variant_assess -t <submssion file> -q <query> -o <assessment file>

In the case of normal-normal calling, all the commands are the same except for the bam collection step. There one uses the command::

    mutest normal_normal_collector -q <query> -n <normal_bam_list> -t <tumor_bam_list> -i <interval_list> -f <folder> -m <metadata_list>

DATABASE MAINTENANCE
~~~~~~~~~~~~~~~~~~~~

It's important to be careful about these commands as they have the potential to affect other users negatively.  You can delete everything in the database using the following command::

    mutest database_delete

You can add things to the database using the _variant_upload_ command discussed above. There is a directory containing submission files for everything in the database. It can be found here::

    /dsde/working/somaticDB/master/records


UTILITIES
~~~~~~~~~

A few utilities make it easier to interact with the contents of the database. For instance, it is possible to look at the variants associated with a particular query::

	mutest variant_extract -t

Further, one can get a list of all projects currently in the database and the counts of indels and SNVs stored in the database using the following command::

	mutest survey -o <survey output file>

