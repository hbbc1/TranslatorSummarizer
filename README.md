This repository contains a Python script for translating text from Arabic to English using the Helsinki-NLP Opus-MT model, and generating a summary of the translated text using the OpenAI GPT-3 language model.

## Installation

To run the code locally, please ensure that you have the following dependencies installed:

- `openai_secret_manager`
- `openai`
- `transformers`
- `sentencepiece`
- `sacremoses`
- `newspaper3k`
- `praw`

You can install these dependencies by running the following command:

```shell
pip install -r requirements.txt
```

## Usage

Obtain API Credentials:

OpenAI API Key: To use the GPT-3 model for summarization, you need to obtain an API key from OpenAI. You can sign up for an API key at OpenAI's website.

Reddit API Credentials: If you plan to scrape Reddit posts, you'll need to create a Reddit application and obtain a client ID, client secret, and user agent. You can create a Reddit application by following the instructions in the Reddit API documentation.

Update the Configuration:

Open the main.py file and replace the placeholder values with your API credentials. Look for the comments that indicate where you should insert your credentials.

The script will prompt you to enter the URL of the text you want to translate and summarize. You can provide a Reddit post URL or a news article URL.

The script will scrape the text from the provided URL, translate it from Arabic to English using the Opus-MT model, and generate a summary using the GPT-3 model.

The translated text and summary will be displayed in the console output.

## License

This project is licensed under the MIT License.
