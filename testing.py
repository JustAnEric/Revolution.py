from revolutionpy import main, lib
import asyncio

#request = main.RequestHandler(main.Request("http://api.ipify.org/?format=json", "GET").request(), main.RequestType.GET, "json").c()['ip']
#print(request)
#pingrequest = main.PingRequest("http://api.ipify.org/?format=json", main.RequestType.GET)
#asyncio.run(pingrequest.request(5))

bot = lib.commands().Bot()

bot.setup(
    name = "Bot"
)

print(bot.get())

bot.run("L78q92", [])