import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
import call_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key returns None")

    client = genai.Client(api_key=api_key)

    # Allows user input for prompts
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # Bool set to True if a final call is reached. Will throw an exit code 1 if set to False after final iteration
    got_final_call = False

    for _ in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[call_functions.available_functions], system_instruction=system_prompt
    ),
        )
        # Checks number of available model requests 
        if response.usage_metadata is None:
            raise RuntimeError("failed API request")
        # Checks for the verbose tag boolean
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # Records generated messages and requests of model for each iteration
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        
        # Checks if it's the final call
        if not response.function_calls:
            print(f"Final response:")
            print(response.text)
            got_final_call = True
            break

        if response.function_calls:
            function_responses = []
            for call in response.function_calls:
                result = call_functions.call_function(call, args.verbose)

                # Safety Checks: Ensure the result isn't empty at any level
                if (not result.parts or \
                    result.parts[0].function_response is None or \
                    result.parts[0].function_response.response is None):
                    raise Exception("Function call returned an empty or malformed response")
                else:
                    if args.verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    function_responses.append(result.parts[0])
            
            messages.append(types.Content(role="user", parts=function_responses))

    if got_final_call == False:
        print("Maximum iterations (20) reached without a final response")
        sys.exit(1)
        
        


if __name__ == "__main__":
    main()
