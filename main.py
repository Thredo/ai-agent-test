import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from prompts import system_prompt

def main():
    load_dotenv()

    #Variables
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    command_lst = ["--verbose"]
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    args = [m for m in sys.argv[1:] if m not in command_lst]
    opt_command = False

    if("--verbose" in sys.argv):
        opt_command = True

    if not args:
        print("Escribile algo al coso nabo de mierda")
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
    if opt_command:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")


if __name__ == "__main__":
    main()
