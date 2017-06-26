from miniupnpc import UPnP

from twisted.internet import reactor
from twisted.internet.error import CannotListenError
from twisted.web import static, server
from twisted.web.resource import Resource

import sys

DEFAULT_PORT = 8000
EXIT_BIND_FAILED = 2
EXIT_UPNP_FAILED = 3

def error(message, code):
    sys.stderr.write(message)
    sys.exit(code)

class Hello(Resource):

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        with open('var/big_file.dat', 'r') as big_file:
            return big_file.read()

def main():
    listen_port = DEFAULT_PORT
    use_upnp = False

    # Parse command line options.
    for i in range(0, len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--port":
            listen_port = int(sys.argv[i+1])
        elif arg == "--upnp":
            use_upnp = True
        elif arg == "--noupnp":
            use_upnp = False

    # Configure a UPnP port mapping if requested.
    if use_upnp:
        upnp = UPnP()
        upnp.discoverdelay = 10
        ndevs = upnp.discover()
        if ndevs == 0:
            error("No UPnP IGD devices were discovered", EXIT_UPNP_FAILED)
        if not upnp.addportmapping(listen_port, 'TCP', upnp.lanaddr, listen_port,
                                   "OONI simple HTTP peer", ''):
            error("Failed to create UPnP port mapping", EXIT_UPNP_FAILED)

    ## XXXX configure auto-removal of mapping

    # Run the HTTP server.
    site = server.Site(Hello())
    try:
        reactor.listenTCP(listen_port, site)
        reactor.run()
    except CannotListenError:
        error("Someone else is already listening on " + str(listen_port),
              EXIT_BIND_FAILED)

if __name__ == '__main__':
    main()
