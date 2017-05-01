from twisted.internet.error import ConnectionRefusedError
from ooni.utils import log
from ooni.templates import tcpt

from twisted.python import usage

class UsageOptions(usage.Options):
    optParameters = [['backend', 'b', 'http://127.0.0.1:57007',
                      'URL of the test backend to use'],
                      ['peer_list', 'p', 'peer_list.txt',
                      'name of the file which stores the address of the peer']
                    ]


class PeerLocator(tcpt.TCPTest):
    """
    This test is only to connect to peers and find more peers
    so we can run web connectivity to them. 
    """
    
    usageOptions = UsageOptions
    requiredTestHelpers = {'backend': 'peer_locator_helper'}
    
    def test_peer_locator(self):
        def got_response(response):
            if response != '':
                self.report['status'] = 'no peer found'
            else:
                self.report['status'] = ''
                with open(self.localOptions['peer_list'], 'a+') as peer_list:
                    for peer in peer_list:
                        if peer == response:
                            log.msg('we already know the peer')
                            self.report['status'] = 'known peer found: %s'%response
                            break

                    if self.report['status'] != '': #no repetition
                        log.msg('new peer discovered')
                        self.report['status'] = 'new peer found: %s'%response
                        peer_list.write(response)
            
        def connection_failed(failure):
            failure.trap(ConnectionRefusedError)
            log.msg("Connection Refused")

        self.address, self.port = self.localOptions['backend'].split(":")
        self.port = int(self.port)
        payload = self.input and self.input or "1234" #http server port, we ultimately need STUN(T) to discover this
        d = self.sendPayload(payload)
        d.addErrback(connection_failed)
        d.addCallback(got_response)
        return d
