Perplexity is a search engine that uses AI to answer questions and provide insights into the latest trends and topics.

[API Documentation] (https://www.perplexity.ai/api/docs)

Example Curl:
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "sonar",
  "messages": [
    {
      "role": "system",
      "content": "Be precise and concise."
    },
    {
      "role": "user",
      "content": "How many stars are there in our galaxy?"
    }
  ],
  "max_tokens": 123,
  "temperature": 0.2,
  "top_p": 0.9,
  "search_domain_filter": null,
  "return_images": false,
  "return_related_questions": false,
  "search_recency_filter": "<string>",
  "top_k": 0,
  "stream": false,
  "presence_penalty": 0,
  "frequency_penalty": 1,
  "response_format": null
}'
```
