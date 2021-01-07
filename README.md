# Ninja Cafe Chatbot

A basic backend application for a Telegram chatbot integrated with Dialogflow. 
Contains a single route to handle Telegram webhooks (updates).

---

#### Prerequisites

- Install [PyCharm](https://www.jetbrains.com/pycharm/download)
  - On Mac, if you have `brew` you may use `brew cask install pycharm-ce`
- Install [python3](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/)
- Install [ngrok](https://ngrok.com/download) to tunnel requests to your local machine
- Install [Postman](https://www.postman.com/downloads/) to make API requests e.g. setting Telegram webhooks
- Install git



### Setup project on PyCharm

- Clone template project from git here: `git clone https://github.com/ninja-van/telegram-workshop-jan-2021.git`
- Copy Google service account key file (see Dialogflow setup) to project base directory
- Open template folder in PyCharm
  - ![1](assets/1.png?raw=true)
    - Click open
  

  - ![2](assets/2.png?raw=true)
    - Select folder that was cloned in git and click open
    

- Set up virtual environment in PyCharm
  - ![3](assets/3.png?raw=true)
    - Open `preferences`
    

  - ![4](assets/4.png?raw=true)
    - Go to `Project: telegram-workshop-jan-2021 in left side bar`
    

  - ![5](assets/5.png?raw=true)
    - Choose `Python Interpreter` and choose `Show All...`
    

  - ![6](assets/6.png?raw=true)
    - Click `+` and choose `Add`
  

  - ![7](assets/7.png?raw=true)
    - Ensure `New environment` is selected and ensure `Location` of environment is the `venv` subfolder in your project folder
  

  - ![8](assets/8.png?raw=true)
    - Click `OK`
  

  - ![9](assets/9.png?raw=true)
    - Go to the `Terminal` tab at the bottom toolbar and type in `pip install -r requirements.txt`
    - Note that you do not need to do this if you have the `requirements plugin` 
  
---

### Telegram Setup

- In Telegram, find the [BotFather](https://t.me/BotFather) and follow the steps for making a new bot

- Type the command `/newbot` 

- You will be prompted to enter a name for your bot. Please fill in a valid bot name (usually should end with a `bot` keyword)

- You will be given a token to access telegram APIs. Please populate this token for the variable `TELEGRAM_API_TOKEN` in the `constants.py` file in the code.


### Dialogflow Setup

- You do not need to do any Dialogflow setup as we have already done it for you and placed the credentials in the repository.


### Local Dev





### Running the Application
- In PyCharm, create a run configuration with the `main.py` file path
- Find the executable for ngrok which you installed, and expose your SNS port using ngrok e.g. `/path/to/ngrok http 5000`
  - ngrok will give you a HTTPS forwarding endpoint e.g. `Forwarding https://92955034edb1.ngrok.io -> http://localhost:5000`
  - Your webhook will therefore be registered at that ngrok endpoint + route you have setup e.g. `https://<YOUR_NGROK_FORWARDING_SUBDOMAIN>.ngrok.io/webhook`

- Link your Telegram bot to your webhook
  - Open a terminal (or command prompt on Windows)
  - Paste the following snippet, replacing the `<API_TOKEN>` with the saved API token for your Telegram bot, and `<WEBHOOK_URL>` with the ngrok url with route that you've configured in the previous step.
  - You should receive the following response `{"ok":true,"result":true,"description":"Webhook was set"}`

```
curl -L -X POST "https://api.telegram.org/bot<API_TOKEN>/setWebhook?url=<WEBHOOK_URL>"

e.g.
curl -L -X POST "https://api.telegram.org/bot1234567890:AAG2g-bIHq4_JDWSINaOrhDw1gf5L7rzniM/setWebhook?url=https://d6e3134b7be7.ngrok.io/webhook"
```

  - Test that your endpoint is returning a valid response for the webhook with the following 
```
curl -L -X POST "https://d6e3134b7be7.ngrok.io/webhook"
```