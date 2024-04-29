# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import requests
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


FOLDER = './Malas_palabras/'
MEMEFOLDER ='./Memes/'
EXT = "txt"

# Define the intents your bot will use
intents = discord.Intents.default()
intents.members = True  # Enable the member intents
intents.message_content = True #v2

client = commands.Bot(command_prefix='/', intents=intents)




@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')



@client.command(name='saludo')
async def saludo(ctx):
    message = "mmg digo glu glu comando"
    response = message
    await ctx.send(response)


   
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if buscar_malas_palabras(message.content):
        response = "No puedes decir eso amiguito"
        await message.delete()
        await message.channel.send(response)

    if message.content.lower() in ['saludo', 'klk']: 
        response = "Saludo mmg digo glu glu"
        await message.channel.send(response)
    
    if message.content.lower() in ['mmg', 'mmgv']: 
        response = "No puedes decir eso amiguito"
        await message.delete()
        await message.channel.send(response)
    
    if message.content == "!meme" and ("memes" in str(message.channel)):

        print(message.channel)
        # Check if the bot can send messages in the channel
        if message.guild and message.channel.permissions_for(message.guild.me).send_messages:
            # Open the image file in binary mode

            archivos = os.listdir(MEMEFOLDER) 
            imagen_de_turno = random.randint(0, len(archivos))
            meme = archivos[imagen_de_turno]

            with open(f'{MEMEFOLDER}{meme}', 'rb') as file:
                # Create a discord.File object from the image file
                image = discord.File(file)
                # Send the image to the channel
                await message.channel.send(file=image)

        else:
            await message.channel.send("I can't send messages in this channel.")
    
    if message.content == "obtener": 
        response = obtener_meme()
        print(response)
        await message.channel.send("Ejecutado")
        
    if message.content.startswith('!ban'):
        # Verificamos si el autor del mensaje tiene los permisos necesarios para banear
        if message.author.guild_permissions.ban_members:
            # Obtenemos la lista de menciones de usuarios mencionados en el mensaje
            mentions = message.mentions
            if len(mentions) == 0:
                await message.channel.send("Por favor, menciona al usuario que deseas banear.")
            else:
                for member in mentions:
                    await member.ban(reason="Razón no especificada.")
                    await message.channel.send(f'{member.mention} ha sido baneado.')
        else:
            await message.channel.send("No tienes los permisos necesarios para banear a usuarios.")


    "peticiones-de-baneo"        
            
def buscar_malas_palabras(palabra):

    with open(f'{FOLDER}malaspalabras.txt', 'r') as archivo:
        lineas = archivo.readlines()
        
    
    for linea in lineas:
        if palabra.lower() == linea.strip().lower():
            return True
    
    return False

#Esta funcion sirve para obtener memes
def obtener_meme():
    archivos = os.listdir(MEMEFOLDER)
    print(archivos)


def guardar_imagen(imagen,name):

    imagen = requests.get(imagen)
    name = name.replace(" ", "-")

    with open(f"{FOLDER}{name}.jpg",'wb') as archivo:
        # Escribe el contenido de la respuesta en el archivo
        archivo.write(imagen.content)
        
    print("Archivo descargado correctamente.")

def sayHello():
    print("hello")

client.run(TOKEN)
