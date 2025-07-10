import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions
from functions.function_call import call_function

def main():
    load_dotenv()

    #Variables
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    command_lst = ["--verbose"]

    args = [m for m in sys.argv[1:] if m not in command_lst]
    opt_command = False

    if("--verbose" in sys.argv):
        opt_command = True

    if not args:
        print("please write something to the ai")
        sys.exit(1)

    user_prompt= " ".join(args)

    messages = [
        types.Content(parts=[types.Part(text=user_prompt)], role="user")
    ]


    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        ),

    )

    if not response.function_calls:
        print("Please make sure the file exists or its a valid function")
        return

    function_call_result = call_function(response.function_calls[0],opt_command)

    if not function_call_result.parts[0].function_response.response:
        print("Error: Fatal error")
        return

    if opt_command:
        print(f"-> {function_call_result.parts[0].function_response.response}")
        return



if __name__ == "__main__":
    main()
