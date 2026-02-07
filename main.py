import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key returns None")

    client = genai.Client(api_key=api_key)

    # Allows user input for prompts
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
    )

    if response.usage_metadata is None:
        raise RuntimeError("failed API request")

    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
