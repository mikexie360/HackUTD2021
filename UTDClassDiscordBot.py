import discord
from discord.ext import commands
from discord import colour
from discord.utils import get
import random
import math
import requests

from asyncio import sleep as s

from itertools import chain
from datetime import datetime
import time
from io import StringIO
import sys
import os
import configparser
import json

client = commands.Bot(command_prefix = ".")
client.remove_command('help')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='.ping',value='Returns Pong and latency in ms!\nNo Arguments', inline=False)
    embed.add_field(name='.createRole',value='Only Admins of server can execute this command. Creates a new role/pronoun.\nOne Argument [newRole]', inline=False)
    embed.add_field(name='.addRole',value='The Bot will give you a new role/pronoun.\nOne Argument [Role]', inline=False)
    embed.add_field(name='.removeRole',value='The Bot will remove a role/pronoun from you.\nOne Argument [Role]', inline=False)
    embed.add_field(name='.createChannel',value='The Bot will create a new private channel between members who share the role.\nTwo Arguments [channelName] [Role]', inline=False)
    embed.add_field(name='.python',value='The Bot will compile and run python code for you. Use code blocks to run the python code.\nExample: .python \`\`\`print("hello world")\`\`\`\nOne Argument [pythonCode]', inline=False)
    embed.add_field(name='.whois',value='The Bot will give a short description of the student.\nOne Argument [member]', inline=False)
    embed.add_field(name='.courseNotes', value="The Bot will give you an image of the notes in a course.\nExample: .courseNotes CS 0\nArgument [course] [int]")
    embed.add_field(name='.math', value="The Bot will use the Wolframalpha API\nArgument [string]")
    embed.add_field(name='.create_course', value="The Bot will create a public channel\nArgument [channelName]")
    embed.add_field(name='.remind', value="The Bot will give the student a dm of upcomming assignments and tests.\nArgument")
    embed.add_field(name='.new', value="The Bot will add a new assignment or test.\nArgument [string]")
    embed.add_field(name='.askQuestion', value="The Bot will post a question for Everyone to Answer.\nArgument [string]")
    embed.add_field(name='.showQuestion', value="The Bot will show questions to be answered.\nArgument")
    embed.add_field(name='.answerQuestion', value="The Bot will accept an answer for a question by a student.\nArgument [questionNumber] [answer]")

    await author.send(embed=embed)

@client.command()
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name, decription = member.mention, color = discord.Colour.red())
    
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text=f"Requested by{ctx.author.name}.")

    await ctx.send(embed=embed)

imageArrayCS = ["https://upload.wikimedia.org/wikipedia/commons/8/84/Finite_State_Machine_diagram.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/3d/Truth_table.JPG","https://upload.wikimedia.org/wikipedia/commons/9/91/HARDWARE.jpg"]
imageArrayPSY = ["https://upload.wikimedia.org/wikipedia/commons/0/07/Brain_regions_involved_in_memory_formation.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/26/An_American_text-book_of_the_diseases_of_children._Including_special_chapters_on_essential_surgical_subjects%3B_orthopaedics%2C_diseases_of_the_eye%2C_ear%2C_nose%2C_and_throat%3B_diseases_of_the_skin%3B_and_on_the_%2814592501170%29.jpg", "https://commons.wikimedia.org/wiki/File:Neuron.jpg"]
@client.command(name="courseNotes")
async def image(ctx, course, topic):
    title = "image "+ course+ " " + topic
    description = "image "+ course + " " + topic
    embed = discord.Embed(title = title, decription = description, color = discord.Colour.red())
    if (course == "CS"):
        try:
            urllink = imageArrayCS[int(topic)]
        except:
            embed.add_field(name = "Error", value = 'That image is unavailable', inline = True)
            await ctx.send(embed=embed)
            return
            
    elif (course == "PSY"):
        try:
            urllink = imageArrayPSY[int(topic)]
        except:
            embed.add_field(name = "Error", value = 'That image is unavailable', inline = True)
            await ctx.send(embed=embed)
            return
    else:
        embed.add_field(name = "Error", value = "Course does not exist", inline = True)
        await ctx.send(embed=embed)
        return
    embed.set_image(url = urllink)
    embed.set_footer(icon_url = ctx.author.avatar_url, text=f"Requested by{ctx.author.name}.")
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def ping(ctx):
    embed = discord.Embed(title = "Pong!", decription = f'Latencey is {round(client.latency * 1000)}ms', color = discord.Colour.red())
    embed.add_field(name="Latency",value =f'Latencey is {round(client.latency * 1000)}ms', inline = True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def createRole(ctx, *,Role):
    try:
        guild = ctx.guild
        await guild.create_role(name=Role)
        embed = discord.Embed(title = "Create Role", color = discord.Colour.red())
        embed.add_field(name="Role Created",value =f'Role {Role} has been created!', inline = True)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title = "Incorrect Permissions", color = discord.Colour.red())
        embed.add_field(name="Cannot Create Role",value ='You do not have permissions to create a role', inline = True)
        await ctx.send(embed=embed)

