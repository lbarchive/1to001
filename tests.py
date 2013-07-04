#!/usr/bin/env python3
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
