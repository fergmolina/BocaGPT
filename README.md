# BocaGPT :large_blue_circle::yellow_circle::large_blue_circle:
This is a bot called BocaGPT that will conduct the role of Manager of _Boca Juniors_ football team.

BocaGPT is live at Twitter in https://twitter.com/BocaGPT

![alt text](imgs/img1.png)

## :godmode: Functionality
At the moment, BocaGPT will perform the following tasks:
- Inform every day about the training plan for that weekday
- Communicate the starting 11 players on a matchday with the available (not sanctioned neither injured) players of the team
- Communicate also the bench players that will complete the team
- Answer fictional questions related with the real result of the match
- Answer a fictional question every day related with the team, training or the club

All this tasks will be communicated using Twitter. 

## :computer: How does BocaGPT work?
Two APIs and two scrapped sites are used to create the content of the bot:
- Scrape information from Transfermarkt for players (only available players and including the second team)
- Scrape information from FBREF for the past and following matches
- Using this scrapped context info, OpenAI API is used to create the bot result. This could be the starting 11 of the team, a training session or an answer to a journalist
- Twitter API is used then to tweet all the content created

## :rocket: Can I create my own bot for my team?
YES! It's too easy. To do that, you will need first to clone the repo and then install the requirmenets.txt. Then, you will need to change the env constants from the .env file:
* FIRST_TEAM_ROSTER = Transfermarkt link to the first team detailed info
* SECOND_TEAM_ROSTER = Transfermarkt link to the first team detailed info
* MATCHES = FBREF link to the team information
* TEAM_NAME = Name of the team that the bot will manage
* BOT_NAME = Name of the bot

After that, and also filling all the API Keys from OpenAI and Twitter, you can deploy the script and enjoy your own bot. 
Enjoy!
