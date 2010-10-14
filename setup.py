#!/usr/bin/env python

from distutils.core import *

setup(
        name = 'job_queue',
        py_modules = ['job_queue'],
        version = '0.1',
        description = 'A Job Queue',
        author = 'Morgan Goose',
        author_email = 'morgan.goose@gmail.com',
        url = 'http://github.com/goosemo/job_queue',
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Clustering',
        ],    
        
    )

