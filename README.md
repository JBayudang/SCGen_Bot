# <div align="center">SCGen Bot</div>
###### <div align="center">[Terms of Service](https://soulcalibre.allabout-anything.com/p/scgen-bot-tos.html) | [Privacy Policy](https://soulcalibre.allabout-anything.com/p/scgen-bot-privacy-policy.html)</div>
# <div align="center">![SCGen Bot](https://github.com/user-attachments/assets/638b4aae-5991-4db0-902b-6f10b0d18bb7)</div>

### SCGen Bot is an All-Around Discord Server Bot (ADSB). Your All-in-One AI Companion for Creativity, Search &amp; Fun.
Unleash the full power of Google's latest AI models directly in your Discord server with SCGen Bot, the ultimate All-Around Discord Server Bot (ADSB). Whether you need instant, up-to-date information, a creative spark, a stunning image, or just a good laugh, SCGen Bot delivers.

Powered by Gemini 1.5 for text and Imagen for image generation, SCGen Bot is more than just a utility—it's your creative partner and information expert, all wrapped into one easy-to-use package with simple slash commands.

### What Makes SCGen Bot Special?
* **Cutting-Edge AI**: Get high-quality, creative, and unique responses every time. We've maximized the API settings to ensure the bot is always imaginative and never repetitive.
* **Versatile & Powerful**: From generating images and searching the web to writing poems and providing surprising facts, SCGen Bot is the only general-purpose bot you'll need.
* **User-Friendly**: All commands are intuitive slash commands. Many commands feature optional arguments, giving you full control—get a random fact, or a fact about a specific topic!
* **Privacy-Focused**: We do not log or store any of your command inputs or server data. Your conversations are yours alone.
* **Minimal Permissions**: SCGen Bot only asks for the permissions it absolutely needs to function, ensuring your server remains secure.

### Core Commands:
* _**/search [query]**_: Get a concise summary on any topic from reliable web sources (Wikipedia excluded), complete with a list of references.
* _**/imagine [prompt]**_: Bring your ideas to life! Generate a high-quality, unique image directly from your text description.
* _**/fact [topic]**_: Learn something new! Get a surprising and little-known fact about a specific topic, or a completely random one if you leave it blank.
* _**/poem [topic]**_: Need a creative boost? Get a unique, AI-generated poem in a random style about any topic, or let the bot surprise you.
* _**/motivate [topic]**_: Feeling stuck? Get a powerful motivational message in a random tone to get you going.
* _**/wouldyourather**_: Spark a fun debate with a mind-bending "Would you rather...?" question.
* _**/roast [member]**_: Engage in some friendly fire with a witty, AI-generated roast for a server member or a general audience.
* _**/inspire**_: Get a dose of quirky, AI-generated visual inspiration from the legendary InspiroBot.
* _**/cointoss**_: Make a quick decision with a simple coin flip.

Ready to upgrade your server? Add SCGen Bot today and discover what's possible when you put the world's most advanced AI at your community's fingertips!

### Deployment on Debian VPS:
![image](https://github.com/user-attachments/assets/b62d5282-a9d3-40ab-892d-ab117a776828)

#### Create the Project Directory
On your VPS, create a directory for your bot.
* `mkdir /root/SCGen_Bot`
* `cd /root/SCGen_Bot`
#### Set Up the Virtual Environment
* `python3 -m venv venv`
* `source venv/bin/activate`
#### Upload Your Bot Files
* Using **scp** or an SFTP client, upload the `bot.py`, `config.json`, `requirements.txt`, and the `cogs` directory to the `/root/SCGen_Bot` directory on your VPS.
#### Install Dependencies
* `pip install -r requirements.txt`
#### Configure Your Bot
* Ensure your `config.json` file is filled out with your **Discord Bot Token**, **Discord User ID**, and **Gemini API Key**.
#### Create the `systemd` Service
* `sudo nano /etc/systemd/system/scgen_bot.service`
##### Paste the following content, which uses the new name and paths: [scgen_bot.service.txt](https://pastebin.com/NPJNZqAn)
#### Enable and Start the New Service
* `sudo systemctl enable scgen_bot.service`
* `sudo systemctl start scgen_bot.service`
#### Check the Status
* `sudo systemctl status scgen_bot.service`
* `sudo journalctl -u scgen_bot.service -f`
##### Remember to **restart the service** (`sudo systemctl restart scgen_bot.service`) after you upload the new `fun.py` file to apply all these changes.
