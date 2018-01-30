"""
Extract information from a logfile.

Author: T. Palmer
Initial Release: February 2018  Version 1.0.0
"""

import os
import argparse


class LogScan:
    def perform(self):
        # 1) Prompts the user for the log file name (via command line)
        parser = argparse.ArgumentParser(
            'Generate a report from a given log file'
        )

        parser.add_argument(
            "-f",
            "--fileName",
            help="Specify the log file to examine",
            required=True
        )

        parsedArgs = parser.parse_args()
        fileName = parsedArgs.fileName

        # 2) Attempt to open the file, provide a meaningful error messages if
        #  anything goes wrong
        fileContents = self.verifyAndOpenFile(fileName)
        if fileContents:
            print('File exists: ' + fileContents)

            # 3) For each line in the file
            #    a) Determine if the line contains the word "worm"
            #    b) Create a list of worms that are identified throughout the
            #       file
            # 4) Generate a report that contains the information regarding each
            #    UNIQUE worms identified
            # 5) Document each step of your script in great detail

    def verifyAndOpenFile(self, path):
        if self.isValidFile(path):
            try:
                openFile = open(path, 'rb')
            except IOError:
                print('Failed to open: ' + path)
                return
            else:
                try:
                    contents = openFile.read()
                except IOError:
                    openFile.close()
                    print('Failed to read: ' + path)
                    return
                else:
                    return contents

    def isValidFile(self, path):
        # Verify that the path is valid, is not a symbolic link, and is real
        if (os.path.exists(path) and
           not os.path.islink(path) and
           os.path.isfile(path)):
            return True
        else:
            print(path + ' is not a valid file.')


scanner = LogScan()
scanner.perform()
