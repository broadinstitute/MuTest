from setuptools import setup

setup(
    name='MuTest',

    version='0.1',

    author = "Kareem Carr ",

    author_email= "kcarr@broadinstitute.org",

    url = "https://github.com/broadinstitute/MuTest",

    entry_points={
        'console_scripts': [
        'mutest  = MuTest.cli:main',
        'parse_mara = MuTest.PreprocessingParsers.parse_mara:main',
        'parse_hcc  = MuTest.PreprocessingParsers.parse_hcc:main',
        'clean_database = MuTest.Scripts.clean_database:main'
        ]
    },

    packages=['MuTest',
              'MuTest.Actions',
              'MuTest.BasicUtilities',
              'MuTest.Scripts',
              'MuTest.SupportLibraries',
              'MuTest.PreprocessingParsers'],

    license='TODO: Determine license',

    long_description='A package for communicating with the DSDE somatic mutation mongo database.',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Scientific/Engineering',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics ',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
)