@client.command()
async def addRole(ctx,*, Role):
    if Role == "student":
        embed = discord.Embed(title = "Incorrect Role", color = discord.Colour.red())
        embed.add_field(name="Cannot Set Role",value ='You do not have permissions to add yourself to this role.', inline = True)
        await ctx.send(embed=embed)
        return
    member = ctx.message.author
    await member.add_roles(discord.utils.get(member.guild.roles, name=Role))
    embed = discord.Embed(title = "Successfully added Role", color = discord.Colour.red())
    embed.add_field(name="Added Role",value =f'Pronoun `{Role}` has been given to {member}', inline = True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def removeRole(ctx, *, Role : discord.Role):
    if Role == "student":
        embed = discord.Embed(title = "Cannot remove self as student role", color = discord.Colour.red())
        embed.add_field(name="Cannot Remove",value ='You cannot remove yourself as a student', inline = True)
        await ctx.send(embed=embed)
        return
    if Role in ctx.author.roles:
        await ctx.author.remove_roles(Role)
        embed = discord.Embed(title = "Success", color = discord.Colour.red())
        embed.add_field(name="Removed Role",value =f'{ctx.message.author} removed role {Role} from {ctx.message.author}.', inline = True)
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title = "You do not have that role to remove", color = discord.Colour.red())
        embed.add_field(name="You tried to remove a role that you do not have",value =f'{ctx.message.author} already does not have Role {Role}.', inline = True)
        await ctx.send(embed=embed)

@client.command()
async def createChannel(ctx, channelName, *, role):
    guild = ctx.guild
    member = ctx.author
    admin_role = get(guild.roles, name=role)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(channelName, overwrites=overwrites)
    embed = discord.Embed(title = "Creating Chanel", color = discord.Colour.red())
    embed.add_field(name=f'Creating a private group channel',value =f'Creating channel called {channelName} for students with {role} role', inline = True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def schedule(ctx):
    area=ctx.message.channel
    await ctx.send(file=discord.File(r'C:\Users\Mork\Desktop\DiscordBot\schedule.PNG'))


@client.event
async def on_reaction_add(reaction, user):
    channel = 815339366179930172
    messageid = 815476838804488193
    if reaction.message.channel.id != channel:
        return

    if(reaction.emoji == "✅"):
        await user.add_roles(discord.utils.get(user.guild.roles, name="student"))
        embed = discord.Embed(title = "New Role", color = discord.Colour.red())
        embed.add_field(name=f'New verified role',value =f'Student `{user}` has been verified and now has the student role!', inline = True)
        await user.send(embed=embed)
        return
    elif(reaction.emoji == "🟦"):
        await user.add_roles(discord.utils.get(user.guild.roles, name="he/him"))
        embed = discord.Embed(title = "New Role", color = discord.Colour.red())
        embed.add_field(name=f'New verified role',value =f'Student `{user}` now has the he/him pronoun!', inline = True)
        await user.send(embed=embed)
        return
    elif(reaction.emoji == "🟥"):
        await user.add_roles(discord.utils.get(user.guild.roles, name="she/her"))
        embed = discord.Embed(title = "New Role", color = discord.Colour.red())
        embed.add_field(name=f'New verified role',value =f'Student `{user}` now has the she/her pronoun!', inline = True)
        await user.send(embed=embed)        
        return
    elif(reaction.emoji == "🟪"):
        await user.add_roles(discord.utils.get(user.guild.roles, name="they/them"))
        embed = discord.Embed(title = "New Role", color = discord.Colour.red())
        embed.add_field(name=f'New verified role',value =f'Student `{user}` now has the they/them pronoun!', inline = True)
        await user.send(embed=embed)
        return
        

@client.command(name="python", help="executes python script")
async def runpy(ctx, *,mystring):
    mystring = mystring[3:-3]

    code_str = mystring
    try:
        code = compile(code_str, 'main.py', 'exec')
    except:
        embed = discord.Embed(title = "Python Code Output", color = discord.Colour.red())
        embed.add_field(name=f'The python code has failed to compile.',value ="The python code must be in code blocks and must compile correctly in a python compiler.\nThe python code runs as an executable", inline = True)
        await ctx.send(embed=embed)

    print(code)
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        exec(code)

        sys.stdout = old_stdout

        embed = discord.Embed(title = "Python Code Output", color = discord.Colour.red())
        embed.add_field(name=f'The python code has compiled and ran successfully',value ="```"+mystdout.getvalue()+"```", inline = True)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title = "Python Code Output", color = discord.Colour.red())
        embed.add_field(name=f'The python code compiled but failed to run',value ="The python code must be in code blocks and must compile correctly in a python compiler.\nThe python code runs as an executable", inline = True)
        await ctx.send(embed=embed)


