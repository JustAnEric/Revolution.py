import asyncio, logging, termcolor
from .main import *

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NORMAL_SPACE = "   "

class commands:
    def __init__(self):
        pass
    
    def Bot(self):
        print(f"{Color.OKCYAN}revolution.bot.checks{Color.ENDC}   {Color.WARNING}Checking for valid internet...{Color.ENDC}")
        request = RequestHandler(Request("http://revolution.ericplayzyt.repl.co/api/v1/internet", "GET").request(), RequestType.GET, "json").c()['hasInternet']
        if request == "false":
            print(f"{Color.OKCYAN}revolution.bot.checks{Color.ENDC}{Color.NORMAL_SPACE}{Color.FAIL}You have no internet connection or your router or proxy is not allowing this site to be accessed. Please try again.{Color.ENDC}")
        if request == "true":
            return BotApplication()

class BotApplication():
    def __init__(self):
        self.token = None
        self.invoked = False
        self.bot = {
            "name": "Bot"
        }
    def run(self, token, in_servers=[]):
        self.token = token
        self.invoked = True
        if token == None or token == "": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly.{Color.ENDC}")
        request = RequestHandler(Request("http://revolution.ericplayzyt.repl.co/api/v1/python/token_exists", "GET", headers={"token": token}).request(), RequestType.GET, "json").c()
        if request['token_exists'] == "false": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly. (NO TOKEN FOUND IN DB){Color.ENDC}")
        print(f"{Color.OKCYAN}revolution.bot.api{Color.ENDC}{Color.NORMAL_SPACE}   {Color.OKGREEN}Hosting bot to servers: {Color.ENDC}{Color.OKBLUE}{in_servers}{Color.ENDC}")
        pingrequest = PingRequest("http://api.ipify.org/?format=json", RequestType.GET)
        asyncio.run(pingrequest.request(10))
    
    def get(self):
        return self.bot
    
    def setup(self, name):
        if self.invoked:
            return print(f"{Color.FAIL}revolution.bot.before_invoke.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}{Color.ENDC}")
        self.bot['name'] = name