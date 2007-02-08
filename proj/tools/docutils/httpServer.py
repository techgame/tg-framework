#!c:\python24\python.exe

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import locale
from cgi import escape
from StringIO import StringIO
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

import docutils.core

import TG.common.path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DocutilsRequest(SimpleHTTPRequestHandler):
    _base_ = SimpleHTTPRequestHandler
    protocol_version = "HTTP/1.0"
    rstExtension = '.txt'

    def do_GET(self):
        path = self.translate_path(self.path)
        path = TG.common.path.path(path)
        if path.splitext()[1] == '.rst':
            output = self.writeRSTFile(path.stripext()+self.rstExtension)
            self.copyfile(output, self.wfile)
        else:
            self._base_.do_GET(self)

    def do_HEAD(self):
        path = self.translate_path(self.path)
        path = TG.common.path.path(path)
        if path.splitext()[1] == '.rst':
            self.writeRSTFile(path.stripext()+self.rstExtension)
        else:
            self._base_.do_HEAD(self)

    def list_directory(self, path):
        cwd = TG.common.path.path(path)
        try:
            doclist = [cwd.relpathto(x) for x in cwd.listdir('*' + self.rstExtension)]
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        doclist.sort(lambda a, b: cmp(a.lower(), b.lower()))
        doclist = [x.stripext()+'.rst' for x in doclist]

        fileListing = StringIO()
        self.writeFileListing(fileListing, doclist, 'DocUtils listing for ' + cwd.relpath())
        return self.postResponse(fileListing, 'text/html')

    def writeRSTFile(self, inputPath):
        inputFile = inputPath.open('rb')
        outputFile = StringIO()
        outputFile.close = lambda: None # docutils insists on closing the file
        try:
            docutils.core.publish_file(source=inputFile, destination=outputFile, writer_name='html')
        finally:
            inputFile.close()
        return self.postResponse(outputFile, 'text/html')

    def writeFileListing(self, fileListing, listing, title='Listing'):
        write = fileListing.write
        write("<html>\n<header>\n")
        write("<title>%s</title>\n" % title)
        write("</header>\n<body>\n")
        write("<h2>%s</h2>\n" % title)
        write("<hr>\n<ul>\n")
        for name in listing:
            name = escape(name)
            write('<li><a href="%s">%s</a>\n' % (name, name))
        write("</ul>\n<hr>\n")
        write("</body>\n</html>\n")

    def postResponse(self, resultFile, contentType="text/html"):
        if hasattr(resultFile, 'seek'):
            resultFile.seek(0, 2) # seek to the end of the file
        else:
            print type(resultFile), resultFile
        if hasattr(resultFile, 'tell'):
            length = resultFile.tell()
        if hasattr(resultFile, 'seek'):
            resultFile.seek(0, 0) # seek to the beginning of the file
        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return resultFile

def DocutilsServer(address=('localhost', 8080), rstExtension='.txt'):
    DocutilsRequest.rstExtension = rstExtension
    httpd = HTTPServer(address, DocutilsRequest)
    return httpd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(address=('localhost', 8080), rstExtension='.txt'):
    locale.setlocale(locale.LC_ALL, '')
    httpd = DocutilsServer(address, rstExtension)
    httpd.serve_forever()

if __name__=='__main__':
    main()

