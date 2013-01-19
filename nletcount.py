"""nletcount.py generate nlet counts over a file

Generates frequency counts for nlets (overlapping sequential tuples of
characters in a given file, as well as frequency accounts for singlets
"""
from collections import defaultdict
from itertools import islice
from sys import exit
from optparse import OptionParser

def window(seq, window_width=1):
  "Returns a sliding window (of width window_width) over data from the iterable"
  "   s -> (s0,s1,...s[window_width-1]), (s1,s2,...,swindow_width), ...        "
  it = iter(seq)
  result = tuple(islice(it, window_width))
  if len(result) == window_width:
    yield result    
  for elem in it:
    result = result[1:] + (elem,)
    yield result

def nletcount(filename, window_width = 2):
  counts = defaultdict(int)
  with open("enwords", "rb") as f:
    for pair in window(iter(lambda:f.read(1), ""), window_width):
      counts[("".join(pair)).lower()]+=1
  return sorted([(j,i) for (i,j) in counts.items()])

def main():
  use = """Usage: python %prog [options] filename"""
  ver = "%prog 0.1"
  parser = OptionParser(usage=use, version=ver)
  parser.add_option("-w", "--window-width",
                    default = 2,
                    type = "int",
                    dest = "window_width",
                    help = "Tally counts of window_width lengthed substrings")
  parser.add_option("-f", "--filter",
                    dest = "filt",
                    help = "show only counts that contain filt")
  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error("incorrect number of arguments")
  filename = args[0]

  scounts = nletcount(filename, 1)
  pcounts = nletcount(filename, options.window_width)
  print "letter counts"
  print "\n".join(map(repr, scounts))
  if options.filt:
    f_counts = filter(lambda x: options.filt.lower() in x[1], pcounts)
    print "pairs that contain %s" % options.filt
    print "\n".join(map(repr, f_counts))
    if options.window_width == 2:
      ff_counts = filter(lambda x: options.filt.lower() == x[1][0], f_counts)
      print "pairs that contain %s in the first position" % options.filt
      print "\n".join(map(repr, ff_counts))
      sf_counts = filter(lambda x: options.filt.lower() == x[1][1], f_counts)
      print "pairs that contain %s in the second position" % options.filt
      print "\n".join(map(repr, sf_counts))

  else:
    print "nlet counts of length %s" %options.window_width
    print "\n".join(map(repr, pcounts))


if __name__ == "__main__":
  exit(main())
