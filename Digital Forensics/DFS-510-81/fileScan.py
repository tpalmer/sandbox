import os
import argparse

# 1) Allow a user to specify a directory
parser = argparse.ArgumentParser('Directory hashing')

parser.add_argument(
    "-d",
    "--path",
    help="Specify the directory to hash",
    required=True
)

parsedArgs = parser.parse_args()
path = parsedArgs.path

# 2) Validate that the directory exists  (provide a meaningful error message if
#    it does not)
if os.path.exists(path):
    if path:
        print "Path: " + path
else:
    print "Not a valid directory"

# 3) Using the OS module and the function os.listdir() obtain the list of files
#    that exist in the specified directory.
# 4) For each file in the directory produce the following output for each File;
#    sorted by FileSize (largest file first)
#
#    Path    FileName    FileSize   Last-Modified-Time  MD5 Hash
#
# 5) If you encounter an exception while processing the files write the
#    information associated with the exception to a python log file (you will
#    need to import the logging module)
# 6) You will submit one python file  fileScan.py
# 7) The file will contain documentation regarding the following:
#     b) Outline of your approach
#     c) Detailed documentation of each step
