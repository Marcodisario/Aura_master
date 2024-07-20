import discord
from discord.ext import commands
from discord import app_commands
from tabulate import tabulate
import os
from dotenv import load_dotenv
# Configura el prefijo que usarás para los comandos (por ejemplo, '!')


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()


aura_points = {}

@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión en Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Conectado a {len(bot.guilds)} servidor(es)')

    # Sincronizar comandos globalmente
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comando(s) global(es)")
    except Exception as e:
        print(f"Error al sincronizar comandos globales: {e}")

    # Opcional: Sincronizar comandos por servidor
    for guild in bot.guilds:
        general_channel =discord.utils.find(lambda x:x.name == 'general',guild.text_channels)
        if general_channel:
            await general_channel.send('¡Hola a todos! ¡Estoy en línea y listo para contar sus auras')
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"Sincronizado {len(synced)} comando(s) en el servidor: {guild.name} (ID: {guild.id})")
        except Exception as e:
            print(f"Error al sincronizar comandos en el servidor {guild.name} (ID: {guild.id}): {e}")

@bot.tree.command(name="ver_aura")
async def ver_aura(interaction: discord.Interaction):
    """Muestra la tabla de aura de todos los usuarios."""
    if not aura_points:
        await interaction.response.send_message("Aún no hay aura registrada en este servidor.")
        return
    
    table_data = [[user.name, points] for user_id, points in aura_points.items() if (user := interaction.guild.get_member(user_id))]
    table = tabulate(table_data, headers=["Usuario", "Aura"], tablefmt="grid")
    await interaction.response.send_message(f"```\n{table}\n```")

@bot.tree.command(name="mi_aura")
async def mi_aura(interaction: discord.Interaction):
    """Muestra tu aura."""
    user_id = interaction.user.id
    points = aura_points.get(user_id, 0)
    await interaction.response.send_message(f"{interaction.user.mention}, tienes {points} de aura.")

@bot.tree.command(name="sumar_aura")
@app_commands.describe(
    usuario="El usuario al que sumar aura (deja en blanco para sumarte a ti mismo)",
    cantidad="La cantidad de aura a sumar"
)
async def sumar_aura(interaction: discord.Interaction, usuario: discord.Member = None, cantidad: int = 1):
    """Suma aura a un usuario o a ti mismo."""
    target_user = usuario or interaction.user
    aura_points[target_user.id] = aura_points.get(target_user.id, 0) + cantidad
    await interaction.response.send_message(f"Se le sumo {cantidad} de aura a {target_user.mention}. Ahora tiene {aura_points[target_user.id]}.")

@bot.tree.command(name="restar_aura")
@app_commands.describe(
    usuario="El usuario al que restar aura (deja en blanco para restarte a ti mismo)",
    cantidad="La cantidad de aura a restar"
)
async def restar_aura(interaction: discord.Interaction, usuario: discord.Member = None, cantidad: int = 1):
    """Resta aura a un usuario o a ti mismo."""
    target_user = usuario or interaction.user
    current_points = aura_points.get(target_user.id, 0)
    aura_points[target_user.id] = current_points - cantidad
    await interaction.response.send_message(f"Se le resto {cantidad} de aura a {target_user.mention}. Ahora tiene {aura_points[target_user.id]}.")

@bot.tree.command(name="reset_aura")
@app_commands.describe(
    cantidad="La cantidad de aura a la que se reseteará (deja en blanco para resetear a 0)"
)
async def reset_aura(interaction: discord.Interaction, cantidad: int = 0):
    """Resetear el aura de todos los usuarios a 0 o a la cantidad especificada."""
    global aura_points
    aura_points = {user_id: cantidad for user_id in aura_points}
    await interaction.response.send_message(f"El aura de todos los usuarios ha sido reseteada a {cantidad}.")

@bot.tree.command(name="chichi")
async def chichi(interaction: discord.Interaction):
    await interaction.response.send_message(f'sisi, {interaction.user.mention},chichi es una rata!')

@bot.command()
async def chau(ctx):
    await ctx.send(f'Adios')

@bot.command()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send('Command tree synced.')

TOKEN= os.getenv('Token')

bot.run(TOKEN)
# Reemplaza 'TU_TOKEN_AQUI' con el token de tu bot