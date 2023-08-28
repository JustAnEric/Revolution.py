import asyncio, logging, websockets, websocket, json, threading, inspect, time, random, traceback
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

privateAccess = random.randint(0,204858968596849689785984892478475837583758748576930)
relative_data = {}

class upper_bot_config_class:
    def __init__(self,*,key):
        if privateAccess == key:
            self.auth = True

    def set(self,a,b):
        if self.auth is None: return
        if a and b:
            relative_data[a]=b
        else:return 0

    def get(self,a):
        if self.auth is None: return
        if a:
            return relative_data[a]
        else:return 0

    def delete(self,a,key):
        if self.auth is None: return
        if a and key == privateAccess:
            del relative_data[a]
        else:return 0

    def __repr__(self) -> dict:
        include = {
            "set":self.set,
            "get":self.get,
            "delete":self.delete,
        }
        return include

class commands:
    def __init__(self):
        pass
    
    def Bot(self):
        print(f"{Color.OKCYAN}revolution.bot.checks{Color.ENDC}   {Color.WARNING}Checking for valid internet...{Color.ENDC}")
        request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/internet", "GET").request(), RequestType.GET, "json").c()['hasInternet']
        if request == "false":
            print(f"{Color.OKCYAN}revolution.bot.checks{Color.ENDC}{Color.NORMAL_SPACE}{Color.FAIL}You have no internet connection or your router or proxy is not allowing this site to be accessed. Please try again.{Color.ENDC}")
        if request == "true":
            self.bot = BotApplication
            return self.bot()
        
    class Structure:
        """This class is for creating easy and simple structures like bot commands. No extra stuff required."""
        def __init__(self,bot,*,prefix):
            self.prefix = prefix
            self.commands = {}
            self.access = upper_bot_config_class(key=privateAccess).__repr__()
            self.bot = bot

        def help_command(self):
            def function(func):
                func

            return function

        def command(self,*,name=None,description=None):
            async def decor(s):
                self.commands[(s.__name__ or str(name))] = {"description":description, "exec":s}
                async def server_message(server:str,message:dict):
                    args = str(message['message'].split(f"{self.prefix}")[1]).split(' ',1)
                    sendReq = RequestHandler(Request("https://revolution-web.repl.co/api/v1/get_server", "GET", headers={"id":server.split('~')[0]}).request(), RequestType.GET, "json").c()
                    MESSAGE = self.Message(
                        message['message'], 
                        self.Server(sendReq, self.bot), 
                        server, 
                        self.Channel(server.split('~')[1], sendReq, self.bot), 
                        self.Member(message['sent_by'], message['author_id'], (message.get('bot') or False)),
                        message['author_id'],
                        message['id'],
                        server.split('~')[1],
                        message['id'],
                        message['timestamp'],
                        (message.get('bot') or False), 
                        (message.get('staff') or False),
                        self.bot
                    )
                    #MESSAGE.author = message['sent_by']
                    #MESSAGE.server = server
                    #MESSAGE.content = message['message']
                    #MESSAGE.channel = server.split('~')[1]
                    return await s(MESSAGE,*args)

            return decor

        async def process_commands(self,message:dict,server:str):
            args = str(message['message'].split(f"{self.prefix}")[1]).split(' ',1)
            commandName = message['message'].split(f"{self.prefix}",1)[1].split(" ",1)[0]
            MESSAGE = self.Message(
                message['message'], 
                self.Server(sendReq, self.bot), 
                server, 
                self.Channel(server.split('~')[1], sendReq, self.bot), 
                self.Member(
                    message['sent_by'], 
                    message['author_id'], 
                    (message.get('bot') or False),
                    (message.get('staff') or False)
                ), 
                message['author_id'], 
                message['id'], 
                server.split('~')[1], 
                message['id'], 
                message['timestamp'], 
                (message.get('bot') or False), 
                (message.get('staff') or False),
                self.bot
            )
            sendReq = RequestHandler(Request("https://revolution-web.repl.co/api/v1/get_server", "GET", headers={"id":server.split('~')[0]}).request(), RequestType.GET, "json").c()
            #MESSAGE.author_id = message['author_id']
            #MESSAGE.author = self.Member(message['sent_by'], MESSAGE.author_id, (message.get('bot') or False))
            #MESSAGE.server_id = server
            #MESSAGE.server = self.Server(sendReq, bot)
            #MESSAGE.content = message['message']
            #MESSAGE.channel = self.Channel(server.split('~')[1], sendReq, bot)
            #MESSAGE.channel_id = server.split('~')[1]
            #MESSAGE.message_id = message['id']
            #MESSAGE.id = message['id']
            #MESSAGE.timestamp = message['timestamp']
            #MESSAGE.bot = (message.get('bot') or False)
            #MESSAGE.staff = (message.get('staff') or False)
            for i in self.commands:
                if i == commandName:
                    return await self.commands[i]['exec'](MESSAGE,*args)
            return None
        
        class Message:
            def __init__(self, content, server, server_id, channel, author, author_id, message_id, channel_id, id, timestamp, bot, staff, botApp):
                self.content = content
                self.server = server
                self.server_id = server_id
                self.channel = channel
                self.author = author
                self.author_id = author_id
                self.message_id = message_id
                self.channel_id = channel_id
                self.id = id
                self.timestamp = timestamp
                self.bot = bot
                self.staff = staff
                self.botApp = botApp
            
            async def send(self, message):
                message = RequestHandler(Request("http://revolution-web.repl.co/api/v1/servers/send_message", "GET", headers={"id": self.server_id, "message": self.content, "token": self.botApp.token}).request(), RequestType.GET, "json").c()
                obj = commands.Structure.Message(
                    message['message'], 
                    self.server, 
                    self.server_id, 
                    self.channel, 
                    commands.Structure.Member(
                        message['sent_by'], 
                        message['author_id'], 
                        (message.get('bot') or False),
                        (message.get('staff') or False)
                    ),
                    message['author_id'],
                    message['id'],
                    self.channel_id,
                    message['id'],
                    message['timestamp'],
                    (message.get('bot') or False), 
                    (message.get('staff') or False),
                    self.bot
                )
                return obj

        class Server:
            def __init__(self, data, bot):
                def mapping_channels(a):
                    return commands.Structure.Channel(a,data,self.bot)
                def mapping_roles(a):
                    return commands.Structure.Role(a,a,self.bot)
                def mapping_members(a):
                    return commands.Structure.Member(a,a['id'],self.bot)
                    
                self.bot = bot
                self.data = data
                
                self.name = data['name']
                self.id = data['serverid']
                self.abbr = data['abbr']
                self.abbreviation = data['abbr']
                self.icon = data['imgurl']
                self.color = data['color']
                self.channels = map(mapping_channels, data['channels'])
                self.roles = map(mapping_roles, data['roles'])
                self.emojis = {"error": "Not available."}
                self.emotes = {"error": "Not available."}
                self.members = map(mapping_members, data['users_chatted'])
                self.partial = False

        class PartialServer:
            def __init__(self, id, bot):
                self.id = id
                self.bot = bot
                self.partial = True

            async def fetch(self):
                sendReq = RequestHandler(Request("https://revolution-web.repl.co/api/v1/get_server", "GET", headers={"id":self.id}).request(), RequestType.GET, "json").c()
                self.bot.cache[self.id] = sendReq
                return commands.Structure.Server(sendReq, self.bot)

        class Member:
            def __init__(self, name, id, bot, staff):
                self.bot = bot
                self.name = name
                self.id = id
                self.staff = staff

            def send(self, content):
                return print("Ignoring a usual exception: \n    [!! COMMANDS FRAMEWORK !!] Sending Direct Messages to server members is not enabled right now.")

        class Role:
            def __init__(self, id, name, bot):
                self.id = id
                self.bot = bot
                self.name = name

        class Channel:
            def __init__(self, name, parentData, bot):
                self.bot = bot
                self.id = name
                self.name = name.split('~')[0]
                self.parentData = parentData
                self.partial_parent = commands.Structure.PartialServer(self.name,bot)
                self.parent = commands.Structure.Server(parentData,bot)

            async def fetch(self):
                """
                [?] **Fetches channel messages** and returns them in a map() object.
                """
                def mapping_messages(a):
                    endRes = commands.Structure.Message()
                    endRes.content = a['message']
                    endRes.server = commands.Structure.Server(self.parentData)
                    endRes.server_id = self.name
                    endRes.channel_id = self.name.split('~')[1]
                    endRes.channel = commands.Structure.Channel(self.name.split('~')[1], self.parentData, self.bot)
                    endRes.bot = (a.get('bot') or False)
                    endRes.staff = (a.get('staff') or False)
                    endRes.author_id = a['author_id']
                    endRes.author = commands.Structure.Member(a['sent_by'], endRes.author_id, self.bot)
                    endRes.timestamp = a['timestamp']
                    return endRes
                sendRw = RequestHandler(Request(f"https://revolution-web.repl.co/get_new_messages/s/{self.id}", "GET", headers={"id":self.id}).request(), RequestType.GET, "json").c()
                return map(mapping_messages, self.parentData)
                

