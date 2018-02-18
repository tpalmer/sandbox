"""
Extract the magic number of a file.

Author: T. Palmer
Initial Release: February 2018  Version 1.0.0
"""

import os
import argparse
import hashlib
import logging

logging.basicConfig(
    filename='magicFinderLog.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)
logger = logging.getLogger('com.palmer.magicfinder')


class MagicFinder:
    """Responsible for magic number extraction business logic."""

    parsedArgs = None

    def perform(self):
        """Perform magic number extraction business logic."""
        parser = argparse.ArgumentParser(
            'solution'
        )

        # -v verbose (optional)
        parser.add_argument(
            "-v",
            "--verbose",
            help="Be more verbose with output",
            action="store_true"
        )

        # 1) Validate the inputFile exists, and is readable within argparse.
        #    Report any errors and abort.
        # -i inputFile (this argument is mandatory and requires the user to
        #    specify a single input file)
        parser.add_argument(
            "-i",
            "--inputFile",
            help="The file to extract the magic number from",
            type=argparse.FileType('rb'),
            required=True
        )

        # -o outputFile (this argument is mandatory and requires the user to
        #    specify a single output file)
        parser.add_argument(
            "-o",
            "--outputFile",
            help="The file to write magic number information to",
            required=True
        )

        # -l logFile (this argument will specify the log file to be used to
        #    record results and exceptions)
        parser.add_argument(
            "-l",
            "--logFile",
            help="The file to log activity information to",
            default='solutionLog.txt'
        )

        self.parsedArgs = parser.parse_args()

    def validateAndOpenFile(self, path, mode):
        """If the file is valid, open it and return the opened file."""
        if self.isValidFile(path):
            return self.openFile(path, mode)
        else:
            return None

    def isValidFile(self, path):
        """Verify the path is valid, is not a symbolic link, and is real."""
        if (os.path.exists(path) and
           not os.path.islink(path) and
           os.path.isfile(path)):
            return True
        else:
            logger.error(path + ' is not a valid file.')
            return False

    def openFile(self, path, mode):
        """Attempt to open the file and return it."""
        try:
            openFile = open(path, mode)
        except IOError:
            logger.error('Failed to open: ' + path)
            return
        else:
            return openFile

    def readFile(self, openedFile):
        """Attempt to read the file contents and return them."""
        try:
            contents = openedFile.read()
        except IOError:
            openedFile.close()
            logger.error('Failed to read: ' + openedFile)
            return
        else:
            return contents

    def fileHash(self, contents):
        """Calcuate an MD5 hash of given contents."""
        hash = hashlib.md5()
        hash.update(contents)
        hexMD5 = hash.hexdigest()
        return hexMD5.upper()


magicFinder = MagicFinder()
magicFinder.perform()


# 2) Validate the logFile during creation.  If any errors occur report them
#    and abort the script.
# 3) Validate the outputFile during creation. if any errors occur report and
#    log them and abort the script.
# 4) If the verbose option is specified then you will provide meaningful
#    output for each major step of the script.  In addition, a welcome message
#    will be displayed along with the details of the arguments specified by
#    the user.  If the verbose option is NOT specified, you will run silently
#    unless a major error occurs.
# 5) The script will:
#     a) Setup the logfile for recording information
#     b) Open the input file for "read-binary"
#        Record information about the input file to the log. (and the screen
#        if verbose is selected)
#         File Path
#         File Size
#         Last-Modified-Time
#     b) Open the output file for writing
#     c) Read the first 32 bytes of the inputFile convert them to a Hex ASCII
#        representation (hint use the binascii standard library) and then
#        write them to the output file
#     d) Close Both Files once all bytes have been written
#     e) Record information about the output file to the log (and to the
#        screen if verbose is selected)
#
# Your output file should look like this.
#
# File Name: Solution.py
# File Size: 7570
# Last Modified: Wed Oct 25 17:26:16 2017
# SHA256 Hash: 2f1cfd7abc52bee5b5ce1d8b591f9f75e3a73935d980b9ace022a9028e84adb8
# File Header: 27-27-27-0d-0a-44-46-53-2d-35-31-30-20-57-45-45-4b-20-37-20-53-4f-4c-55-54-49-4f-4e-0d-0a-50-52
#
# Your Log file should look like this.
#
# 2017-10-25 17:19:30,433 Week 7 Solution, Professor Hosmer
# 2017-10-25 17:19:30,433 File: Solution.py Read the file stats Sucess
# 2017-10-25 17:19:30,433 File: Solution.py Open File Success
# 2017-10-25 17:19:30,433 File: Solution.py File Contents Read Success
# 2017-10-25 17:19:30,433 File: Solution.py SHA256: 18496a26e116e0c0d93984e8102e2d86a5310c65e23bcd0a13ad22334d86b016
# 2017-10-25 17:19:30,433 File: Solution.py Header Read: 27-27-27-0d-0a-44-46-53-2d-35-31-30-20-57-45-45-4b-20-37-20-53-4f-4c-55-54-49-4f-4e-0d-0a-50-52-
#
# Your Screen Output when Verbose is selected should look like this.
#
# DFS-510 Week 7 Solution
# Professor Hosmer, October 2017
#
# Input File: ProfessorSolution.py
# Output File: result.txt
# Log File: log.txt
#
# Creating Log File
# Extracting File Stats ...
# Opening the Input File ...
# Reading the Input File Contents ...
# Hashing the File Contents - SHA256 ...
# Reading the first 32 bytes of the file ...
# Creating the Output File and Recording the Results ...
#
# Script Complete
