import textwrap

from reStUtil import *

doc = ReStDocument('README.rst',title='reStUtil python package') # accepts file pointer or filename string

intro_sec = ReStSection('Introduction')
doc.add(intro_sec) # add a top level section

intro = """reStructuredText_ is a simple markup syntax for producing human-readable
and easily machine-parsable documents. This python package provides
a simple API to produce reStructuredText-formatted documents.  It is useful
to, for example, generate human readable reports from within scripts, rather
than generating intermediate data files that are then later transformed.
reStructuredText directives are represented as python objects that can be
arbitrarily nested for structural and/or organizational purposes.  It is far
from complete, but has many useful directives, including sections, tables,
figures, and hyperlinks.
"""

intro_sec.add(intro)

intro_sec.add("`API Documentation`_")

intro_sec.add(ReStHyperlink('reStructuredText',url='http://docutils.sourceforge.net/rst.html'))
intro_sec.add(ReStHyperlink('API Documentation',url='http://adamlabadorf.github.com/reStUtil/'))

doc.add(ReStSection('Examples'))

examples = """There is a growing number of real examples in the *examples/*
directory under this repository.  Look there for uses of the various directive
classes"""

doc.add(examples)

doc.write()
