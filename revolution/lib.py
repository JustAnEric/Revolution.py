import asyncio, logging, websockets, websocket, json, threading
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
    async def run(self, token, in_server=[]):
        self.token = token
        self.invoked = True
        self.watching_servers = in_server
        #self.ws = await websocket.create_connection("wss://revolution-web.repl.co")
        self.wsClient = websocket.WebSocketApp(
            "wss://revolution-web.repl.co",
            on_open=self.WebSocket(self).on_open,
            on_message=self.WebSocket(self).on_message,
            on_error=self.WebSocket(self).on_error,
            on_close=self.WebSocket(self).on_close
        )

        if token == None or token == "": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly.{Color.ENDC}")
        request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/python/token_exists", "GET", headers={"token": token}).request(), RequestType.GET, "json").c()
        if request['token_exists'] == "false": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly. (NO TOKEN FOUND IN DB){Color.ENDC}")
        print(f"{Color.OKCYAN}revolution.bot.api{Color.ENDC}{Color.NORMAL_SPACE}   {Color.OKGREEN}Hosting bot to servers: {Color.ENDC}{Color.OKBLUE}{in_server}{Color.ENDC}")
        try: self.WebSocket(self).register_function_for("websocket_open",self.events['ready'],True)
        except Exception as e: raise Exception(e)

        self.wst = threading.Thread(target=self.wsClient.run_forever)
        #self.wst.daemon = True
        self.wst.start()

        conn_timeout = 5
        while not self.wsClient.sock.connected and conn_timeout:
            pass
            conn_timeout -= 1

        msg_counter = 0
        while self.wsClient.sock.connected:
            pass
            msg_counter += 1
    
    class WebSocket:
        def __init__(self, self_obj):
            self.functions = []
            self.main = self_obj

        def on_open(self,ws):
            print("[!] Opening websocket connection...")
            for i in self.functions:
                if i['type'] == "websocket_open":
                    if (i['awaited']): asyncio.run(i['function']())
                    if i['awaited'] is None or i['awaited'] == False: i['function']()
            print("latestfunction received: on_open")
            ws.send(data='{"type": "follow", "channels": '+str(self.main.watching_servers).replace("'",'"')+', "token": "'+str(self.main.token)+'"}', opcode=websocket.ABNF.OPCODE_TEXT)
            print("finished")

        def on_message(self,ws, message):
            print("latestfunction received: on_message")
            print("Received message: {}".format(message))
            for i in self.functions:
                if i['type'] == "websocket_message":
                    if (i['awaited']): asyncio.run(i['function'](message))
                    if i['awaited'] is None or i['awaited'] == False: i['function'](message)

            obj = json.loads(message)

            if (obj.get("type") == "messageCreate"):
                try:
                    for i in self.main.events:
                        if i == "server_message":
                            loop = asyncio.new_event_loop()
                            loop.run_until_complete(self.main.events[i](obj["channel"], {"message": obj['message'], "sent_by": obj['sent_by']}))

                except Exception as e: print(f"${Color.WARNING}Error while running event:\n${e}${Color.ENDC}")

        def on_close(self,ws,statuscode,statusmessage):
            print("[!] Closed websocket connection... Shutting down")
            for i in self.functions:
                if i['type'] == "websocket_close":
                    if (i['awaited']): asyncio.run(i['function']())
                    if i['awaited'] is None or i['awaited'] == False: i['function']()
            #exit(23419) # websocket connection closed // exit code/signal

        def on_error(self,ws, error):
            print(f"[!] Error while processing websocket connection: {error}\nPlease contact anyone for help with this error code.")
            for i in self.functions:
                if i['type'] == "websocket_error":
                    if (i['awaited']): asyncio.run(i['function'](error))
                    if i['awaited'] is None or i['awaited'] == False: i['function'](error)
        
        def register_function_for(self, type, function, awaited):
            if type == "websocket_open":
                self.functions.append({
                    "awaited": awaited,
                    "function": function,
                    "type": "websocket_open",
                })
            if type == "websocket_message":
                self.functions.append({
                    "awaited": awaited,
                    "function": function,
                    "type": "websocket_message",
                })
            if type == "websocket_close":
                self.functions.append({
                    "awaited": awaited,
                    "function": function,
                    "type": "websocket_close",
                })
            if type == "websocket_error":
                self.functions.append({
                    "awaited": awaited,
                    "function": function,
                    "type": "websocket_error",
                })
            return None

            

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

    class websock:
        def __init__(self,main):
            self.main = main

        def event(self):
            """Provides a method for setting up a unique event that will execute on these occasions: the websocket closes, the websocket opens or the websocket has an error."""
            return

    async def after_each_request(self):
        return
        """# check for new messages
        #for u in self.watching_servers:
            #request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/get_server_messages", "GET", headers={"id": u}).request(), RequestType.GET, "json").c()
            #compare server messages
            #server = self.server_storage.get(u)
            #if server is None:
                #self.server_storage[u] = {
                    "server": #{},
                    #"messages": request['messages']
                #}
                #return 
            #if server['messages'] == request['messages'] and request['messages'][-1]['sent_by'] == self.bot['name']:
                #pass
            #else: 
                #execute event and update
                #try: await self.events['server_message'](u, request['messages'][-1])
                #except Exception as e: print(e)
                #self.server_storage = {}
                #return 0
        #return 0"""
        
        

    async def send_message(self, server, message):
        return RequestHandler(Request("http://revolution-web.repl.co/api/v1/servers/send_message", "GET", headers={"id": server, "message": message, "sent-by": self.bot['name']}).request(), RequestType.GET, "json").c()
