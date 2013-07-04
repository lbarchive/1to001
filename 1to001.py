#!/usr/bin/env python3
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
