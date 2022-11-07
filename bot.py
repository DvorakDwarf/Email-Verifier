import discord
import csv
from discord.ext import commands
from discord.utils import get

SERVER_ID = int(input("WHat is the ID of the server ?\n"))
role_name = input("What is the name of the member role ?\n")
organizer_role_name = input("What role should be able to update the database ?\n")
TOKEN = input("What is the bot's token ?\n")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

guild = bot.get_guild(SERVER_ID)

@bot.event
async def on_ready():
    print("Bot Ready")
    await bot.change_presence(activity=discord.Game(name="$verify [e-mail]"))

#Main command. Checks that the emil following the command against emails.csv
#All of the commands are expected to be used in DMs with the bot
#emails.csv is a bunch of fake emails 
@bot.command()
async def verify(ctx, email):
    author = ctx.message.author

    with open('emails.csv', 'r') as file:
        if is_used(email) == True:
            await author.send("Sorry, email has already been used")
            return

        reader = csv.reader(file)
        for row in reader:
            #If email is in the email csv
            if email == row[0]:
                #Adds emails to already used list
                with open('used_emails.csv', 'a') as file:
                    file.write(email + "\n")

                server = bot.get_guild(SERVER_ID)
                user = server.get_member(author.id)
                role = get(server.roles, name=role_name)

                await user.add_roles(role)

                await author.send("Thank you, your email has been verified")
                return

        await author.send("Sorry, your email has not been found")

#Check whether an email has already been used
def is_used(email):
    with open('used_emails.csv', 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            if email == row[0]:
                return True
            
        return False

#Update emails.csv with another .csv
@bot.command()
async def update(ctx):
    msg = ctx.message
    author = ctx.message.author

    server = bot.get_guild(SERVER_ID)
    user = server.get_member(author.id)
    role = get(server.roles, name=organizer_role_name)

    if role in user.roles:
        if len(msg.attachments) > 0:
            file = msg.attachments[0]
            if file.filename == "emails.csv":
                await file.save('emails.csv')
                await author.send("File updated")
            else:
                await author.send("File must follow the format")
        else:
            await author.send("You did not attach any files")
    else:
        await author.send("You don't have the permission to use this command")

bot.run(TOKEN)