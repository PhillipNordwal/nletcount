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

def first(x): return x[0];
def second(x): return x[1];

def nletddict(filename, window_width = 2):
  """Returns a frequency count defaultdict.
  
  Returns a default dict whose keys are window_width sequences of characters, and
  whose value is the frequency count of the sequence."""
  counts = defaultdict(int)
  with open(filename, "rb") as f:
    for pair in window(iter(lambda:f.read(1).lower(), ""), window_width):
      counts["".join(pair)]+=1
  return counts

def nletcount(filename, window_width = 2):
  """Returns a frequency count list.
  
  Returns a sorted list of tuples whose first element is the frequency count
  and whose second element is the window_width sequence of characters for which
  it occurs."""
  return sorted([(j,i) for (i,j) in nletddict(filename, window_width).items()])

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

def countprint(counts, printmessage, printarguments=None):
  if printarguments:
    print printmessage % printarguments
  else:
    print printmessage
  print "\n".join(map(repr, counts))


def dispcouplets(fname, rows=2, cols=2, size='small',
                 divs=7, normalized=False):
  import numpy as np
  import matplotlib.pylab as plt
  chars=sorted(nletddict(fname, 1))
  sp = nletddict(fname, 2)
  mat = [[sp[ci+cj] for cj in chars] for ci in chars]
  matlab = [[ci+cj for cj in chars] for ci in chars]
  maxcount = max(max(mat))
  l = len(chars)
  pos = np.arange(l)+.5
  for s in range(0, l, rows*cols):
    plt.figure()
    for i in range(rows*cols):
      if i+s<l:
        plt.subplot(rows, cols, i+1)
        plt.barh(pos,mat[i+s],align='center')
        plt.yticks(pos,map(repr,map(second, matlab[i+s])))
        plt.ylabel("couplets")
        plt.xlabel("count")
        if not normalized:
          plt.xticks(np.arange(divs+1)*maxcount/divs, size=size)
        else:
          plt.xticks(size=size)
        plt.title("The %d couplets that begin with %s" % (sum(mat[i+s]), repr(matlab[i+s][0][0])))
  plt.show()

def main():
  use = """Usage: python %prog [options] filename"""
  ver = "%prog 0.2"
  parser = OptionParser(usage=use, version=ver)
  parser.add_option("-s", "--single-char-frequencies",
                    action = "store_true",
                    dest = "single",
                    help = "Display single character frequencies")
  parser.add_option("-g", "--graph-display",
                    action = "store_true",
                    dest = "graph",
                    help = "Display graphs (requires matplotlib and numpy)")
  parser.add_option("-n", "--normalized",
                    action = "store_true",
                    dest = "normalized",
                    help = "Display graphs normalized (-g or --graph-display must be set)")
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

  if options.pos != None:
    if not options.filt:
      parser.error("-p or --pos can't be set without -f or --filter being specified")
    elif options.pos >= options.window_width:
      parser.error("|pos| must be less than window_width")
  if options.normalized and not options.graph:
    parser.error("-g or --graph-display must be specified with -n or --normailized")
  if len(args) != 1:
    parser.error("incorrect number of arguments")
  filename = args[0]

  if options.single:
    # print single character frequencies
    scounts = nletcount(filename, 1)
    countprint(scounts, "letter counts", None)

  pcounts = nletcount(filename, options.window_width)
  if options.filt:
    f_counts = countfilter(options.filt, pcounts, options.pos)
    if options.pos == None:
      countprint(f_counts, "nlets that contain %s", options.filt)
    else: # options.pos set
      countprint(f_counts, "nlets that contain %s in the %s'th position", (options.filt, options.pos))
  else: # options.filt not set
    countprint(pcounts, "nlet counts of length %s", options.window_width)
  if options.graph:
    dispcouplets(filename, normalized=options.normalized)


if __name__ == "__main__":
  exit(main())
