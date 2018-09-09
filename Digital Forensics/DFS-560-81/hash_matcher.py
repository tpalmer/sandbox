"""
Find plaintext that corresponds to password hash.

Author: T. Palmer
"""


class HashMatcher:
    def perform(self):
        passwords = self.openFile('passwords.txt', 'r')
        wordlist = self.openFile('wordlist.txt', 'r')

        if passwords and wordlist:
            for rawHash in passwords:
                hash = rawHash.strip()
                for wordRow in wordlist:
                    plaintext, listHash = wordRow.strip().split('\t')
                    if listHash == hash:
                        print(listHash + ' -> ' + plaintext)
                        break

    # Attempt to open the file and return it
    def openFile(self, path, mode):
        try:
            openFile = open(path, mode)
        except IOError:
            print('Failed to open: ' + path)
            return
        else:
            return openFile


matcher = HashMatcher()
matcher.perform()
