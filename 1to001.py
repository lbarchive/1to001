#!/usr/bin/env python3
import os
import re
import sys

RE = re.compile('([0-9]+|[^0-9]+)')


def main():

  ofns = sys.argv[1:]
  if not ofns:
    return

  fns = [RE.findall(fn) for fn in ofns]
  fn0 = fns[0]
  nfields = len(fns[0])

  # same number of fields
  if any(nfields != len(fn) for fn in fns):
    print('different number of fields', file=sys.stderr)
    return

  # find fields contain numbers
  n_idx = [idx for idx, item in enumerate(fn0)
           if item.strip('0123456789') == '']

  # check non-number fields have same content
  if any(fn0[idx] != fn[idx]
         for fn in fns
         for idx in range(nfields) if idx not in n_idx):
    print('at least one non-number field does not have same content',
          file=sys.stderr)
    return

  # find the maximal length
  n = [(idx, max(len(fn[idx]) for fn in fns))
       for idx in n_idx]

  # pad zeros
  cfns = []
  for fn, ofn in zip(fns, ofns):
    dfn = fn[:]
    for idx, maxlen in n:
      l = maxlen - len(fn[idx])
      if not l:
        continue
      fn[idx] = '0'*l + fn[idx]
      dfn[idx] = '\033[1;32m0\033[0m'*l + dfn[idx]

    nfn = ''.join(fn)
    if nfn != ofn:
      cfns.append((ofn, nfn))
      print(''.join(dfn))

  if not cfns:
    print('nothing to pad zeros')
    return

  if input('perform padding (y/n)? ') != 'y':
    return

  # do renaming
  for ofn, nfn in cfns:
    print('%s -> %s' % (ofn, nfn))
    os.rename(ofn, nfn)

if __name__ == '__main__':
  main()
