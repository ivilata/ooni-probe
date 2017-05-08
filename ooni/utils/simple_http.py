from twisted.internet import reactor
from twisted.internet.error import CannotListenError
from twisted.web import static, server
from twisted.web.resource import Resource

from sys import argv

DEFAULT_PORT = 8000

class Hello(Resource):

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        with open('var/big_file.dat', 'r') as big_file:
            return big_file.read()

listen_port = DEFAULT_PORT

for i in range(0, len(argv)):
    if  argv[i] == "--port":
        listen_port = int(argv[i+1])
            
site = server.Site(Hello())
try:
    reactor.listenTCP(listen_port, site)
    reactor.run()
except CannotListenError:
    print "Someone else is already listening on " + str(listen_port)
