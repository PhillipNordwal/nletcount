"""nletcount.py generate nlet counts over a file

Generates frequency counts for nlets (overlapping sequential tuples of
characters in a given file, as well as frequency accounts for singlets
"""
from collections import defaultdict
from itertools import islice
from sys import exit

def window(seq, window_width=1):
  "Returns a sliding window (of width window_width) over data from the iterable"
  "   s -> (s0,s1,...s[window_width-1]), (s1,s2,...,swindow_width), ...        "
  result = tuple(islice(iter(seq), window_width))
  if len(result) == window_width:
    yield result    
  for elem in it:
    result = result[1:] + (elem,)
    yield result

def nletcount(filename, window_width = 2):
  counts = defaultdict(int)
  with open("enwords") as f:
    for pair in window(iter(lambda:f.read(1), ""), window_width):
      counts[("".join(pair)).lower()]+=1
  return sorted([(j,i) for (i,j) in counts.items()])

def main():
  scounts = nletcount("enwords", 1)
  pcounts = nletcount("enwords", 2)
  d_counts = filter(lambda x: 'd' in x[1], pcounts)
  f_dcounts = filter(lambda x: 'd' == x[1][1], pcounts)
  s_dcounts = filter(lambda x: 'd' == x[1][0], pcounts)
  print "letter counts"
  print "\n".join(map(repr, scounts))
  print "pairs that contain d"
  print "\n".join(map(repr, d_counts))
  print "\npairs start with d"
  print "\n".join(map(repr, f_dcounts))
  print "\npairs end with d"
  print "\n".join(map(repr, s_dcounts))

if __name__ == "__main__":
  exit(main())
