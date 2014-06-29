======
1to001
======

*1to001* is made for padding numbers in filenames automatically. It's written in Python 3.


Installation
============

System-wide installation:

.. code:: sh

  $ pip install 1to001

User installation:

.. code:: sh

  $ pip install --user 1to001

For development code:

.. code:: sh

  $ pip install git+https://github.com/livibetter/1to100.git


Example
=======

.. code:: sh

  $ touch 1.txt 100.txt
  $ 1to001 *.txt
  + 001.txt
  ? ++
  perform padding (y/n)? y
  1.txt -> 001.txt


Options
=======

``-i`` (``--ignore-case``)
  When cases are mixed, this option would ignore the cases, for example for files like::

    read100me1.TXT
    read5Me02.txt

  They can be renamed to::

    1to001 -i *.{txt,TXT}
    + read005Me02.txt
    ?     ++
    + read100me01.TXT
    ?          +
    perform padding (y/n)?


More information
================

* 1to001_ on GitHub
* PyPI_
* Some usage examples in this `blog post`_

.. _1to001: https://github.com/livibetter/1to001
.. _PyPI: https://pypi.python.org/pypi/1to001
.. _blog post: http://blog.yjl.im/2013/07/padding-numbers-in-filenames.html


License
=======

This project is licensed under the MIT License::

  Copyright (c) 2013, 2014 Yu-Jie Lin
