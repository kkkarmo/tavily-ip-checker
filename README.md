# Tavily IP Checker

This script checks a list of IP addresses against the Tavily API for malicious or suspicious activity.

## Usage
## Setup

1. Create a `.env` file in the project root with your Tavily API key:
2. Build the Docker image:
docker build -t tavily-ip-checker .
text

3. Run the container:
docker run --env-file .env tavily-ip-checker
text

For production use or when sharing the Docker image, you would still pass the API key as an environment variable when running the container:


docker run -e TAVILY_API_KEY=your_api_key tavily-ip-checker
text

This approach allows for flexibility in how you manage the API key, whether through a .env file for local development or environment variables for production deployment.
# tavily-ip-checker
