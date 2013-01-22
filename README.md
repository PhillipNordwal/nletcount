nletcount
=========

Generates frequency counts for nlets (overlapping sequential tuples of characters in a given file, as well as frequency accounts for singlets

```
Usage: python nletcount.py [options] filename

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s, --single-char-frequencies
                        Display single character frequencies
    -w WINDOW_WIDTH, --window-width=WINDOW_WIDTH
                        Tally counts of window_width lengthed substrings.
  -f FILT, --filter=FILT
                          Show only counts that contain filt.
    -p POS, --pos=POS     Require that the filt character specified with -f or
                          --filter be at the pos'th position.
```
