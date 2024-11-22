#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-cerberus',
    version='1.0.1',
    description='Django app that locks out users after too many failed login attempts.',
    long_description=open('README.rst').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/django-cerberus',
    packages=[
        'cerberus',
        'cerberus.migrations',
    ],
    include_package_data=True,
    install_requires=('django>=3',),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha'
    ],
    license='BSD License',
    keywords = "django login auth cerberus",
)
