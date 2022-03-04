#!/usr/bin/python

import pytest

import os

# add content roots to python path for tets
os.environ['PYTHONPATH'] = os.path.dirname(os.path.realpath(__file__))

pytest.main()
