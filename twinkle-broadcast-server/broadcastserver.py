from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

cs = []

class MyServerProtocol(WebSocketServerProtocol):

   def onConnect(self, request):
      print("Client connecting: {0}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")
      if self not in cs:
         cs.append(self)

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
      else:
         print("Text message received: {0}".format(payload.decode('utf8')))

      ## echo back message verbatim
      self.sendMessage(payload, isBinary)
      for client in cs:
         client.sendMessage(payload)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
   factory.protocol = MyServerProtocol

   reactor.listenTCP(9000, factory)
   reactor.run()
