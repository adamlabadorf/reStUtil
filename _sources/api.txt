
reStUtil API Documentation
==========================

.. automodule:: reStUtil

.. autoclass:: ReStBase
   :members:

Container Classes
-----------------

:py:class:`ReStContainer` and its subclasses are convenience classes for grouping
sequences of :py:class:`ReStBase` derived objects.  Use as follows:

  >>> container = ReStContainer()
  >>> container.add("Some text first")
  >>> container.add(ReStImage("my_img.png"))
  >>> fruit_data = [['apple',70],
                    ['peach',77],
                    ['snozzcumber',32]]
  >>> container.add(ReStSimpleTable(['*Fruit*','*Delicious Index*'],
                                    fruit_data))
  >>> print container

produces::

      Some text first

      .. image:: my_img.png
      
      
      +-------------+-------------------+
      |   *Fruit*   | *Delicious Index* |
      +-------------+-------------------+
      | apple       | 70                |
      +-------------+-------------------+
      | peach       | 77                |
      +-------------+-------------------+
      | snozzcumber | 32                |
      +-------------+-------------------+


.. autoclass:: ReStContainer
   :members:

.. autoclass:: ReStSection
   :members:

.. autoclass:: ReStDocument
   :members:


Directive Classes
-----------------

.. autoclass:: ReStText
   :members:

.. autoclass:: ReStImage
.. autoclass:: ReStFigure
.. autoclass:: ReStSimpleTable
.. autoclass:: ReStTable
.. autoclass:: ReStHyperlink
.. autoclass:: ReStInclude

Writer-specific Classes
-----------------------

.. autoclass:: ReStHTMLStyle
