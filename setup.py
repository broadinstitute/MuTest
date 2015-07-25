from setuptools import setup

setup(
    name='MuTest',

    version='alpha',

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

    long_description='A somatic database in mongo.',

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
