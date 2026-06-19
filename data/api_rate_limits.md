# API Rate Limits

Default API limits:

- 100 requests per minute
- 10,000 requests per day

Exceeding limits returns:

HTTP 429 Too Many Requests

Recommended:

- Implement retry logic
- Use exponential backoff