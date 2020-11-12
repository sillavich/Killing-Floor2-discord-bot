
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from discord.ext import commands, tasks

import discord.ext
from test1 import *

init()

client = discord.Client()
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome(chromedriver,options=options)
drivers = webdriver.Chrome(chromedriver,options=options)
drivers.get(url)
driver.get(url)

u = driver.find_element_by_name('username')
u.send_keys(f'{username}')
p = driver.find_element_by_name('password')
p.send_keys(f'{password}')
p.send_keys(Keys.RETURN)

z = drivers.find_element_by_name('username')
z.send_keys(f'{username}')
y = drivers.find_element_by_name('password')
y.send_keys(f'{password}')
y.send_keys(Keys.RETURN)


@client.event
async def on_message(message):

    channel2=["chat"]
    channel1=["commands"]
    if message.author == client.user:
        return

    elif message.content.startswith('#help'):
        await message.channel.send('```md\n#detail in order to show current players and current server details`\n#kick (playername) in order to kick a player from the server (can be used only in command channel)\n#changemap (mapname) in order to change map (can be used only in command channel)```')
    elif message.content.startswith('#test'):
        msg = 'Hi {0.author.mention}'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('#map'):
      try:
        await message.channel.send("```css\n running ```")

        driver.get(url+ "/ServerAdmin/settings/maplist")
        map = driver.find_element_by_xpath('.//td[@class="ui-droppable"]')
        map1 = map.find_elements_by_class_name('entry')
        maplist = []
        for maps in map1:
         maplist.append(maps.text)
        maplist0 = dict.fromkeys(maplist)
        maplist1=list(maplist0)

        maplist2 = []
        for i in range(0, len(maplist1) - 1):
            maplist2.append(maplist1[i])
        maplist3='\n'.join(maplist2)
        await message.channel.send('```md\n#Maps available:\n{}```'.format(maplist3))

      except Exception as e:
          print(e)
          await message.channel.send("```fix\n Error invalid login form or incorrect username/password```")
          driver.close()
    elif  message.content.startswith('#detail'):
        driver.get('http://139.99.120.59:5075/ServerAdmin/current/info')
        player = driver.find_element_by_xpath('.//dl[@id="currentRules"]')
        players=player.text.split('\n')
        await message.channel.send('```css\n Player(s) Online:{}```'.format(players[1]))

        try:
         driver.get("http://139.99.120.59:5075/ServerAdmin/current/players")

         table = driver.find_element_by_xpath("//table[@id='players']")
         table1 = table.find_element_by_xpath("//tbody")
         list1 = []
         list2 = []
         
         for row in table1.find_elements_by_xpath(".//tr"):
            list1.append([td.text for td in row.find_elements_by_xpath(".//td")][3])
            list2.append(f'{[td.text for td in row.find_elements_by_xpath(".//td")][1]}:{[td.text for td in row.find_elements_by_xpath(".//td")][5]}')
         await message.channel.send('```md\nPlayer(s) name #{}\nCountry:(not available) ```'.format(list2))
         driver.get('http://139.99.120.59:5075/ServerAdmin/current/info')
         detail=driver.find_element_by_xpath('.//dl[@id="currentGame"]')
         details=detail.text.split('\n')
         await message.channel.send('```css\nMap={map}\nMutators={mut}```'.format(map=details[7],mut=details[9]))
        except:
            await message.channel.send("```fix\n No players online```")
            driver.get('http://139.99.120.59:5075/ServerAdmin/current/info')
            detail=driver.find_element_by_xpath('.//dl[@id="currentGame"]')
            details=detail.text.split('\n')
            await message.channel.send('```css\nMap={map}\nMutators={mut}```'.format(map=details[7],mut=details[9]))

    elif str(message.channel) in channel1:
        if message.content.startswith('#kick '):
            player=message.content[6:]
            driver.get("http://139.99.120.59:5075/ServerAdmin/current/players")
            table = driver.find_element_by_xpath("//table[@id='players']")
            table1 = table.find_element_by_xpath("//tbody")
            list2 = []
            for row in table1.find_elements_by_xpath(".//tr"):
                list2.append([td.text for td in row.find_elements_by_xpath(".//td")][1])
            if player in list2:

                driver.get("http://139.99.120.59:5075/ServerAdmin/console")
                change = driver.find_element_by_name('command')
                change.send_keys('kick {}'.format(player))
                change.send_keys(Keys.RETURN)
                await message.channel.send("```fix\n {}'s arse has been removed from the server goodluck!```".format(player))
            else:
                await message.channel.send("```fix\nCouldn't find player with that name! ```")
                return False
        if message.content.startswith('#changemap '):
            changemap=message.content[11:]
            try:
             driver.get("http://139.99.120.59:5075/ServerAdmin/console")
             change = driver.find_element_by_name('command')
             change.send_keys('switch {}'.format(changemap))
             change.send_keys(Keys.RETURN)
             await message.channel.send('```css\n changing map to {}```'.format(changemap))
            except:
             await message.channel.send('```fix\n "{}" not found try #map (ex.#changemap KF-Outpost)```'.format(changemap))

    elif str(message.channel) in channel2:
        if message.author == client.user:
            return
        else:
            driver.get(url + "/ServerAdmin/current/chat+frame")
            sub = driver.find_element_by_class_name('chatframe')
            sub1 = sub.find_element_by_xpath("//div[@id='content']")
            sub2 = sub1.find_element_by_xpath("//div[@id='chat']")
            sub3 = sub2.find_element_by_xpath("//form[@id='chatform']")
            sub4 = sub3.find_element_by_id("chatmessage")
            sub4.send_keys(message.content)
            sub4.send_keys(Keys.RETURN)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    chatbox.start()
    spam.start()


