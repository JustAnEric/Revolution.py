import asyncio, logging
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
        request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/internet", "GET").request(), RequestType.GET, "json").c()['hasInternet']
        if request == "false":
            print(f"{Color.OKCYAN}revolution.bot.checks{Color.ENDC}{Color.NORMAL_SPACE}{Color.FAIL}You have no internet connection or your router or proxy is not allowing this site to be accessed. Please try again.{Color.ENDC}")
        if request == "true":
            return BotApplication()

class BotApplication():
    def __init__(self):
        self.token = None
        self.invoked = False
        self.watching_servers = []
        self.events = {}
        self.server_storage = {}
        self.bot = {
            "name": "Bot"
        }
    async def run(self, token, in_server=""):
        self.token = token
        self.invoked = True
        self.watching_servers = in_server
        if token == None or token == "": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly.{Color.ENDC}")
        request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/python/token_exists", "GET", headers={"token": token}).request(), RequestType.GET, "json").c()
        if request['token_exists'] == "false": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly. (NO TOKEN FOUND IN DB){Color.ENDC}")
        print(f"{Color.OKCYAN}revolution.bot.api{Color.ENDC}{Color.NORMAL_SPACE}   {Color.OKGREEN}Hosting bot to servers: {Color.ENDC}{Color.OKBLUE}{in_server}{Color.ENDC}")
        try: await self.events['ready']()
        except Exception as e: print(e)
        pingrequest = PingRequest("https://revolution-web.repl.co/api/v1/python/ping_bot_online", RequestType.GET)
        await pingrequest.request(0.5, self.after_each_request)
    
    def get(self):
        return self.bot
    
    def setup(self, name):
        if self.invoked:
            return print(f"{Color.FAIL}revolution.bot.before_invoke.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}{Color.ENDC}")
        self.bot['name'] = name

    def get_server(self, id):
        if id not in self.watching_servers: return print(f"{id} SERVER IS NOT BEING WATCHED! ADD IT TO THE WATCH LIST.")
        if self.invoked:
            request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/get_server_messages", "GET", headers={"id": id}).request(), RequestType.GET, "json").c()
            request2 = RequestHandler(Request("http://revolution-web.repl.co/api/v1/get_server", "GET", headers={"id": id}).request(), RequestType.GET, "json").c()
            return {
                "server": request2,
                "messages": request['messages']
            }
    
    def event(self, coro):
        print(coro.__name__)
        if str(coro.__name__) == "ready":
            self.events[coro.__name__] = coro
        if str(coro.__name__) == "server_message":
            self.events[coro.__name__] = coro

    async def after_each_request(self):
        # check for new messages
        for u in self.watching_servers:
            request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/get_server_messages", "GET", headers={"id": u}).request(), RequestType.GET, "json").c()
            #compare server messages
            server = self.server_storage.get(u)
            if server is None:
                self.server_storage[u] = {
                    "server": {},
                    "messages": request['messages']
                }
                return 
            if server['messages'] == request['messages'] and request['messages'][-1]['sent_by'] == self.bot['name']:
                pass
            else: 
                #execute event and update
                try: await self.events['server_message'](u, request['messages'][-1])
                except Exception as e: print(e)
                self.server_storage = {}
                return 0
        return 0

    async def send_message(self, server, message):
        return RequestHandler(Request("http://revolution-web.repl.co/api/v1/servers/send_message", "GET", headers={"id": server, "message": message, "sent_by": self.bot['name']}).request(), RequestType.GET, "json").c()