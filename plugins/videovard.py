#t.me/ask_admin001


import aiohttp
from pyrogram import Client, filters
from config import API_KEY


#Latest Files in VideoVard
@Client.on_message(filters.command('files'))
async def files(bot, message):
    async with aiohttp.ClientSession() as session:
        msg = ""
        url = 'https://api.videovard.sx/v2/api/file/list'
        params = {'key': API_KEY,
                  'page': 1,
                  'per_page': 20,
                  }
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:

            data = await response.json()
            print(data)
            result = data["result"]
            file1 = result["files"]
            count = 0
            for file in file1:
                count += 1
                title = str(file["title"])
                link = file["link"]
                title1 = title.replace("'", "")
                print(title1)
                msg += f"{count}. <a href={link}>{title1}\n\n</a>"
            await message.reply_text(msg, quote=True)


# Search Files in VideoVard
@Client.on_message(filters.command('get_files'))
async def get_files(bot, message):
    async with aiohttp.ClientSession() as session:
        try:
            title = str(message.command[1])
            msg = ""
            url = 'https://api.videovard.sx/v2/api/file/list'
            params = {'key': API_KEY,
                      'page': 1,
                      'per_page': 20,
                      'title': title,
                      }
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:

                data = await response.json()
                print(data)
                result = data["result"]
                file1 = result["files"]
                count = 0
                for file in file1:
                    count += 1
                    title = str(file["title"])
                    link = file["link"]
                    title1 = title.replace("'", "")
                    print(title1)
                    msg += f"{count}. <a href={link}>{title1}\n\n</a>"
                if msg == "":
                    await message.reply_text("No Movies Found", quote=True)
                elif msg != "":
                    await message.reply_text(msg, quote=True)
        except IndexError:
            await message.reply_text("<code>/get_files [query]</code>", quote=True)


#remotely upload files to videovard.sx
@Client.on_message(filters.command('add_remote'))
async def link_handler(bot, message):
    try:
        link = str(message.command[1])
        short_link = await get_shortlink(link)
        await message.reply(f"<code>https://videovard.sx/e/{short_link}</code>", quote=True)
    except IndexError as e:
        await message.reply(f'`/add_remote [link]`', quote=True)


async def get_shortlink(link):
    url = 'https://api.videovard.sx/v2/api/remote/add'
    params = {'key': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            result = data["result"]
            return result["filecode"]