@tasks.loop(seconds=1)
async def chatbox():
            channelchatbot = client.get_channel(int(chatbotchannelid))

            try:

                drivers.get(url + "/ServerAdmin/current/chat+frame")
                chat = drivers.find_element_by_class_name('chatframe')
                chat1 = chat.find_element_by_xpath("//div[@id='content']")
                chat2 = chat1.find_element_by_xpath("//div[@id='chatlog']")
                list = chat2.find_elements_by_xpath(".//span[@class='message']")
                list1 = chat2.find_elements_by_class_name('username')
                a = str((list[-1].text))
                b1 = str((list1[-1].text))

                async for message in channelchatbot.history(limit=1):
                    if message.content !=  f'``{b1}``:{a}':
                        await channelchatbot.send(f'``{b1}``:{a}')

            except Exception as e:
                pass

@tasks.loop(seconds=60)
async def spam():
 channel = client.get_channel(int(botspamchannelid))

 driver.get('http://139.99.120.59:5075/ServerAdmin/current/info')
 player = driver.find_element_by_xpath('.//dl[@id="currentRules"]')
 players = player.text.split('\n')
 if players[1] == '0/6':
        pass
 else:
        await channel.send('```css\n Player(s) Online:{}```'.format(players[1]))
        #      driver.close()
        try:
            driver.get("http://139.99.120.59:5075/ServerAdmin/current/players")

            table = driver.find_element_by_xpath("//table[@id='players']")
            table1 = table.find_element_by_xpath("//tbody")
            list1 = []
            list2 = []
            text = ''
            for row in table1.find_elements_by_xpath(".//tr"):
                list1.append([td.text for td in row.find_elements_by_xpath(".//td")][3])
                list2.append([td.text for td in row.find_elements_by_xpath(".//td")][1])
            await channel.send('```css\nPlayer(s) name:{}\nCountry:(not available) ```'.format(list2))
            driver.get('http://139.99.120.59:5075/ServerAdmin/current/info')
            detail = driver.find_element_by_xpath('.//dl[@id="currentGame"]')
            details = detail.text.split('\n')
            await channel.send('```css\nMap={map}\nMutators={mut}```'.format(map=details[7], mut=details[9]))
            await channel.send('```css\n------------------------------------------------------------```')
        except:
            await channel.send("```fix\n No players online```")
            driver.get('http://139.99.120.59:5075/ServerAdmin/current/info')
            detail = driver.find_element_by_xpath('.//dl[@id="currentGame"]')
            details = detail.text.split('\n')
            await channel.send('```css\nMap={map}\nMutators={mut}```'.format(map=details[7], mut=details[9]))
            await channel.send('```css\n------------------------------------------------------------```')



client.run(token)
