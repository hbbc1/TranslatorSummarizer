import praw
from newspaper import Article
from transformers import MarianMTModel, MarianTokenizer
import openai
import torch

#Provide Reddit API information
reddit = praw.Reddit(
    client_id='ENTER-CLIENT-ID',
    client_secret='ENTER-CLIENT-SECRET',
    user_agent='ENTER-USER-AGENT',
)

# Scrape Reddit post by URL
def scrape_reddit(url):
    submission = reddit.submission(url=url)
    post = reddit.submission(id=submission)
    text = post.selftext
    return text

# Scrape news article by URL
def scrape_news(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except ArticleException:
        return None


# Main loop takes URL as input and determines whether URL is Reddit or not and scrapes it appropriately
while True:
    url = input("Enter the URL you want to scrape (or 'q' to quit): ")
    if url == 'q':
        break

    if "reddit.com" in url:
        # Scrape Reddit post
        text = scrape_reddit(url)
        if text:
            #print(text)
            break
    else:
        # Scrape news article
        text = scrape_news(url)
        if text is not None:
            break

    # If no relevant scraper found or failed to scrape, print an error message
    print("Unable to scrape the provided URL.")

#Define Language Model
model_name = "Helsinki-NLP/opus-mt-ar-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
tokenizer.src_lang = "ar"
tokenizer.tgt_lang = "en"  # Set the target language to English
max_sequence_length = 100  # Maximum sequence length for the model

# Chunk the input text into smaller segments
chunked_text = [text[i:i+max_sequence_length] for i in range(0, len(text), max_sequence_length)]

translated_text = ""

for chunk in chunked_text:
  encoded_inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)

  generation_params = {
            "max_length": max_sequence_length,
            "do_sample": True,
            "temperature": 1.2,  # Adjust the temperature value as needed
            "num_beams": 4,  # Change the value of num_beams as desired
        }

        # Generate translations
  with torch.no_grad():
    generated_tokens = model.generate(**encoded_inputs, **generation_params)

  if generated_tokens.shape[1] == 0:
    print("No translation generated for:", file)
    continue

  chunk_translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
  translated_text += chunk_translated_text

#Summarize text
def summarize_text(text, max_length=300):
    # Generate a summary using the GPT-3 model
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=max_length,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Retrieve the generated summary from the API response
    summary = response.choices[0].text.strip()

    return summary

#Enter open.ai API information
openai.api_key = "ENTER-KEY-HERE"
summary = summarize_text(translated_text, max_length=150)
print(summary)
