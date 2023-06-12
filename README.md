# Revolution.py
This is a Python fork of the working Revolution API.

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
    print(bot.get())
    print(bot.get_server("revolution"))

@bot.event
async def server_message(server, message):
    if str(message['message']).lower() == "hi":
        return await bot.send_message(server, "Hello!")

asyncio.get_event_loop().run_until_complete(bot.run("L78q92", ["revolution"])) # insert your token
```