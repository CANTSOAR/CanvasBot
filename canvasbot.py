import discord
import datetime as dt

token = "REDACTED"

colors = ["white", "black", "orange", "blue", "red", "brown", "purple", "green", "yellow"]
emojinames = ["white_large", "black_large", "orange", "blue", "red", "brown", "purple", "green", "yellow"]

open_canvas = []

canvas_row_ids = []

channel_id = 83046730 #REDACTED

painters = {}

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("[]help"):
        await message.channel.send("Everyone gets one pixel a day, similar to that thing on reddit they did \nthe grid is 20x20, and the colors are the squares in the emoji thing")

    if msg.startswith("[]create"):

        if str(message.author) != "MËGĀ#7297":
            await message.channel.send("only for admin sry")
            return

        global open_canvas

        size = msg.split()[1]
        size = int(size)

        blank = [[0 for x in range(size)] for y in range(size)]
        open_canvas = blank

        for row in string_format(open_canvas):
            send_row = await message.channel.send(row)
            canvas_row_ids.append(send_row.id)
        
        print(canvas_row_ids)

        await message.channel.send("done")

    if msg.startswith("[]paint"):

        print(painters)

        if message.author not in painters:
            painters[message.author] = dt.datetime.now()
        else:
            if dt.datetime.now() - painters[message.author] < dt.timedelta(seconds = 30):
                await message.channel.send("plz wait ur 30 seconds")
                return

        print(dt.datetime.now() - painters[message.author])

        posandcol = msg.split()[1:4]

        if len(posandcol) < 3:
            await message.channel.send("after paint, put in coords then color example: []paint 3 7 red")
            return

        x = int(posandcol[0])
        y = int(posandcol[1])
        color = posandcol[2]

        if x not in range(1, 21) or y not in range(1, 21) or color not in colors:
            await message.channel.send("after paint, put in coords then color example: []paint 3 7 red")
            return
        
        color = emojinames[colors.index(color)]

        await message.channel.send(":" + color + "_square: at " + str(x) + ", " + str(y))

        open_canvas[y-1][x-1] = emojinames.index(color)

        painters[message.author] = dt.datetime.now()

        channel = client.get_channel(channel_id)
        print(channel)
        row_to_edit = await channel.fetch_message(canvas_row_ids[y-1])
        print(row_to_edit.content)

        await row_to_edit.edit(content = string_format(open_canvas)[y-1])

    if msg.startswith("[]view"):

        for row in string_format(open_canvas):
            await message.channel.send(row)
        
def string_format(canvas):
    size = range(len(canvas))
    msg = []

    for y in size:
        canv_row = ""
        for x in size:
            canv_row += ":" + emojinames[canvas[y][x]] + "_square: "

        msg.append(canv_row)

    return msg

def status_format(canvas):
    size = range(len(canvas))
    msg = ""

    for y in size:
        for x in size:
            msg += str(canvas[y][x]) + ":"

        msg += "|"

    print(msg)

    return msg

print(channel_id)
client.run(token)