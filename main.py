import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Check for command line arguments
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    sys.exit(1)

prompt = sys.argv[1]

# Create a list of messages for the conversation
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

# Generate content using the gemini-2.0-flash-001 model
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages
)

# Print the model's response
print(response.text)

# Print token usage
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
