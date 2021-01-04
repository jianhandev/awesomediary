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

### Dialogflow Setup

- Carry out Dialogflow setup here <br>
  `https://cloud.google.com/dialogflow/es/docs/quick/setup`
- Generate a Google service account key
- Create a new agent by following only the steps under _**Create an agent**_ here <br>
  `https://cloud.google.com/dialogflow/es/docs/quick/build-agent`
- Zip the prebuilt agent files in `dialogflowagent` (excluding the parent folder itself)
- Restore the agent with the zipped file via the console
  - Visit `https://dialogflow.cloud.google.com/`
  - Select your created agent using the dropdown at the top left, under `Dialogflow Essentials`
  - Click on the gear icon beside the agent name
  - Click on the `Export and Import` tab
  - Click on `RESTORE FROM ZIP` and upload your zipped file
  - You should see a green success bar `Done` after your agent file has been uploaded
  - Once uploaded, click on the `Intents` section of the left panel. You should find all the intents already created for you e.g. those starting with `Ninja Cafe -...`


### Setup project on PyCharm

- Clone template project from git here: `git clone https://github.com/ninja-van/telegram-workshop-jan-2021.git`
- Copy Google service account key file (see Dialogflow setup) to project base directory
- In the terminal in PyCharm, do the following:
  - Create and activate virtual environment <br>
   `https://flask.palletsprojects.com/en/1.1.x/installation/#`
  - Install required dependencies <br>
	- Flask - `pip install Flask` <br>
	- Google Authentication - `pip install google.oauth` <br>
	- Dialogflow Client - `pip install google-cloud-dialogflow` <br>
	- Basic Caching Library - `pip install Flask-Caching` <br>
    - Telegram Client - `pip install pyTelegramBotAPI`

---

### Telegram Setup

- In Telegram, find the [BotFather](https://t.me/BotFather) and follow the steps for making a new bot

- Save your new bot's token somewhere safe

### Local Dev





### Running the Application
- In PyCharm, create a run configuration with the `main.py` file path
- Find the executable for ngrok which you installed, and expose your SNS port using ngrok e.g. `/path/to/ngrok http 5000`
  - ngrok will give you a HTTPS forwarding endpoint e.g. `Forwarding https://92955034edb1.ngrok.io -> http://localhost:5000`
  - Your webhook will therefore be registered at that ngrok endpoint + route you have setup e.g. `https://<YOUR_NGROK_FORWARDING_SUBDOMAIN>.ngrok.io/telegram/webhook`

- Link your Telegram bot to your webhook
  - Open a terminal (or command prompt on Windows)
  - Paste the following snippet, replacing the `<API_TOKEN>` with the saved API token for your Telegram bot, and `<WEBHOOK_URL>` with the ngrok url with route that you've configured in the previous step.
  - You should receive the following response `{"ok":true,"result":true,"description":"Webhook was set"}`

```
curl -L -X POST "https://api.telegram.org/bot<API_TOKEN>/setWebhook?url=<WEBHOOK_URL>"

e.g.
curl -L -X POST "https://api.telegram.org/bot1234567890:AAG2g-bIHq4_JDWSINaOrhDw1gf5L7rzniM/setWebhook?url=https://d6e3134b7be7.ngrok.io/telegram/webhook"
```

  - Test that your endpoint is returning a valid response for the webhook with the following 
```
curl -L -X POST "https://d6e3134b7be7.ngrok.io/telegram/webhook"
```