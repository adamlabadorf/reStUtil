
=======================
reStUtil python package
=======================

Introduction
============

reStructuredText_ is a simple markup syntax for producing human-readable and
easily machine-parsable documents. This python package provides a simple API to
produce reStructuredText-formatted documents.  It is useful to, for example,
generate human readable reports from within scripts, rather than generating
intermediate data files that are then later transformed. reStructuredText
directives are represented as python objects that can be arbitrarily nested for
structural and/or organizational purposes.  It is far from complete, but has
many useful directives, including sections, tables, figures, and hyperlinks.

`API Documentation`_

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

.. _API Documentation: http://adamlabadorf.github.com/reStUtil/

Installation
============

To install on a command line, clone this repo and run setup.py:

  $> python setup.py install
  
If you would like to install the package elsewhere, use the **--prefix** flag:

  $> python setup.py --prefix=/path/to/install/dir install

Examples
========


There is a growing number of real examples in the *examples/* directory under
this repository.  Look there for uses of the various directive classes

