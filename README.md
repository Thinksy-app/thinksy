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

### 2️⃣ Prepare .env file
* Save the ``.env`` template from here
* Add your slack bot token, slack app token, and relevant OpenAI info


### 3️⃣ Run Docker
Once you have your ``.env`` file prepared you can get this running!

Simply run this docker image with your updated `.env` file

```
docker run --env-file .env my_image
```


_Optional: You can also use the included `Dockerfile` if you'd like to deploy the app manually_


## Using Thinksy








## License

MIT License