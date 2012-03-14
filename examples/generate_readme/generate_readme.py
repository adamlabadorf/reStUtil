import textwrap

from reStUtil import *

doc = ReStDocument('README',title='reStUtil python package') # accepts file pointer or filename string

doc.add(ReStSection('Introduction')) # add a top level section

intro = """reStructuredText_ is a simple markup syntax for producing human-readable
and easily machine-parsable documents. This python package provides
a simple API to produce reStructuredText-formatted documents.  It is useful
to, for example, generate human readable reports from within scripts, rather
than generating intermediate data files that are then later transformed.
reStructuredText directives are represented as python objects that can be
arbitrarily nested for structural and/or organizational purposes.  It is far
from complete, but has many useful directives, including sections, tables,
figures, and hyperlinks.

API documentation `here<api>`_.
"""

doc.add(textwrap.fill(intro))

doc.add(ReStHyperlink('reStructuredText',url='http://docutils.sourceforge.net/rst.html'))
doc.add(ReStHyperlink('api',url='http://adamlabadorf.github.com/reStUtil/'))

doc.add(ReStSection('Examples'))

examples = """There is a growing number of real examples in the *examples/*
directory under this repository.  Look there for uses of the various directive
classes"""

doc.add(textwrap.fill(examples))

doc.write()
