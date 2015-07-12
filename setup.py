from setuptools import setup

setup(
    name='somaticDB',

    version='alpha',

    entry_points={
        'console_scripts': [
        'somaticDB = SomaticDB.cli:main',
        ]
    },

    packages=['SomaticDB','SomaticDB.Actions', 'SomaticDB.BasicUtilities', 'SomaticDB.SupportLibraries'],

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
