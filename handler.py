class Handler:
    def getHandled(self):
        raise NotImplemented("A handler didn't implement getHandled. What does it handle? lava??")

    def handle(self, environ, start_response):
        raise NotImplemented("A handler didn't implement handle. Why does it even exist then?")
