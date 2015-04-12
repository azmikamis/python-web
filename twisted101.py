__author__ = 'azmi'

from twisted.web.server import Site  # glues a listening server port to the HTTP protocol implementation
from twisted.web.static import File  # glues the HTTP protocol implementation to the filesystem
from twisted.internet import reactor  # accepting TCP connections and moving bytes into and out of them
from twisted.web.resource import Resource  # represents a page
from twisted.web.error import Error
from time import ctime
from calendar import calendar


class YearPage(Resource):
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        return "<html><body><pre>%s</pre></body></html>" % (calendar(self.year),)


class Calendar(Resource):
    def getChild(self, name, request):
        try:
            year = int(name)
        except ValueError:
            return Error()
        else:
            return YearPage(year)


class Clock(Resource):
    isLeaf = True  # ClockPage resources will never have any children

    def render_GET(self, request):
        return "<html><body>%s</body></html>" % (ctime(),)  # what will be sent to the browser

root = Resource()
root.putChild("tmp", File('/tmp'))
root.putChild("clock", Clock())
root.putChild("calendar", Calendar())

factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()