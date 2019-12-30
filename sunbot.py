#id 655453559034347540
#token NjU1NDUzNTU5MDM0MzQ3NTQw.XgOuGQ.J7Yl25PfE9xuWItRuZNnZzvwqbU
TOKEN = "NjU1NDUzNTU5MDM0MzQ3NTQw.XgOuGQ.J7Yl25PfE9xuWItRuZNnZzvwqbU"
# perm 67648
# auth https://discordapp.com/oauth2/authorize?client_id=655453559034347540&scope=bot&permissions=67648
import discord
from firebase import firebase
from bs4 import BeautifulSoup as bs
import requests

firebase = firebase.FirebaseApplication("https://sunraker-bot.firebaseio.com/",None)

client = discord.Client()
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='*sun help for help'))

@client.event
async def on_message(message):
    try:
        inpString = message.content
        inpString  = inpString.split(' ')

        if '*sun' in inpString[0]:
            inpString.remove('*sun')

            if 'hey' in inpString[0]:
                msg = "Hey! " + message.author.name +"...sup?"
                await message.channel.send(msg)

            elif 'math' in inpString[0]:
                inpString.remove('math')
                ans = mather(inpString)
                mms = "`` "+str(ans)+" ``"
                await message.channel.send(mms)
            elif 'ping' in inpString[0]:
                ping = '`` '+' Current ping: '+ str(round(client.latency*100,1)) +' ``'
                await message.channel.send(ping)

            elif 'bnotes' in inpString[0]:
                inpString.remove('bnotes')
                test = bnotes(inpString,message.guild)
                await message.channel.send(test)

            elif 'lexis' in inpString[0]:
                inpString.remove('lexis')
                test = lexis(inpString)
                await message.channel.send(test)

            elif 'help' in inpString[0]:
                inpString.remove('help')
                if len(inpString) == 0:
                    helpcomms = ["``hey`` to say hey to sunrakerbot",
                                "``math [math-func] [int-set]`` to perform math stuff",
                                "``bnotes [bnotes-func] [string]`` to make guild notes",
                                "``lexis [word]`` to do a dictionary search",
                                "``ping`` to get bot ping"
                                ]
                    ms = helplister(helpcomms)

                    await message.channel.send(ms)

                elif 'math' in inpString[0]:
                    mathhelp = ["``add [int-set]`` to add",
                                "``sub [int-set]`` to subtract",
                                "``multiply [int-set]`` to multiply",
                                "``divide [int] [int]`` to divide",
                                "``mod [int] [int]`` to get remainder"
                                ]
                    ms = helplister(mathhelp)
                    await message.channel.send(ms)
                elif 'bnotes' in inpString[0]:
                    mathhelp = ["'add [string]' to add new note",
                                "'show' to show guild notes"
                                ]
                    ms = helplister(mathhelp)
                    await message.channel.send(ms)

    except:
         await message.channel.send("What?? Try `` *sun help `` for help.")


#help
def helplister(inp):
    test = inp
    fin = ""
    for i in test:
        fin +='+ '+ i +'\n\n'

    ind = ">>> **>Help:**\n"+fin+"```* You can also ask something like *sun help math or *sun help bnotes```"

    return ind


#math function
def mather(inp):
    merg = inp
    if 'add' in merg[0]:
        merg.remove('add')
        for i,j in enumerate(merg):
            merg[i] = int(j)
        return sum(merg)
    if 'multiply' in merg[0]:
        merg.remove('multiply')
        for i,j in enumerate(merg):
            merg[i] = int(j)
        res = 1
        for i in merg:
            res = res*i
        return res
    if 'mod' in merg[0]:
        merg.remove('mod')
        for i,j in enumerate(merg):
            merg[i] = int(j)
        res = merg[0] % merg[1]
        return res
    if 'divide' in merg[0]:
        merg.remove('divide')
        for i,j in enumerate(merg):
            merg[i] = int(j)
        res = merg[0] / merg[1]
        return res
    if 'sub' in merg[0]:
        merg.remove('sub')
        for i,j in enumerate(merg):
            merg[i] = int(j)
        res = merg[0]
        merg.remove(res)
        for i in merg:
            res = res - i
        return res
    else:
        return "Math function error"

#bnotes
def bnotes(inpstr,guild_name):
    guild_path = 'b-notes/'+str(guild_name)
    getter = firebase.get("/",guild_path)

    if 'add' in inpstr[0]:
        inpstr.remove('add')
        note_string = ""
        for i in inpstr:
            note_string += i +" "

        if (note_string == ""):
            return "`` No notes? ``"
        else:
            if (getter == None):
                notes = ['Notes:- <-']
                notes.append(note_string)
                firebase.put('/',guild_path,notes)
                return "`` Notes added! ``"
            else:
                guild_notes_copy = getter
                guild_notes_copy.append(note_string)
                firebase.put('/',guild_path,guild_notes_copy)
                return "`` Notes appended! ``"

    if 'show' in inpstr[0]:
        if(getter == None):
            return "`` No notes to show ``"
        else:
            get_note_str = ""
            get_note = getter
            for i in get_note:
                get_note_str += '-> '+i+'\n'

            final_note = ">>> "+get_note_str
            return final_note

    if 'drop' in inpstr[0]:
        if(getter == None):
            return "`` No notes to drop dumbo! ``"
        else:
            firebase.delete('/b-notes',str(guild_name))
            return "`` Notes dropped ``"


#lexis-vocabulary-function
def lexis(inp):
    try:

        inp_word = inp[0]

        url = "https://www.vocabulary.com/dictionary/"
        url += inp_word.lower().strip()
        req = requests.get(url)
        soup_var = bs(req.content,'lxml')
        vocab = soup_var.findAll('p',{'class' : 'short'})

        str_slice = str(vocab).replace('<p class="short">','').replace('</p>','').replace('<i>','``').replace('</i>','``').replace('[','').replace(']','')

        return str_slice
    except:
        return "`` no word like that in lexis! ``"




client.run(TOKEN)
