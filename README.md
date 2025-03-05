# trend-pulse

## Overview

Trend Pulse is a tool that uses various AI models to analyze news and social media data to provide insights into the latest trends and topics.

We will use the following AI models:

- xAI        Grok-3
- Perplexity GPT-4o
- DeepSeek   3.5

The goal of this project is to provide a tool that can run and retrieve active trends and topics from the internet. Continuely store that data and crunch it to provide insights into the latest trends and topics.

As of 3/3/2025, no available tools to access the continuous data streams of the internet.

## journals of the journey


### 3/4/25
- I've come to realize Xai has given fake articles every single time which is suprising. What it has come up with is very unique and would be wild news if true. 
- I must come up with a way to get the most accurate news possible.
- Perplexity is most likely the answer and use xAI to then aggregate the results and give additional context ontop of the article. 
- Most likely will be perplexity api to get all of the legitimate news, python to wget the html from the site to get the full article, and xAI to aggregate the results and give additional context. 
- I wish to also put a classification on these articles