class BotApplication():
    def __init__(self):
        self.token = None
        self.invoked = False
        self.watching_servers = []
        self.events = {}
        self.relative_storage_class = upper_bot_config_class(key=privateAccess)
        self.server_storage = {}
        self.bot = {
            "name": "Bot"
        }
        self.socketClass = self.WebSocket(self)
        self.invokedSocket = 0
        self.websocket_cfg = {}

    async def run(self, token, in_server=[]):
        self.token = token
        self.invoked = True
        self.watching_servers = in_server
        #self.ws = await websocket.create_connection("wss://revolution-web.repl.co")
        if self.websocket_cfg.get('connect_on_start') == True or self.websocket_cfg.get('connect_on_start') == None:
            self.wsClient = websocket.WebSocketApp(
                "wss://revolution-web.repl.co",
                on_open=self.socketClass.on_open,
                on_message=self.socketClass.on_message,
                on_error=self.socketClass.on_error,
                on_close=self.socketClass.on_close
            )
        else: print("You just have disabled an essential/required part of revolution.py, experience may be slow and we may throttle you. There are expected bugs too. If this was a mistake, initialise BotApplication().WebSocketConfig in BotApplication().setup")

        if token == None or token == "": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly.{Color.ENDC}")
        request = RequestHandler(Request("http://revolution-web.repl.co/api/v1/python/token_exists", "GET", headers={"token": token}).request(), RequestType.GET, "json").c()
        if request['token_exists'] == "false": return print(f"{Color.FAIL}revolution.bot.run.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}Bot cannot run: token has not been set correctly. (NO TOKEN FOUND IN DB){Color.ENDC}")
        print(f"{Color.OKCYAN}revolution.bot.api{Color.ENDC}{Color.NORMAL_SPACE}   {Color.OKGREEN}Hosting bot to servers: {Color.ENDC}{Color.OKBLUE}{in_server}{Color.ENDC}")
        
        try:
            events_found = self._get_events__("ready")
            await events_found().exec_pool()
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
            self.ws = ws
            print("[!] Opening websocket connection...")
            for i in self.functions:
                if i['type'] == "websocket_open":
                    if (i['awaited']): asyncio.run(i['function']())
                    if i['awaited'] is None or i['awaited'] == False: i['function']()
            if self.main.websocket_cfg.get('follow_on_start') == True or self.main.websocket_cfg.get('follow_on_start') == None:
                ws.send(data='{"type": "follow", "channels": '+str(self.main.watching_servers).replace("'",'"')+', "token": "'+str(self.main.token)+'"}', opcode=websocket.ABNF.OPCODE_TEXT)
                print("[!] Opened and sent follow data")
            self.main.invokedSocket = 1

        def on_message(self,ws, message):
            self.ws = ws
            #print("Received message: {}".format(message))
            for i in self.functions:
                if i['type'] == "websocket_message":
                    if (i['awaited']): asyncio.run(i['function'](message))
                    if i['awaited'] is None or i['awaited'] == False: i['function'](message)

            obj = json.loads(message)

            if (obj.get("type") == "messageCreate"):
                try:
                    events_found = self.main._get_events__("server_message")()
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(
                        #self.main.events[i](obj["channel"], {"message": obj['message'], "sent_by": obj['sent_by']})
                        events_found.exec_pool(obj["channel"], obj)
                    )

                except Exception as e: print(f"${Color.WARNING}Error while running event:\n${e}${Color.ENDC}"); traceback.print_exc()

        def on_close(self,ws,statuscode,statusmessage):
            self.ws = ws
            print("[!] Closed websocket connection... Shutting down")
            for i in self.functions:
                if i['type'] == "websocket_close":
                    if (i['awaited']): asyncio.run(i['function']())
                    if i['awaited'] is None or i['awaited'] == False: i['function']()
            #exit(23419) # websocket connection closed // exit code/signal

        def on_error(self,ws, error):
            self.ws = ws
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
        
    def _get_events__(self,name):
        pool = []
        class ExecutablePool:
            def __init__(self):
                self.pool = pool
            def __repr__(self):
                return self.pool
            async def exec_pool(self, *args, **kwargs):
                print(args)
                print(kwargs)
                for i in self.pool:
                    await i(*args, **kwargs)
        try:
            for event in self.events:
                if event == name:
                    for execv in self.events[event]:
                        pool.append(execv)
            return ExecutablePool
        except Exception as e: raise Exception(e)

    class WebSocketConfig:
        def __init__(self,*,FOLLOW_ON_START=True,CONNECT_ON_START=True):
            self.config_stored = { "follow_on_start": FOLLOW_ON_START, "connect_on_start": CONNECT_ON_START }
        
        def __repr__(self):
            return self.config_stored
            
        def remove_all_traces(self):
            """Removes config data if necessary || if `WebSocketConfig` is stored to a variable."""
            self.config_stored = {"removed": "yes"}
        
        def store_trace_to_global_var(self,bot):
            if self.config_stored == {"removed": "yes"} or self.config_stored == {} or self.config_stored == None:
                raise BaseException("!![TRACES] No config to store.")
            bot.websocket_cfg = self.config_stored

    def get(self):
        return self.bot
    
    def setup(self,*, websocket_cfg=WebSocketConfig):
        if self.invoked:
            return print(f"{Color.FAIL}revolution.bot.before_invoke.error{Color.ENDC}{Color.NORMAL_SPACE}{Color.WARNING}{Color.ENDC}")
        self.websocket_cfg = websocket_cfg
        

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
            if self.events.get('ready') == None:
                self.events['ready'] = []
            self.events['ready'].append(coro)
        if str(coro.__name__) == "server_message":
            if self.events.get('server_message') == None:
                self.events['server_message'] = []
            self.events['server_message'].append(coro)

    class websock(WebSocket):
        def __init__(self,main):
            self.s = main

        def event(self,*,event_type:str=str):
            """
            Provides a method for setting up a unique event that will execute on these occasions: the websocket closes, the websocket opens or the websocket has an error.
            (External method that connects to the main method and registers functions)
            """

            def register_child(function):
                self.s.socketClass.register_function_for(event_type, function, inspect.iscoroutinefunction(function))
                print(f"[!] Registered websock event: {event_type.split('websocket_')[1]}")

            return register_child
        
        async def send_follow_data(self,*,code:int=int):
            socketClass = self.s.socketClass
            """[!] Sends the server follow data in case it was changed during the run."""
            if socketClass.ws:
                wait = await self.s.wait_until(somepredicate=lambda: self.s.invokedSocket,timeout=10,value_meant_to_be=1)
                socketClass.ws.send(data='{"type": "resetfollowlist", "token": "'+str(self.s.token)+'"}')
                socketClass.ws.send(data='{"type": "follow", "channels": '+str(self.s.watching_servers).replace("'",'"')+', "token": "'+str(self.s.token)+'"}', opcode=websocket.ABNF.OPCODE_TEXT)
                print("[!!] Opened and sent follow data")
            else: return print("[!!!] Follow data could not be sent, server is not active or websocket service is experiencing some issues.")
            

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
        
    async def wait_until(self, somepredicate, timeout, period=0.25, value_meant_to_be=True, *args, **kwargs):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if somepredicate == value_meant_to_be: return True
            time.sleep(period)
        return False

    async def send_message(self, server, message):
        return RequestHandler(Request("http://revolution-web.repl.co/api/v1/servers/send_message", "GET", headers={"id": server, "message": message, "sent-by": "", "token": self.token}).request(), RequestType.GET, "json").c()
