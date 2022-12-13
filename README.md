# DiscordMinecraft
Remote Minecraft Service from Discord, using Idcloudhost Server, Idcloudhost API and Linux systemd for minecraft server

Bot for remoting Minecraft Server (systemd) from discord using Python3.
All you need to do is copy the .env_example to .env and change the value using yours.
The server is need to be specific using [Idcloudhost Provider](https://idcloudhost.com/cloud-vps/), if you want to change provider, feel free to edit the URL on utils/APIConnection.py

So, How it's work:
(Discord.py) -> ([Idcloudhost API](https://api.idcloudhost.com/) for Managing a Cloud - Start, Stop, CheckStatus, etc) -> (SSH into the Machine for executing linux custom service like 
"sudo service kuromine start", etc).

That's it. just a personal use right now, if you interesting in this repository, feel free to fork it or having a pizza while watching netflix, whatever.
