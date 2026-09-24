import os
from setuptools import setup

MYDIR = os.path.dirname(__file__)

setup(
    name='django-starfield',
    version='2.0',
    keywords = ['django', 'forms', 'widget', 'rating'],
    description = 'A no-frills Django form widget for rating stars',
    long_description = open(os.path.join(MYDIR, "README.rst"), "r", encoding="utf-8").read(),
    url = 'https://edugit.org/nik/django-starfield',
    author='Dominik George',
    author_email='nik@naturalnet.de',
    packages=['django_starfield'],
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=['Django>=5.2'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
