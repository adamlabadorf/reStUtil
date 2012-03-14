
reStUtil API Documentation
==========================

.. automodule:: reStUtil

.. autoclass:: ReStBase

Container Classes
-----------------

*ReStContainer* and its subclasses are convenience classes for grouping
sequences of *ReStBase* derived objects.  Use as follows:

  >>> container = ReStContainer()
  >>> container.add("Some text first")
  >>> container.add(ReStImage("my_img.png"))
  >>> fruit_data = [['apple',70],
                    ['peach',77],
                    ['snozzcumber',32]]
  >>> container.add(ReStSimpleTable(['*Fruit*','*Delicious Index*'],
                                    fruit_data))
  >>> print container


.. autoclass:: ReStContainer
.. autoclass:: ReStSection
.. autoclass:: ReStDocument


Directive Classes
-----------------

.. autoclass:: ReStText
.. autoclass:: ReStImage
.. autoclass:: ReStFigure
.. autoclass:: ReStSimpleTable
.. autoclass:: ReStTable
.. autoclass:: ReStHyperlink
.. autoclass:: ReStInclude