######################################################################
MAX_SIZE_COURSE = 6
database_user = [0] * 1000
question = [" "] * 1000
duplicateQ = {"null"}
duplicateS = {"CS2301.004", "MATH2414.017", "PHYS1301.002", "HIST1301.002", "CS1337.018"}
courses, homework_deadline, homework = [], [], []

#Getting the detail of homework and also exam, including deadline
def get_homework(cousesID):
    #Reading all the homeworks for each course
    #count = 0
    #while can read homework:
        #homework[courseID][count] = homework
        #deadline[courseID][count++] = deadline
    return


#Pretending that we can get access to blackboard and read the courses of the student
def get_courses():
    ##for i in range(MAX_SIZE_COURSE):
        #Reading all the courses in elearning
        #Calling get_homework(i)
    ##course, count = "", 0 
    return 5 #For simplification, we assume that we have 5 courses

#This is a hardcode courses. Assuming we can get access to elearning and blackboard collaborative, we get these hardcode courses below. This can be different for each student
courses = ["CS2301.004", "MATH2414.017", "PHYS1301.002", "HIST1301.002", "CS1337.018"]

homework_deadline = [["Mar 3rd, 2021, 11:59 PM", "Mar 5th, 2021, 11:59 PM"], ["Feb 28th, 2021, 11:59 PM", "Feb 28th, 2021, 11:59 PM", "Mar 5th, 2021, 11:59 PM"], ["Mar 2nd, 2021, 11:59 PM", "Mar 3rd, 2021, 11:59 PM"],["Mar 3rd, 2021, 11:59 PM", "Mar 5th, 2021, 11:59 PM"], ["Mar 2nd, 2021, 11:59 PM"]]

homework = [["Quiz 3: Chapter 3", "Homework Chapter 4"], ["Exam 1", "Homework Chapter 3", "Quiz 2"], ["Homework 3 Section 1", "Homework 3 Section 2"], ["Reading Chapter 5", "Reading Chapter 6"], ["Assignment 3: Insertion Sort"]]

@client.command()
async def remind(ctx):
    embed = discord.Embed(title="Assignment Deadlines:", description = None, color = discord.Colour.red())
    print(courses, homework, homework_deadline)
    for id in range(len(courses)):
        for index in range(len(homework[id])):
            embed.add_field(name=courses[id], value = homework[id][index] + ": " + homework_deadline[id][index], inline = False)
    await ctx.send(embed=embed)

@client.command()
async def new(ctx, *,newAssignment):
    if get(ctx.author.roles, name="professor") is not None:
        #newAssignment = ctx.content.split("!new.")[1]
        dotCount = 0
        subject = ""
        assignment_name = ""
        assignment_deadline = ""
        for i in range(len(newAssignment)):
            if(newAssignment[i] == '.'):
                dotCount += 1
            if dotCount < 2:
                subject += newAssignment[i]
            elif dotCount == 2 and newAssignment[i] != '.':
               assignment_name += newAssignment[i]
            elif dotCount > 2 and newAssignment[i] != '.':
                assignment_deadline += newAssignment[i]
        updateAssignment(subject, assignment_name, assignment_deadline)
        await ctx.author.send("Reminder succesfully added")
    else:
        await ctx.author.send("You do not have permission to do this!")

