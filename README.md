
![DALL·E 2023-11-19 13 57 02 - A pixel art style Twitter banner image in 3_1 aspect ratio, featuring a multitude of lightbulbs with the phrase 'thinksy app'  The image should showca copy](https://github.com/Thinksy-app/thinksy/assets/5726457/29039d35-3bc0-48bb-909f-248fad26f7f9)

# Thinksy - Self Hosted

This is the open source version of [Thinksy](http://thinksy.app), A Slack App that compiles a concise list of what you’ve worked on for your next daily standup, weekly update, or performance review.

If you're interested in purchasing the full self-hosted version of Thinksy that includes integrations like Asana, Google Drive, and GitHub, please contact calli@thinksy.app.

If you're looking for the cloud version of Thinksy it is available now at [thinksy.app](https://www.thinksy.app).

## Who is this for?
Software engineers, product managers, and engineering managers who need to quickly summarize work that has been accomplished in a given time period.

Normally this is done through manually searching through your Slack and documents but Thinksy helps do the search and summarization for you so you can get a quicks snapshop of what's been accomplished.

This can be useful for gathering standup notes, weekly updates, or even performance reviews.

## How does it work?
Thinksy will look at the messages you've sent in the chosen time frame and feed them into OpenAI to summarize the work you've accomplished.

## How to Install

### Requirements
- Your own [OpenAI API key](https://platform.openai.com/account/api-keys)
- Permissions to create [Slack App](https://api.slack.com/apps) in your workspace
- Docker

### 1️⃣ Create Slack App

You want to create your internal Slack App to be used for your workspace.

- Go to https://api.slack.com/apps and select "Create New App"
- Select "From an app manifest"
- Select the workspace where you'd like to create the app
- Paste the manifest from manifest.yml
- Go to **OAuth & Permissions** and get the user bot token
<img width="737" alt="SCR-20231128-skdp-2" src="https://github.com/Thinksy-app/thinksy/assets/5726457/ac4a7cf1-dab7-4257-a9de-d1a01ca53364">

- Go to **Basic Information** and create an App-Level Token
<img width="551" alt="SCR-20231128-skrf-2" src="https://github.com/Thinksy-app/thinksy/assets/5726457/77f62eeb-4b2e-4739-b081-ae58cc3953f6">
<img width="576" alt="SCR-20231128-sksn-2" src="https://github.com/Thinksy-app/thinksy/assets/5726457/f98c86be-9c03-405a-bf69-35898bef0c80">

- _Optional:_ Add the [Thinksy logo](https://github.com/Thinksy-app/thinksy/blob/main/thinksy-logo.png) as the app icon
<img width="720" alt="SCR-20231128-sloq-2" src="https://github.com/Thinksy-app/thinksy/assets/5726457/a6cc7e4e-4260-4be9-a26c-b758029fe6a2">


### 2️⃣ Prepare .env file
* Save the ``.env`` template [from here](https://github.com/Thinksy-app/thinksy/blob/main/.env-example)
* Add your slack bot token, slack app token, and relevant OpenAI info


### 3️⃣ Run Docker
Once you have your ``.env`` file prepared you can get this running!

Simply run this docker image with your updated `.env` file

```
docker pull entreeden/thinksy:v0.1
docker run --env-file .env entreeden/thinksy:v0.1
```


_Optional: You can also use the included `Dockerfile` if you'd like to deploy the app manually_


## Using Thinksy

Wahoo 👏 Now Thinksy is on your workspace, let's run it!

### 1. Select your parameters for who to review and for what time range.

<img width="578" alt="SCR-20231128-srqh-2" src="https://github.com/Thinksy-app/thinksy/assets/5726457/709096d8-d565-4875-af35-5837b336ff8e">


### 2. Voilà, your review is ready!

<img width="1008" alt="SCR-20231128-ssuy" src="https://github.com/Thinksy-app/thinksy/assets/5726457/9030dafd-8bad-4918-9acb-0153414727d0">


## Questions?

We're continuing to grow and iterate Thinsky every day 🚀 If you have any feedback please feel free to reach out our CTO eden@thinsky.app or CEO calli@thinksy.app. Godspeed!


## License

MIT License
