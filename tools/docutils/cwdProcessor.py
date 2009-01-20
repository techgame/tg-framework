#!c:\python24\python.exe

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.common import path
import locale
from docutils import core

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(rstExtension='.txt'):
    locale.setlocale(locale.LC_ALL, '')
    cwd = path.path('.')

    for sourceName in cwd.listdir('*' + rstExtension):
        destName = sourceName.stripext() + '.html'
        print "Processing:", sourceName, "into:", destName
        core.publish_file(source_path=sourceName, destination_path=destName, writer_name='html')

if __name__=='__main__':
    main()