@client.command()
async def showQuestion(ctx):
    if len(duplicateQ) == 1:
        await ctx.channel.send("No questions have been asked yet!")
    else:
        embed = discord.Embed(title="All pending question(s):", description = None, color = discord.Colour.blue())
        for i in range(len(duplicateQ) - 1):
            embed.add_field(name = "Question " + str(i + 1) + ":", value = question[i], inline = False)
            # await message.channel.send("Question " + str(i + 1) + ": " + question[i] + "\n")
        await ctx.channel.send(embed=embed)

@client.command()
async def askQuestion(ctx, *,quest):
    amountQ = len(duplicateQ)-1
    print(amountQ)
    print(quest)
    print("enter ask function")
    if (quest in duplicateQ):
        await ctx.send("Question was already asked!")
    else:
        database_user[amountQ] = ctx.author.id #storing the student's id
        question[amountQ] = quest #storing the question
        duplicateQ.add(quest) 
        amountQ += 1
        await ctx.send("Question \"" + quest + "\" has successfully added!")
    print("exit")

@client.command()
async def answerQuestion(ctx,questionNumber,*,answer):
    if ((int(questionNumber)-1) > len(duplicateQ)):
        await ctx.send("There is no such question \"" + answer + "\" !")
    else:
        qFound = -1
        #for i in range(len(duplicateQ)):
        #    if question[i] == answer:
        #        qFound = i
        #        break
        #user = await client.fetch_user(database_user[qFound])
        await ctx.send("Your answer " + answer + "\nIs for Question "+ question[int(questionNumber)-1])
        await ctx.send("Your question has been answered!")
        duplicateQ.remove(question[int(questionNumber)-1])
        question.remove(question[int(questionNumber)-1])

def updateAssignment(subject, name, deadline):
    if subject not in duplicateS:
        duplicateS.add(subject)
        courses.append(subject)
        homeworkTemp, deadlineTemp = [],[]
        homeworkTemp.append(strModify(name))
        homework.append(homeworkTemp)
        deadlineTemp.append(timeFormat(deadline))
        homework_deadline.append(deadlineTemp)
    else:
        found = -1
        for i in range(len(courses)):
            if courses[i] == subject:
                found = i
                break
        homework[i].append(strModify(name))
        homework_deadline[i].append(timeFormat(deadline))

        
def strModify(string):
    modified_string = ""
    for i in range(len(string)):
        if string[i] == '_':
            modified_string += " "
        else:
            modified_string += string[i]
    return modified_string

def timeFormat(time):
    format = ""
    for i in range(len(time)):
        if time[i] == '_':
            format += " "
        elif time[i] == ',':
            format += ", "
        else:
            format += time[i]
    format += ", 11:59 PM"
    return format
#######################################################################
KEY='8XPQT7-TTTGAUGPVK'
GOOGLE_KEY='AIzaSyCkW9AsR_UYp-kX0JwXQFiiMFw4TOGvDy0'

@client.command(brief='this command does math')
async def math(ctx, *args):
    query = '%20'.join(args)
    split_query = list(query)
    for n, i in enumerate(split_query):
        if i == '+':
            split_query[n] = 'plus'
    query = ''.join(split_query)

    url = f"https://api.wolframalpha.com/v2/result?appid={KEY}&i={query}%3F"
    print(url)
    response = requests.get(url)

    embed = discord.Embed(
        title = 'Answer:',
        description = response.text,
        color = discord.Colour.dark_gold()
    )

    await ctx.send(embed=embed)


@client.command(aliases=['new_course'])
#role = string role : discord.role
async def create_course(ctx, channelName):
    guild = ctx.guild

    embed = discord.Embed(
        title = 'Course created',
        description = '{} has been successfully created'.format(channelName),
        color = discord.Colour.red()
    )
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_text_channel(name='{}'.format(channelName))
        await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Error: invalid command.')

client.run('ODE1MjQ5NDk2NTY4MTAyOTQ1.YDpqQg.RuEz3rpxT7QfsMqb9HSa2BF9WBM')

