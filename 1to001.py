#!/usr/bin/env python3
import os
import re
import sys

RE = re.compile('([0-9]+|[^0-9]+)')


class Error(Exception):

  pass


def get_cfns(ofns):

  fns = [RE.findall(fn) for fn in ofns]
  fn0 = fns[0]
  nfn0 = len(fns[0])

  # same number of fields
  if any(nfn0 != len(fn) for fn in fns):
    raise Error(1, 'different number of fields')

  # find fields contain numbers
  n_idx = [idx for idx, item in enumerate(fn0) if not item.strip('0123456789')]

  # check if non-number fields have same content
  if any(fn0[idx] != fn[idx]
         for fn in fns
         for idx in range(nfn0) if idx not in n_idx):
    raise Error(2, 'at least one non-number field does not have same content')

  # find the maximal lengths of number fields
  n = [(idx, max(len(fn[idx]) for fn in fns)) for idx in n_idx]

  # pad zeros
  cfns = []
  dfns = []
  for fn, ofn in zip(fns, ofns):
    dfn = fn[:]
    for idx, maxlen in n:
      l = maxlen - len(fn[idx])
      if not l:
        continue
      fn[idx] = '0' * l + fn[idx]
      dfn[idx] = '\033[1;32m%s\033[0m%s' % ('0' * l, dfn[idx])

    if fn != dfn:
      cfns.append((ofn, ''.join(fn)))
      dfns.append(''.join(dfn))

  return cfns, dfns


def do_renaming(cfns):

  for ofn, nfn in cfns:
    print('%s -> %s' % (ofn, nfn))
    os.rename(ofn, nfn)


def main():

  fns = sys.argv[1:]
  if not fns:
    return

  try:
    cfns, dfns = get_cfns(fns)
  except Error as e:
    print('Error %d: %s' % e.args, file=sys.stderr)
    sys.exit(1)

  if not cfns:
    print('nothing to pad zeros')
    return

  for dfn in dfns:
    print(dfn)

  if input('perform padding (y/n)? ') == 'y':
    do_renaming(cfns)


if __name__ == '__main__':
  main()
