
"""usage: rad
           [-c <name>=<value>] [--help]
           <command> [<args>...]
options:
   -c <name=value>
   -h, --help
The most commonly used rad commands are:
   ashp       Process the ASHP file
   gshp       Process the GSHP file
   evs        Process the Electric Vehicle File
   solar      Process the Solar Panels file
"""
import sys
from docopt import docopt

import rad_pipeline.pipeline


def main():
    """Console script for rad_pipeline."""

    # arguments = docopt(__doc__)
    # print("Arguments: " + str(arguments))
    # print("Change this message by putting your code into "
    #       "rad_pipeline.cli.main")
    # print("See docopt documentation at http://docopt.org/")


if __name__ == "__main__":
    rad_pipeline.pipeline.main()
