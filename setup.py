from setuptools import setup, find_packages

long_description = open('README.rst').read()

packages = find_packages(exclude=['tests", "tests.*'])

setup(
    name='pyflare',
    version='1.0.0b',
    packages=packages,
    url='https://github.com/jlinn/pyflare',
    license='LICENSE.txt',
    author='Joe Linn',
    author_email='',
    description="An adapter for CloudFlare's client API",
    long_description=long_description,
    install_requires=['requests'],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
