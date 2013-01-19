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
  """Returns a frequency count list.
  
  Returns a sorted list of tuples whose first element is the frequency count
  and whose second element is the window_width sequence of characters for which
  it occurs."""
  counts = defaultdict(int)
  with open(filename, "rb") as f:
    for pair in window(iter(lambda:f.read(1), ""), window_width):
      counts[("".join(pair)).lower()]+=1
  return sorted([(j,i) for (i,j) in counts.items()])

def countfilter(filt, counts, pos=None):
  """Returns a occurences in counts that contain the filter

  counts is a frequency count list, a list of tuples whose first element is the
  frequency count, and whose second element is the sequence of characters for 
  which the count is for.

  When pos is None, or not specified the return value is the list of tuples for
  which the second element contains the sequence in filt.

  When pos is a number the return value is the list of tuples for which the
  second elements pos'th character matches the character in filt.
  """
  if pos == None:
    return filter(lambda item: filt in item[1], counts)
  else:
    return filter(lambda item: filt == item[1][pos], counts)

def main():
  use = """Usage: python %prog [options] filename"""
  ver = "%prog 0.2"
  parser = OptionParser(usage=use, version=ver)
  parser.add_option("-w", "--window-width",
                    default = 2,
                    type = "int",
                    dest = "window_width",
                    help = "Tally counts of window_width lengthed substrings.")
  parser.add_option("-f", "--filter",
                    dest = "filt",
                    help = "Show only counts that contain filt.")
  parser.add_option("-p", "--pos",
                    default = None,
                    type = "int",
                    dest = "pos",
                    help = "Require that the filt character specified with -f or --filter be at the pos'th position.")
  (options, args) = parser.parse_args()

  if options.pos != None and not options.filt:
    parser.error("-p or --pos can't be set without -f or --filter being specified")
  if len(args) != 1:
    parser.error("incorrect number of arguments")
  filename = args[0]

  scounts = nletcount(filename, 1)
  pcounts = nletcount(filename, options.window_width)
  # print single character frequencies
  print "letter counts"
  print "\n".join(map(repr, scounts))

  if options.filt:
    f_counts = countfilter(options.filt, pcounts, options.pos)
    if options.pos != None:
      print "pairs that contain %s" % options.filt
    else: # options.pos set
      print "pairs that contain %s in the %s'th position" % (options.filt, options.pos)
    print "\n".join(map(repr, f_counts))
  else: # options.filt not set
    print "nlet counts of length %s" %options.window_width
    print "\n".join(map(repr, pcounts))


if __name__ == "__main__":
  exit(main())
