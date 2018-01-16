#!/usr/local/bin/python3
#
# first : Search a hard-coded string
# Author: T. Palmer
#
# Initial Release: January 2018  Version 1.0.0


class First:
    def perform_search(self):
        testString = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        searchWord = self.get_input()

        foundIndex = testString.find(searchWord)
        termFound = "found" if foundIndex != -1 else "not found"

        print(searchWord, "was", termFound)

    def get_input(self):
        return input("Please enter search term: ")


f = First()
f.perform_search()
