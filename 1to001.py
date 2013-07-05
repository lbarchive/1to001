#!/usr/bin/env python3
# Padding numbers in filenames automatically
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
#
# Blog: http://blog.yjl.im/2013/07/padding-numbers-in-filenames.html
# Gist: https://gist.github.com/livibetter/5930770
from difflib import ndiff
import os
import re
import sys

RE = re.compile('([0-9]+|[^0-9]+)')


class Error(Exception):

  pass


def get_cfns(ofns):

  fns = [RE.findall(fn) for fn in ofns]

  # check if filenames have same pattern
  d = set(tuple(item.strip('0123456789') for item in fn) for fn in fns)
  if len(d) != 1:
    raise Error(3, 'different amount of fields and/or '
                   'at least one non-number field does not have same content')

  # find the maximal lengths of number fields
  d = (idx for idx, item in enumerate(d.pop()) if not item)
  n = [(idx, max(len(fn[idx]) for fn in fns)) for idx in d]

  # pad zeros
  cfns = []
  for fn, ofn in zip(fns, ofns):
    for idx, maxlen in n:
      l = maxlen - len(fn[idx])
      if not l:
        continue
      fn[idx] = '0' * l + fn[idx]

    nfn = ''.join(fn)
    if ofn != nfn:
      cfns.append((ofn, nfn))

  return cfns


def do_renaming(cfns):

  for ofn, nfn in cfns:
    print('%s -> %s' % (ofn, nfn))
    os.rename(ofn, nfn)


def main():

  if len(sys.argv) == 1:
    return

  try:
    cfns = get_cfns(sys.argv[1:])
  except Error as e:
    print('Error %d: %s' % e.args, file=sys.stderr)
    sys.exit(1)

  if not cfns:
    print('nothing to pad zeros')
    return

  for line in ndiff(*zip(*cfns)):
    if line.startswith(('+', '?')):
      print(line.strip())

  if input('perform padding (y/n)? ') == 'y':
    do_renaming(cfns)


if __name__ == '__main__':
  main()
