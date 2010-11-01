from reStUtil import *

doc = ReStDocument('README') # accepts file pointer or filename string

doc.add(ReStSection('Introduction')) # add a top level section

doc.add("""reStructuredText_ is a simple markup syntax for producing human-readable and
easily machine-parsable documents. This python package provides a simple
programmatic API to produce reStructuredText-formatted documents.  It is useful
to, for example, generate human readable reports from within scripts, rather
than generating intermediate data files that are then later transformed.
reStructuredText directives are represented as python objects that can be
arbitrarily nested for structural and/or organizational purposes.  It is far
from complete, but has many useful directives, including sections, tables,
figures, and hyperlinks.""")

doc.add(ReStHyperlink('reStructuredText',url='http://docutils.sourceforge.net/rst.html'))

doc.add(ReStSection('Examples'))

doc.add("""There is a growing number of real examples in the *examples/*
directory under this repository.  Look there for uses of the various directive
classes""")

doc.write()