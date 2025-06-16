# cogs/run.py
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import json
import random
import typing # Added for Optional type hinting
import base64
import io
import time

# Load API Key from the main config file
def get_api_key():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config.get('gemini_api_key')

GEMINI_API_KEY = get_api_key()

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def generate_with_gemini(self, prompt: str) -> str:
        """
        Helper function to call the Gemini API for text generation.
        Configuration is set for maximum creativity and output length.
        """
        if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("YOUR_"):
             return "Error: Gemini API Key is not configured. Please contact the bot owner."

        # Settings are maximized for creativity and detailed responses
        generation_config = {
            "temperature": 1.0,
            "topP": 0.95,
            "topK": 64,
            "maxOutputTokens": 8192, # Maximize output for complete code and search results
        }
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": generation_config}
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        try:
                            return data['candidates'][0]['content']['parts'][0]['text']
                        except (KeyError, IndexError):
                            print(f"Gemini API returned unexpected data: {data}")
                            return "The AI returned an unusual response. Please try again."
                    else:
                        error_text = await response.text()
                        print(f"Gemini API Error: {response.status} - {error_text}")
                        return f"Sorry, I couldn't get a response from the AI. (Error: {response.status})"
            except Exception as e:
                print(f"An exception occurred while calling Gemini API: {e}")
                return "An error occurred while trying to contact the AI service."

    async def generate_image_with_imagen(self, prompt: str) -> typing.Union[io.BytesIO, str]:
        """Helper function to call the Imagen API for image generation."""
        if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("YOUR_"):
            return "Error: API Key is not configured."

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={GEMINI_API_KEY}"
        payload = {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1}}
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        try:
                            image_bytes = base64.b64decode(data['predictions'][0]['bytesBase64Encoded'])
                            return io.BytesIO(image_bytes)
                        except (KeyError, IndexError):
                            print(f"Imagen API returned unexpected data: {data}")
                            return "The AI generated an invalid image response."
                    else:
                        error_text = await response.text()
                        print(f"Imagen API Error: {response.status} - {error_text}")
                        return f"Sorry, I couldn't generate an image. (Error: {response.status})"
            except Exception as e:
                print(f"An exception occurred while calling Imagen API: {e}")
                return "An error occurred while trying to contact the image generation service."

    # --- Commands ---

    @app_commands.command(name="roast", description="Roasts a specific member or just tells a general roast.")
    @app_commands.describe(member="The member you want to roast (optional).")
    async def roast(self, interaction: discord.Interaction, member: typing.Optional[discord.Member] = None):
        await interaction.response.defer()
        if member:
            prompt = f"Tell me a new, creative, and funny roast about a Discord user named {member.display_name}. It should be sarcastic and witty, but not genuinely mean or offensive. Keep it short."
        else:
            prompt = "Tell me a short, witty, and savage roast that is general purpose and could apply to anyone. Make it funny."
        roast_text = await self.generate_with_gemini(prompt)
        await interaction.followup.send(f"{member.mention if member else ''} {roast_text}")

    @app_commands.command(name="poem", description="Creates a unique, short poem about a given topic (or a random one).")
    @app_commands.describe(topic="The topic for the poem (optional).")
    async def poem(self, interaction: discord.Interaction, topic: typing.Optional[str] = None):
        await interaction.response.defer()
        styles = ["in a mysterious tone", "in a joyful style", "from a thoughtful point of view", "with a humorous twist", "in a dramatic narrative style"]
        random_style = random.choice(styles)
        
        if topic:
            prompt = f"Write a completely new and creative four-line poem about '{topic}' {random_style}. Take a unique perspective on it."
            poem_title = f"A Poem About: {topic.capitalize()}"
        else:
            prompt = f"Write a completely new and creative four-line poem about a random, interesting topic. The poem should be {random_style}."
            poem_title = "A Random Poem"
            
        poem_text = await self.generate_with_gemini(prompt)
        embed = discord.Embed(title=poem_title, description=poem_text, color=discord.Color.purple())
        embed.set_footer(text=f"Style: {random_style.replace('in a ', '').replace(' style', '').capitalize()}")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="motivate", description="Gives you a fresh motivational push on a specific topic (or in general).")
    @app_commands.describe(topic="What you need motivation for (optional, e.g., 'studying').")
    async def motivate(self, interaction: discord.Interaction, topic: typing.Optional[str] = None):
        await interaction.response.defer()
        tones = ["like a hype drill sergeant", "like a wise and calm mentor", "with a touch of sarcastic humor", "in a very enthusiastic way", "like a philosopher offering deep wisdom"]
        random_tone = random.choice(tones)

        if topic:
            prompt = f"Give me a short, powerful, and hype motivational message for someone who needs to start '{topic}'. Phrase it {random_tone}."
        else:
            prompt = f"Give me a short, powerful, and general motivational message. Phrase it {random_tone}."
            
        motivation_text = await self.generate_with_gemini(prompt)
        await interaction.followup.send(f"Hey {interaction.user.mention}! {motivation_text}")

    @app_commands.command(name="inspire", description="Fetches an AI-generated inspirational quote.")
    async def inspire(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://inspirobot.me/api?generate=true&t={int(time.time())}"
                async with session.get(url) as response:
                    if response.status == 200:
                        image_url = await response.text()
                        embed = discord.Embed(title="A Spark of Inspiration", color=discord.Color.teal())
                        embed.set_image(url=image_url)
                        embed.set_footer(text="Generated by inspirobot.me")
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send("Sorry, I couldn't get inspiration from InspiroBot right now.")
            except Exception as e:
                print(f"Inspirobot Error: {e}")
                await interaction.followup.send("An error occurred while contacting InspiroBot.")

    @app_commands.command(name="cointoss", description="Flips a coin for you.")
    async def cointoss(self, interaction: discord.Interaction):
        random.seed(int(time.time()))
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"The coin landed on... **{result}**!")

    @app_commands.command(name="wouldyourather", description="Presents you with a difficult choice.")
    async def wouldyourather(self, interaction: discord.Interaction):
        await interaction.response.defer()
        categories = ["absurd", "philosophical", "funny", "impossible", "food-related", "superpower-related"]
        creativity_boosters = ["Make it completely original.", "Think of a scenario no one has thought of before.", "Create a genuinely difficult dilemma."]
        prompt = f"Generate one single, interesting, and difficult 'Would you rather...?' question. The category is '{random.choice(categories)}'. {random.choice(creativity_boosters)} Just the question itself, no extra text."
        question = await self.generate_with_gemini(prompt)
        await interaction.followup.send(question)

    @app_commands.command(name="fact", description="Get a surprising fact about a specific or random topic.")
    @app_commands.describe(topic="The topic you want a fact about (optional).")
    async def fact(self, interaction: discord.Interaction, topic: typing.Optional[str] = None):
        await interaction.response.defer()
        angles = ["from a historical perspective", "related to science", "that is a common misconception", "that is bizarre", "focusing on a statistic", "related to its origin"]
        creativity_boosters = ["Avoid common knowledge.", "Find a detail that would surprise an expert.", "Give me a fact that sounds fake but is true.", "Tell me the most unexpected fact you can find."]
        
        if topic:
            prompt = f"Tell me one single, surprising fun fact about '{topic}' {random.choice(angles)}. {random.choice(creativity_boosters)} Keep it concise and start directly with the fact."
            fact_title = f"Fact About: {topic.capitalize()}"
        else:
            prompt = f"Tell me one single, surprising, and obscure fun fact about a completely random topic. {random.choice(creativity_boosters)} Start the response with 'Did you know...' and then the fact."
            fact_title = "A Random Fact"
        
        fact_text = await self.generate_with_gemini(prompt)
        embed = discord.Embed(title=fact_title, description=fact_text, color=discord.Color.blue())
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="imagine", description="Generates an image from a prompt using AI.")
    @app_commands.describe(prompt="A description of the image you want to create (at least 2 words).")
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        if len(prompt.split()) < 2:
            await interaction.response.send_message("Your prompt needs to be at least two words long.", ephemeral=True)
            return
            
        await interaction.response.defer(thinking=True)
        image_data = await self.generate_image_with_imagen(prompt)

        if isinstance(image_data, str):
            await interaction.followup.send(image_data)
        else:
            file = discord.File(fp=image_data, filename="image.png")
            embed = discord.Embed(title="Image Generated!", color=discord.Color.orange())
            embed.set_image(url="attachment://image.png")
            embed.set_footer(text=f"Prompt: {prompt}")
            await interaction.followup.send(embed=embed, file=file)

    @app_commands.command(name="search", description="Searches the web for up-to-date info on a topic, with sources.")
    @app_commands.describe(query="What you want to search for.")
    async def search(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer(thinking=True)
        prompt = f"""
        Please perform an up-to-date web search for the query: '{query}'.
        Synthesize the information from multiple reliable sources into a concise summary.
        **Important Rules:**
        1.  **Do not use Wikipedia as a source.** Prioritize official websites, respected news outlets, academic journals, and expert documentation.
        2.  At the end of your summary, you **MUST** list the primary source URLs you used. Format them clearly under a "Sources:" heading. The sources are mandatory.
        Present the information clearly and objectively.
        """
        search_result = await self.generate_with_gemini(prompt)
        embed = discord.Embed(title=f"Web Search Results for: {query}", description=search_result, color=discord.Color.green())
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
