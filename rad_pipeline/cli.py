
"""Usage: rad [-vqrh] [FILE] ...
          rad (--left | --right) CORRECTION FILE
Process FILE and optionally apply correction to either left-hand side or
right-hand side.
Arguments:
  FILE        optional input file
  CORRECTION  correction angle, needs FILE, --left or --right to be present
Options:
  -h --help
  -v       verbose mode
  -q       quiet mode
  -r       make report
  --left   use left-hand side
  --right  use right-hand side
"""
import sys
from docopt import docopt


def main():
    """Console script for rad_pipeline."""

    arguments = docopt(__doc__)
    print("Arguments: " + str(arguments))
    print("Change this message by putting your code into "
          "rad_pipeline.cli.main")
    print("See docopt documentation at http://docopt.org/")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
