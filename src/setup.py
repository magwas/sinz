#!/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import sys, os

srcdir = os.path.dirname(sys.path[0])

setup(
  name="sinz",
  description="Sinz Is Not ZWA",
  author="Árpád Magosányi",
  author_email="mag@balabit.hu",
  packages=["sinz", "sinz.cli", "sinz.plugins", "sinz.plugins.identity"]
  )
