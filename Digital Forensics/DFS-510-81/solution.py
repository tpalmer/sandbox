# Arguments include the following:
# -v verbose  (this argument will be optional)
# -i inputFile (this argument is mandatory and requires the user to specify a
#    single input file) You must validate the inputFile exists, and is
#    readable, during within argparse.
# -o outputFile (this argument is mandatory and requires the user to specify a
#    single output file)
# -l logFile  (this argument will specify the log file to be used to record
#    results and exceptions)
#
# 1) Validate the inputFile from within argparse and report any errors abort.
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

"""
Calculate MD5 Hash of files in provided directory.

Author: T. Palmer
Initial Release: February 2018  Version 1.0.0

Required PyPI Library: texttable
"""

import os
import argparse
import logging

logging.basicConfig(
    filename='week7Log.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)
logger = logging.getLogger('com.palmer.week7')


class Week7:
    sortedFileList = []
    parsedArgs = None

    def perform(self):
        parser = argparse.ArgumentParser(
            'Calculate MD5 Hash of files in provided directory'
        )

        parser.add_argument(
            "-d",
            "--path",
            help="Specify the directory to hash",
            required=True
        )

        self.parsedArgs = parser.parse_args()
        path = self.parsedArgs.path

        # 2) Validate that the directory exists
        if not os.path.exists(path):
            logger.error("Please provide a valid directory")
            return

        # 3) Using the OS module and the function os.listdir() obtain the list
        #    of files that exist in the specified directory.
        tempDictionary = {}
        for filePath in os.listdir(path):
            fullPath = os.path.join(path, filePath)
            openedFile = self.validateAndOpenFile(fullPath, 'rb')
            if not openedFile:
                break

            fileContents = self.readFile(openedFile)
            if fileContents:
                hashValue = self.fileHash(fileContents)
                localModifiedTime = time.ctime(os.path.getmtime(fullPath))

                # Store relevant data points in a dictionary using the path
                # as the key
                tempDictionary[fullPath] = {
                    'name': os.path.basename(fullPath),
                    'sizeInBytes': os.path.getsize(fullPath),
                    'modifiedTime': localModifiedTime,
                    'md5': hashValue
                }

            openedFile.close()

        # Sort the dictionary by file size
        self.sortedFileList = sorted(
            tempDictionary.items(),
            key=lambda x: x[1]['sizeInBytes'],
            reverse=True
        )
        self.generateReport()

    def generateReport(self):
        # 4) For each file in the directory produce the following output for
        # each File; sorted by FileSize (largest file first)
        #
        #    Path    FileName    FileSize   Last-Modified-Time  MD5 Hash
        #
        # Use the texttable module to format the output in a more
        # human-readable format
        table = Texttable()
        table.add_row([
            "Path",
            "FileName",
            "FileSize",
            "Last-Modified-Time",
            "MD5-Hash"
        ])
        for path, fileDictionary in self.sortedFileList:
            table.add_row([
                path,
                fileDictionary["name"],
                fileDictionary["sizeInBytes"],
                fileDictionary["modifiedTime"],
                fileDictionary["md5"]
            ])
        print(table.draw())

    # If this file is valid, attempt to open it and return the opened file
    def validateAndOpenFile(self, path, mode):
        if self.isValidFile(path):
            return self.openFile(path, mode)
        else:
            return None

    # Verify that the path is valid, is not a symbolic link, and is real
    def isValidFile(self, path):
        if (os.path.exists(path) and
           not os.path.islink(path) and
           os.path.isfile(path)):
            return True
        else:
            logger.error(path + ' is not a valid file.')
            return False

    # Attempt to open the file and return it
    def openFile(self, path, mode):
        try:
            openFile = open(path, mode)
        except IOError:
            logger.error('Failed to open: ' + path)
            return
        else:
            return openFile

    # Attempt to read the file contents and return them
    def readFile(self, openedFile):
        try:
            contents = openedFile.read()
        except IOError:
            openedFile.close()
            logger.error('Failed to read: ' + openedFile)
            return
        else:
            return contents

    # Calcuate an MD5 hash of given contents
    def fileHash(self, contents):
        hash = hashlib.md5()
        hash.update(contents)
        hexMD5 = hash.hexdigest()
        return hexMD5.upper()


scanner = FileScan()
scanner.perform()
