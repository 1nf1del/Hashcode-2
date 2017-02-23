.. -*- mode: rst -*-

.. |Travis| image:: https://travis-ci.com/RomainBrault/Hashcode.svg?token=BGkmfYrnrsiGdq17pxis&branch=master
.. _Travis: https://travis-ci.com/RomainBrault/Hashcode

.. |Python35| image:: https://img.shields.io/badge/python-3.5-blue.svg
.. _Python35: https://github.com/RomainBrault/Hashcode

Hashcode
========

Hashcode qualification 2017 |Travis|_ |Python35|_

Environment
===========

Create conda environement::

    conda create -n hashcode python=3 anaconda numpy scipy ipython scikit-learn

Activate environment::

    source activate hashcode

Install
=======

Install hashcode::

    python setup.py develop

Usage
=====

Run program::

    python samples/main.py

Or::

    chmod +x run
    ./run
