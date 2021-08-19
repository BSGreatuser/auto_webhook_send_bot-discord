import requests, asyncio, discord, json, os, shutil, sys, time, aiohttp
from discord_webhook import DiscordWebhook, DiscordEmbed
from collections import OrderedDict
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import tasks
from itertools import cycle
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

token = 'token'

client = discord.Client()
mkjson = OrderedDict()

status = cycle(['=명령어', '{n}개의 서버'])

@client.event
async def on_ready():
    print(client.user)
    change_message.start()

@client.event
async def on_message(message):
    if message.guild is None:
        return

    async def pause():
        if not os.path.isdir(f'./DB/{message.guild.id}/working'):
            return

        await asyncio.sleep(1200)
        await work()


    async def work():
        async with aiohttp.ClientSession() as session:
            if not os.path.isdir(f'./DB/{message.guild.id}/working'):
                return
            with open(f'./DB/{message.guild.id}/{message.guild.id}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            everyone = data['everyone']
            invite = data['invite']
            name = data['name']
            avatar = data['avatar']
            thumb_url = data['thumbnail']
            color = data['color']
            inter = int(color, 16)
            color = int(hex(inter), 0)
            icon = 'https://cdn.discordapp.com/emojis/756692866289631312.gif?v=1'

            count = 0

            f = open(f'./DB/{message.guild.id}/ments.txt', 'r', encoding='utf-8')
            ments = f.read()
            f.close()

            if everyone == 'true':
                content = '@everyone'
            else:
                content = '@'

            webhooks = open(f'./DB/{message.guild.id}/{message.guild.id}.txt', 'r')

            used = []
            total = len(webhooks.readlines())

            with open(f'./DB/{message.guild.id}/{message.guild.id}.txt', "r", encoding='utf-8'):
                webhooks = open(f'./DB/{message.guild.id}/{message.guild.id}.txt', encoding='utf-8')
                for i in range(total):
                    if len(used) >= int(total):
                        await pause()

                    if not os.path.isdir(f'./DB/{message.guild.id}/working'):
                        return

                    count += 1

                    swebhook = webhooks.readline().strip()
                    try:
                        webhook = Webhook.from_url(url=swebhook, adapter=AsyncWebhookAdapter(session))
                    except:
                        pass
    

                    e = discord.Embed(description=ments, color=color)
                    e.set_author(name=message.guild.name, url=invite, icon_url=icon)
                    e.add_field(name='디스코드 서버주소', value=invite)
                    e.set_thumbnail(url=thumb_url)
                    e.set_footer(text=str(message.author), icon_url=str(message.author.avatar_url))

                    try:
                        await webhook.send(content=f'{content}ㅣ{invite}', username=name, embed=e, avatar_url=avatar)
                    except:
                        pass

                    used.append(swebhook)
                    print(f'{message.author}: {str(len(used))} / {total}\n{time.ctime().split(" ")[4]} [{str(count)}] {swebhook[:-15]}***************\n\n')

                    #res = requests.post(webh, json=data)

                    #if not res.status_code == 200:
                    #    pass

                    await asyncio.sleep(1)
                await pause()
    ###############################################################################################

    if message.content == '=명령어':
        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(title='봇 초대하기', description='24시간 자동으로 웹훅메시지를 보내주는 멋진 봇',
                                  url='https://discord.com/api/oauth2/authorize?client_id=838608625244045342&permissions=8&scope=bot',
                                  colour=discord.Colour.gold())
            embed.set_footer(text='관리자 권한이 있을시 명령어를 볼 수 있습니다')
        else:
            embed = discord.Embed(title='명령어', url='https://discord.gg/F82Z6c43WE'')
            embed.add_field(name='=등록', value='\u200b', inline=False)
            embed.add_field(name='=수정 서버주소 [서버주소]', value='웹훅메시지에 들어갈 서버주소를 설정합니다', inline=False)
            embed.add_field(name='=멘트 [홍보글]', value='홍보멘트를 설정합니다', inline=False)
            embed.add_field(name='=웹훅추가 [웹훅]', value='줄바꿈으로 웹훅 여러개 추가 가능합니다', inline=False)
            embed.add_field(name='=전송', value='설정된 값에 맞춰 자동으로 웹훅메시지를 전송합니다', inline=False)
        await message.channel.send(f'{message.author.mention} 디엠을 확인해주세요')
        await message.author.send('https://discord.gg/F82Z6c43WE', embed=embed)


    if message.content == '=등록':
        if message.author.guild_permissions.administrator:
            if os.path.isdir(f'./DB/{message.guild.id}'):
                embed = discord.Embed(description='', color=discord.Colour.red())
                embed.set_author(name='이미 등록된 서버',
                                 icon_url='https://cdn.discordapp.com/emojis/820991216182624266.png?v=1')
                embed.set_footer(text=f'▶ {message.author}')
                await message.reply(embed=embed)
                return

            os.mkdir(f'./DB/{message.guild.id}')
            mkjson['everyone'] = 'true'
            mkjson['invite'] = 'https://discord.gg/F82Z6c43WE'
            mkjson['name'] = '봉순이 배너봇'
            mkjson['avatar'] = 'https://i.imgur.com/oBPXx0D.png'
            mkjson['thumbnail'] = 'https://i.imgur.com/oBPXx0D.png'
            mkjson['color'] = '03b2f8'
            mkjson['delay'] = '50'  # 단위: 분
            with open(f'./DB/{message.guild.id}/{message.guild.id}.json', 'w', encoding='utf-8') as making:
                json.dump(mkjson, making, ensure_ascii=False, indent='\t')

            #if not os.path.isfile('f./DB/{message.guild.id}/{message.guild.id}.json'):
            #    await message.reply('파일 생성에 오류가 발생하였습니다\n관리자에게 문의해주세요')
            #    return

            embed = discord.Embed(description='', color=discord.Colour.green())
            embed.set_author(name=f'등록완료',
                             icon_url='https://cdn.discordapp.com/emojis/820904919518937118.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
        else:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='권한 부족', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)

    if message.content.startswith('=수정'):
        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='권한 부족', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        if not os.path.isdir(f'./DB/{message.guild.id}'):
            # 미등록서버
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='등록되지 않은 서버',
                             icon_url='https://cdn.discordapp.com/emojis/820991216182624266.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        try:
            target = message.content.split(" ")[1]
        except IndexError:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='수정할 값이 지정되지 않음',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        with open(f'./DB/{message.guild.id}/{message.guild.id}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        '''수정'''

        if target == '서버주소':
            try:
                thumb_url = message.content.split(" ")[2]
            except IndexError:
                embed = discord.Embed(description='', color=discord.Colour.red())
                embed.set_author(name='주소가 입력되지 않음',
                                 icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
                embed.set_footer(text=f'▶ {message.author}')
                await message.reply(embed=embed)
                return

            if str(thumb_url).startswith('https://discord.gg/'):
                data['invite'] = thumb_url
                with open(f'./DB/{message.guild.id}/{message.guild.id}.json', 'w', encoding='utf-8') as making:
                    json.dump(data, making, indent='\t')

                with open(f'./DB/{message.guild.id}/{message.guild.id}.json', 'r') as f:
                    data = json.load(f)

                status = data['invite']
                embed = discord.Embed(description='', color=discord.Colour.green())
                embed.set_author(name=f'{status}로 수정됨',
                                 icon_url='https://cdn.discordapp.com/emojis/820991216203726878.png?v=1')
                embed.set_footer(text=f'▶ {message.author}')
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(description='', color=discord.Colour.red())
                embed.set_author(name='주소가 잘못됨',
                                 icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
                embed.set_footer(text=f'▶ {message.author}')
                await message.reply(embed=embed)



    if message.content.startswith('=웹훅추가'):
        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='권한 부족', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        if not os.path.isdir(f'./DB/{message.guild.id}'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='등록되지 않은 서버', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            await message.reply(embed=embed)
            return

        try:
            item = message.content.split(" ")[1]
        except IndexError:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='웹훅이 입력되지 않음',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        await message.delete()

        if not '/api/webhooks' in item:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='잘못된 형식',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.channel.send(message.author.mention, embed=embed)
            return
            

        '''
        try:
            res = requests.get(item, verify=False)
        except:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='잘못된 형식',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.channel.send(message.author.mention, embed=embed)
            return

        if not res.status_code == 200:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='만료된 웹훅',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.channel.send(message.author.mention, embed=embed)
            return
        elif res.status_code == 429:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='Status code: 429\n일시적으로 ip가 차단되었습니다\n관리자에게 추가요청 또는 대량추가를 이용해주세요',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.channel.send(message.author.mention, embed=embed)
            return
        '''
            

        if not os.path.isfile(f'./DB/{message.guild.id}/{message.guild.id}.txt'):
            f = open(f'./DB/{message.guild.id}/{message.guild.id}.txt', 'w')
            f.close()
            txt = open(f'./DB/{message.guild.id}/{message.guild.id}.txt', 'w', encoding='utf-8')
            txt.write(item)
            txt.close()
        else:
            txt = open(f'./DB/{message.guild.id}/{message.guild.id}.txt', 'a', encoding='utf-8')
            txt.write("\n{0}".format(item))
            txt.close()
        embed = discord.Embed(description='', color=discord.Colour.green())
        embed.set_author(name=f'추가완료',
                         icon_url='https://cdn.discordapp.com/emojis/820991216203726878.png?v=1')
        embed.set_footer(text=f'▶ {message.author}')
        await message.channel.send(message.author.mention, embed=embed)

    if message.content == '=전송':
        if os.path.isdir(f'./DB/{message.guild.id}/ban'):
            await message.channel.send(f'{message.author.mention} 사용이 차단된 서버입니다.\n관리자에게 문의해주세요.\nhttps://discord.gg/F82Z6c43WE')
            return
        
        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='권한 부족', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        if not os.path.isdir(f'./DB/{message.guild.id}'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='등록되지 않은 서버', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            await message.reply(embed=embed)
            return

        if not os.path.isfile(f'./DB/{message.guild.id}/{message.guild.id}.txt'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='웹훅이 추가되지 않음',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        if not os.path.isfile(f'./DB/{message.guild.id}/ments.txt'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='멘트가 추가되지 않음',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        if os.path.isdir(f'./DB/{message.guild.id}/working'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='이미 전송되는 중',
                             icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return
        
        with open(f'./DB/{message.guild.id}/{message.guild.id}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        delay = data['delay']

        print(f'{message.guild.id} ◇ {str(delay)}분')

        try:
            os.mkdir(f'./DB/{message.guild.id}/working')
        except:
            return
        
        #await message.channel.send('딜레이 50분 미만으로 설정해주세요 ~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
        await asyncio.sleep(1)
    
        embed = discord.Embed(description='', color=discord.Colour.green())
        embed.set_author(name=f'전송 시작됨',
                         icon_url='https://cdn.discordapp.com/emojis/810163083640176661.png?v=1')
        embed.set_footer(text=f'▶ {message.author}')
        await message.reply('봉순이네 복구중\nhttps://discord.gg/F82Z6c43WE', embed=embed)
        await work()


    if message.content.startswith('=멘트'):
        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='권한 부족', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            embed.set_footer(text=f'▶ {message.author}')
            await message.reply(embed=embed)
            return

        if not os.path.isdir(f'./DB/{message.guild.id}'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='등록되지 않은 서버', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            await message.reply(embed=embed)
            return

        try:
            checking = message.content.split(" ")[1]
        except IndexError:
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='글 미작성됨', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            await message.reply(embed=embed)
            return

        ments = message.content[4:]

        f = open(f'./DB/{message.guild.id}/ments.txt', 'w')
        f.close()

        if not os.path.isfile(f'./DB/{message.guild.id}/ments.txt'):
            embed = discord.Embed(description='', color=discord.Colour.red())
            embed.set_author(name='[오류] 파일 생성실패\n관리자에게 문의해주세요', icon_url='https://cdn.discordapp.com/emojis/820904919484596245.png?v=1')
            await message.reply(embed=embed)
            return

        with open(f'./DB/{message.guild.id}/ments.txt', 'w', encoding='utf-8') as p:
            p.write(ments)

        embed = discord.Embed(description='', color=discord.Colour.green())
        embed.set_author(name='멘트 설정됨', icon_url='https://cdn.discordapp.com/emojis/820904919518937118.png?v=1')
        embed.set_footer(text=f'▶ {message.author}')
        await message.reply(embed=embed)


@tasks.loop(seconds=5)
async def change_message():
    name = next(status)
    name = name.format(n=len(client.guilds))
    await client.change_presence(activity=discord.Game(name))


client.run(token)
