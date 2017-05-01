from twisted.internet import reactor
from twisted.web import static, server
from twisted.web.resource import Resource

class Hello(Resource):

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        return '<html>Hello, world!</html>'%(request.prepath)

site = server.Site(Hello())
reactor.listenTCP(8000, site)
reactor.run()
