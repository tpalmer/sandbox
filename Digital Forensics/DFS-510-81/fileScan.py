import os
import argparse
import hashlib
import time
import pprint


class FileScan:
    def perform(self):
        # 1) Allow a user to specify a directory
        parser = argparse.ArgumentParser(
            'Calculate MD5 Hash of files in provided directory'
        )

        parser.add_argument(
            "-d",
            "--path",
            help="Specify the directory to hash",
            required=True
        )

        parsedArgs = parser.parse_args()
        path = parsedArgs.path

        # 2) Validate that the directory exists  (provide a meaningful error
        # message if it does not)
        if not os.path.exists(path):
            print "Please provide a valid directory"
            return

        # 3) Using the OS module and the function os.listdir() obtain the list
        # of files that exist in the specified directory.
        fileDictionary = {}
        for filePath in os.listdir(path):
            fullPath = os.path.join(path, filePath)
            fileContents = self.verifyAndOpenFile(fullPath)

            if fileContents:
                hashValue = self.fileHash(fileContents)
                localModifiedTime = time.ctime(os.path.getmtime(fullPath))

                if fullPath not in fileDictionary:
                    fileDictionary[fullPath] = {
                        'name': os.path.basename(fullPath),
                        'sizeInBytes': os.path.getsize(fullPath),
                        'modifiedTime': localModifiedTime,
                        'md5': hashValue
                    }

        # 4) For each file in the directory produce the following output for
        # each File; sorted by FileSize (largest file first)
        #
        #    Path    FileName    FileSize   Last-Modified-Time  MD5 Hash
        #
        # Sort output by file size
        sortedDictionary = sorted(
            fileDictionary.items(),
            key=lambda x: x[1]['sizeInBytes'],
            reverse=True
        )
        pprint.pprint(sortedDictionary)

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

    # Calcuate the MD5 hash
    def fileHash(self, contents):
        hash = hashlib.md5()
        hash.update(contents)
        hexMD5 = hash.hexdigest()
        return hexMD5.upper()
# 5) If you encounter an exception while processing the files write the
#    information associated with the exception to a python log file (you will
#    need to import the logging module)
# 6) You will submit one python file  fileScan.py
# 7) The file will contain documentation regarding the following:
#     b) Outline of your approach
#     c) Detailed documentation of each step


scanner = FileScan()
scanner.perform()
