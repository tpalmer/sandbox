"""
Compare magic numbers with file extensions.

Author: T. Palmer
Initial Release: February 2018  Version 1.0.0

Required System Library: libmagic
Required Python Library: python-magic
"""

import magic

mime = magic.from_file("./capture.raw", mime=True)
print(mime)
