import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    command_lst = ["--verbose"]

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
        contents=messages
    )
    if opt_command:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
