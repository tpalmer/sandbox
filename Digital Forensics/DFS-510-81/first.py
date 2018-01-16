#!/usr/bin/python
#
# first : Search a hard-coded string
# Author: T. Palmer
#
# Initial Release: January 2018  Version 1.0.0


def main():
    testString = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    searchWord = raw_input("Please enter search term: ")

    foundIndex = testString.find(searchWord)
    termFound = "found" if foundIndex != -1 else "not found"

    print searchWord, "was", termFound


main()
