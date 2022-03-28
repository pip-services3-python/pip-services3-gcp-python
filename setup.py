"""
Pip.Services GCP
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_gcp provides synchronous and asynchronous communication components.

Links
`````

* `website <http://github.com/pip-services-python/>`_
* `development version <http://github.com/pip-services3-python/pip-services3-gcp-python>`

"""

from setuptools import setup
from setuptools import find_packages

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_gcp',
    version='3.0.0',
    url='http://github.com/pip-services3-python/pip-services3-gcp-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='judas.priest999@gmail.com',
    description='Communication components for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'Flask >= 2.0.3, < 3.0',

        'pip_services3_commons >=3.3.12, <4.0',
        'pip_services3_components >=3.5.9, <4.0',
        'pip_services3_container >=3.2.5, <4.0',
        'pip_services3_rpc >=3.3.2, <4.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
