"""
Extract the magic number of a file.

Author: T. Palmer
Initial Release: February 2018  Version 1.0.0
"""

import os
import argparse
import hashlib
import logging


# 5) The script will:
#     a) Setup the logfile for recording information
#     b) Open the input file for "read-binary"
#        Record information about the input file to the log. (and the screen
#        if verbose is selected)
#         File Path
#         File Size
#         Last-Modified-Time
#     c) Open the output file for writing
#     d) Read the first 32 bytes of the inputFile convert them to a Hex ASCII
#        representation (hint use the binascii standard library) and then
#        write them to the output file
#     e) Close Both Files once all bytes have been written
#     f) Record information about the output file to the log (and to the
#        screen if verbose is selected)
class MagicFinder:
    """Responsible for magic number extraction business logic."""

    parsedArgs = None
    logger = None
    outputFile = None
    inputFileStats = None

    def __init__(self):
        """Magic number finder constructor."""
        self.setupParsedArguments()

        # A welcome message will be displayed along with the details of the
        # arguments specified by the user.  If the verbose option is NOT
        # specified, you will run silently unless a major error occurs.
        self.printOut("DFS-510 Week 7 Solution")
        self.printOut("Professor Hosmer, February 2018\n")
        self.printOut("Input File: " + self.parsedArgs.inputFile.name)
        self.printOut("Output File: " + self.parsedArgs.outputFile)
        self.printOut("Log File: " + self.parsedArgs.logFile + "\n")
        self.printOut("Creating Log File")
        self.setupLogger()
        self.logger.info("Week 7 Solution, Professor Hosmer")

    def perform(self):
        """Perform magic number extraction business logic."""
        self.printOut("Extracting File Stats ...")
        self.inputFileStats = os.fstat(self.parsedArgs.inputFile.fileno())

        # self.printOut("Opening the Input File ...")
        # self.logger.info(
        #     "File: " + self.parsedArgs.inputFile.name +
        #     " Open File Success"
        # )
        self.printOut("Reading the Input File Contents ...")
        inputContents = self.readFile(self.parsedArgs.inputFile)
        self.logger.info(
            "File: " + self.parsedArgs.inputFile.name +
            " Read the file stats Sucess"
        )

        self.printOut("Hashing the File Contents - SHA256 ...")
        fileHash = self.fileHash(inputContents)
        self.logger.info(
            "File: " + self.parsedArgs.inputFile.name +
            " SHA256: " + fileHash
        )
        self.printOut("Reading the first 32 bytes of the file ...")
        # 5d) Read the first 32 bytes of the inputFile convert them to a Hex
        # ASCII representation (hint use the binascii standard library) and
        # then write them to the output file
        # TODO: Read the magic number from the inputFile
        magicNumber = "32-42-12-43"
        self.logger.info(
            "File: " + self.parsedArgs.inputFile.name +
            " Header Read: " + magicNumber
        )

        self.printOut("Creating the Output File and Recording the Results ...")
        # 3) Validate the outputFile during creation. if any errors occur
        #    report and log them and abort the script.
        # 5c) Open the output file for writing
        # Record information about the input file:
        #         File Path
        #         File Size
        #         Last-Modified-Time
        # TODO: Open and write to output file
        outputFile = self.validateAndOpenFile(self.parsedArgs.outputFile, 'w')
        # Your output file should look like this.
        #
        # File Name: Solution.py
        # File Size: 7570
        # Last Modified: Wed Oct 25 17:26:16 2017
        # SHA256 Hash: 2f1cfd7abc52bee5b5ce1d8b591f9f75e3a73935d980b9ace022a9028e84adb8
        # File Header: 27-27-27-0d-0a-44-46-53-2d-35-31-30-20-57-45-45-4b-20-37-20-53-4f-4c-55-54-49-4f-4e-0d-0a-50-52
        outputFile.write("File Name: " + self.parsedArgs.inputFile.name)
        outputFile.write("File Size: " + self.inputFileStats.st_size())

        # 5f) Record information about the output file to the log (and to the
        #     screen if verbose is selected)
        # 5e) Close Both Files once all bytes have been written
        self.parsedArgs.inputFile.close()
        outputFile.close()
        self.printOut("Script Complete")

    def setupParsedArguments(self):
        """Initialize parsedArgs."""
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
        # 5b) Open the input file for "read-binary"
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
            default='magicFinderLog.log'
        )

        self.parsedArgs = parser.parse_args()

    def setupLogger(self):
        """Initialize logger."""
        # 2) Validate the logFile during creation.  If any errors occur report
        #    them and abort.
        # 5a) Setup the logfile for recording information
        logging.basicConfig(
            filename=self.parsedArgs.logFile,
            level=logging.DEBUG,
            format='%(asctime)s %(message)s'
        )
        self.logger = logging.getLogger('com.palmer.magicfinder')

    def printOut(self, message):
        """If the verbose option is set, print the passed message."""
        # 4) If the verbose option is specified then meaningful output is
        #    provided for each major step of the script.
        if self.parsedArgs.verbose:
            print(message)

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
            self.logger.error(path + ' is not a valid file.')
            return False

    def openFile(self, path, mode):
        """Attempt to open the file and return it."""
        try:
            openFile = open(path, mode)
        except IOError:
            self.logger.error('Failed to open: ' + path)
            return
        else:
            return openFile

    def readFile(self, openedFile):
        """Attempt to read the file contents and return them."""
        try:
            contents = openedFile.read()
        except IOError:
            openedFile.close()
            self.logger.error('Failed to read: ' + openedFile)
            return
        else:
            return contents

    # TODO: Convert to SHA256 hash
    def fileHash(self, contents):
        """Calcuate an MD5 hash of given contents."""
        hash = hashlib.md5()
        hash.update(contents)
        hexMD5 = hash.hexdigest()
        return hexMD5.upper()


magicFinder = MagicFinder()
magicFinder.perform()
