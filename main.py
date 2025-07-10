import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions
from functions.function_call import call_function
from config import MAX_ITERS

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

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Max iterations of {MAX_ITERS} was reached")
            sys.exit(1)
        
        try:
            end_response = generate_content(client, messages, opt_command)
            if end_response:
                print(end_response)
                break
        except Exception as e:
            print (f"Error in generate_content: {e}")

def generate_content(client, messages, opt_command):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        ),

    )
    if opt_command:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            content = candidate.content
            if content.parts:
                messages.append(content)

    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, opt_command)
        if (
            not function_call_result. parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call")
        if opt_command:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function response generated")
    
    messages.append(types.Content(parts=function_responses, role="tool"))




if __name__ == "__main__":
    main()
