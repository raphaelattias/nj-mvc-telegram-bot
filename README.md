# NJ MVC Telegram Bot
Automated bot sending you the location of the earliest available slot for New Jersey DMV / MVC.

# Installation
## Setting-up the environnement  
1. Clone this repository and open a terminal in this directory.
2. In the terminal, type 
```
conda env create -f environment.yml -n dmv
conda activate dmv
```
## Setting-up the telegram bot
To use the code, you will need to create a telegram bot. Your personal bot will have a *token*. Your own personal telegram account can be identified with an unique *userid*. You will need both the token and userid to send the notification.

It takes 5 min to create a bot for telegram. I recommend [this tutorial](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot) to create a bot and get its token. To get your userid, I recommend [this tutorial](https://bigone.zendesk.com/hc/en-us/articles/360008014894-How-to-get-the-Telegram-user-ID-). 
# Usage
After setting-up the environment, simply run
```
python run.py
````
You will be prompted for your token, userid, and the kind of test you are trying to get. 

### Adding arguments
You can also run the code with arguments

```
python run.py --token YOURTOKEN --user YOURUSERID --permit knowledge
```

### Get help
You can see examples and additional informations on the argument by running
```
python run.py -help
```

### Example
<img src="https://i.imgur.com/ZO5ERPe.jpg" alt="drawing" width="200"/>
