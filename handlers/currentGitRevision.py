import json
import utils
from handler import Handler


class CurrentGitRevisionHandler(Handler):
    def handle(self, environ, start_response):
        encode = json.dumps({"gitLongHash": utils.git_revision[0], "gitShortHash": utils.git_revision[1]}).encode()
        start_response("200 OK", [])
        return [encode]

    def getHandled(self):
        return "currentGitRevision"
