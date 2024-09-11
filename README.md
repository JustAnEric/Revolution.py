# Revolution.py
This is a Python fork of the working Revolution API.

# IMPORTANT: 
> :warning: This Revolution.py fork does ***NOT*** apply to the new and improved Revolution version.

## REQUIREMENTS
- aiohttp
- requests
- websockets
> If these are **not prompted to automatically install,** you will have to install them yourself using the command below.
```sh
pip install aiohttp websockets requests
```

## USAGE

```python
from revolutionpy import main, lib
import asyncio

bot = lib.commands().Bot()

bot.setup(
    name = "Cool Bot" # name of your bot account. default is "Bot"
)

@bot.event
async def ready():
    print(bot.get()) # gets the bot instance (JSON)
    print(bot.get_server("revolution")) # prints json of server information

@bot.event
async def server_message(server, message):
    if str(message['message']).lower() == "hi":
        return await bot.send_message(server, "Hello!") # sends a message to the following server by ID.

asyncio.get_event_loop().run_until_complete(
    bot.run(
        "L78q92", # token
        "revolution" # guild id
    )
) # insert your token and guild id to invoke the bot to. The bot will not be given editing permissions unless the owner of the server gives it permission.
```

## Install the development build of Revolution.py
If you want to test out new features, you can download the latest release and extract the ZIP into your `site-packages` folder.
If you cannot do this, add this line of code into your main file before running the bot:
```python
...
from revolutionpy import development_builds
development_builds.initialize(app)
...
```
This should initialize and download the new code.

## Commands Structure Documentation
The commands structure class documentation is available on the Revolution website:
[https://revolution-web.repl.co/api/docs/py](https://revolution-web.repl.co/api/docs/py)
