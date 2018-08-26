import os


if os.getenv('VIRTUAL_ENV'):
    print 'yes'
else:
    print 'no'    