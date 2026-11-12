from dotenv import load_dotenv
from pathlib import Path
import os
import sys

# Import namespaces



# Folder of this app (works whether you run the starter or solution/ version)
APP_DIR = Path(__file__).resolve().parent
if APP_DIR.name == "solution":
    APP_DIR = APP_DIR.parent


def main():
    try:
        # Clear the console
        os.system("cls" if os.name == "nt" else "clear")

        # Get Configuration Settings
        load_dotenv(APP_DIR / ".env")
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT", "")
        agent_name = os.getenv("AGENT_NAME", "Text-Analysis-Agent")
        if "<" in foundry_endpoint or "/api/projects/" not in foundry_endpoint:
            sys.exit("FOUNDRY_ENDPOINT must be your PROJECT endpoint (…/api/projects/<name>). Update .env, save and run again.")

        # Get project client
        # (8 spaces: inside main's try block)


        # Get an OpenAI client


        # Use the agent to get a response


    except Exception as ex:
        print(f"\nError: {ex}")
        print("See docs/troubleshooting.md")


if __name__ == "__main__":
    main()
