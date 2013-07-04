#!/usr/bin/env python3
# Copyright (C) 2013 by Yu-Jie Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import imp
import unittest

m = imp.load_source('1to001', '1to001.py')


class TestFile(unittest.TestCase):

  def test_no_renames(self):

    fns = [
      '1.txt',
      '2.txt',
    ]
    expect = []

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  def test_simple(self):

    fns = [
      '1.txt',
      '10.txt',
    ]
    expect = [
      ('1.txt', '01.txt'),
    ]

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  def test_leading_text(self):

    fns = [
      'a1.txt',
      'a10.txt',
    ]
    expect = [
      ('a1.txt', 'a01.txt'),
    ]

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  def test_tailing_text(self):

    fns = [
      '1b.txt',
      '10b.txt',
    ]
    expect = [
      ('1b.txt', '01b.txt'),
    ]

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  def test_surrounding_texts(self):

    fns = [
      'a1b.txt',
      'a10b.txt',
    ]
    expect = [
      ('a1b.txt', 'a01b.txt'),
    ]

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  def test_more_texts(self):

    fns = [
      'something a1b.txt',
      'something a10b.txt',
    ]
    expect = [
      ('something a1b.txt', 'something a01b.txt'),
    ]

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  def test_2_number_fields(self):

    fns = [
      'a1b 33.txt',
      'a10b 3.txt',
    ]
    expect = [
      ('a1b 33.txt', 'a01b 33.txt'),
      ('a10b 3.txt', 'a10b 03.txt'),
    ]

    cfns = m.get_cfns(fns)
    self.assertEqual(cfns, expect)

  ##############
  # Exceptions #
  ##############

  def test_different_fields_error(self):

    fns = [
      '1.txt',
      '1 0.txt',
    ]

    with self.assertRaises(m.Error) as e:
      cfns = m.get_cfns(fns)

    self.assertEqual(e.exception.args[0], 3)

  def test_content_differ_error(self):

    fns = [
      '1 a.txt',
      '1 b.txt',
    ]

    with self.assertRaises(m.Error) as e:
      cfns = m.get_cfns(fns)

    self.assertEqual(e.exception.args[0], 3)


if __name__ == '__main__':

  unittest.main()
