import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

setup(
    name='somaticDB',

    version='alpha',

    entry_points={
        'console_scripts': [
        'data_parser = somaticDB.DatabaseParser:main'
        ]
    },

    test_suite='test',

    install_requires=['pyvcf'],

    tests_require=['nose'],

    packages=['SomaticDB'],

    license='TODO: Determine license',

    long_description=open('README.rst').read(),

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
