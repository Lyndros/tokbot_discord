# Tokugawa coin discord channel bot installation instructions
A beautiful channel discord bot that allows you to retrieve interesting information.

## 1. Requirements

In order to run this program the following python3 and the following libraries need to be installed:
```
$sudo apt-get install python3-pip python3-yaml
$sudo pip3 install -U discord.py
$sudo pip3 install coinmarketcap
```
## 2. Copying the necessary files
```
$mkdir -p /opt/tokbot_discord/
$cd /opt/tokbot_discord/
$wget https://raw.githubusercontent.com/Lyndros/tokbot_discord/master/tokbot_discord.py
```
-- These are configuration examples, you need to customize them --
```
$wget https://raw.githubusercontent.com/Lyndros/tokbot_discord/master/config/tokugawa_bot.yml
```
## 3. Setting your configuration file

Edit the configuration file and modify as needed; coin parameters, masternodes addresses, etc...
If the coin explorer base url is not known by you contact the coin developer.
In the Discord section add your API key (check how to create a key <a href="https://discordpy.readthedocs.io/en/rewrite/discord.html">here</a>).

## 4. Executing the script
``` 
$python3 tokbot_discord.py /your_path/your_configuration.yml & 
```

## 5. Optional starting the bot automatically at boot
If you want to automatically start your bot at boot consider to add them to systemctl.
You can check the predefine service available in: https://github.com/Lyndros/tokbot_discord/tree/master/service/.

Please before enabling edit the file as needed, to update the location, user, etc..

i.e: Adding tokugawa bot service,
```
$cd /etc/systemd/system/
$wget https://raw.githubusercontent.com/Lyndros/tokbot_discord/master/service/tokugawa_bot.service
$systemctl enable tokugawa_bot.service
```

## 6. Chatting with your bot
In order to chat with your bot just open a chat or a channel where your bot is present and type 
"/bot help" in order to see the available commands.

## 7. Donations
If you want o support this repository I accept donations even the smalles portion of ETH is always welcome :-)!

- <b>ethereum address:</b> <i>0x44F102616C8e19fF3FED10c0b05B3d23595211ce</i>

For any questions feel free to contact me at <i>lyndros at hotmail.com</i>
