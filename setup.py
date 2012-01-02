from setuptools import setup

setup( name='turrentine',
    version = '0.0.4',
    description = 'A simple CMS for Django',
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
    include_package_data=True,
)
