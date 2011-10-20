import os
from setuptools import setup

setup( name='turrentine',
    version = '0.0.1',
    description = 'A very simple CMS for Django',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url = 'https://github/af/turrentine',

    author = 'Aaron Franks',
    author_email = 'aaron.franks+turrentine@gmail.com',

    keywords = ['django', 'cms',],
    packages = ['turrentine',],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
