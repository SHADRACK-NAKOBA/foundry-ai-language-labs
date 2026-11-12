from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse
import os
import sys

# Import namespaces



# Folder of this app (works whether you run the starter or solution/ version)
APP_DIR = Path(__file__).resolve().parent
if APP_DIR.name == "solution":
    APP_DIR = APP_DIR.parent


def get_endpoint():
    """Read FOUNDRY_ENDPOINT and keep only https://<resource>.services.ai.azure.com"""
    load_dotenv(APP_DIR / ".env")
    value = os.getenv("FOUNDRY_ENDPOINT", "")
    if not value or "<" in value:
        sys.exit("FOUNDRY_ENDPOINT is not set. Copy .env.example to .env, paste your endpoint, save and run again.")
    parts = urlparse(value.strip())
    return f"{parts.scheme}://{parts.netloc}"


def main():
    try:
        # Clear the console
        os.system("cls" if os.name == "nt" else "clear")

        # Get Configuration Settings
        foundry_endpoint = get_endpoint()

        # Create client using endpoint
        # (8 spaces: inside main's try block)


        # Analyze each text file in the reviews folder
        reviews_folder = APP_DIR / "reviews"
        for file_name in sorted(os.listdir(reviews_folder)):
            # Read the file contents
            print("\n-------------\n" + file_name)
            text = open(reviews_folder / file_name, encoding="utf8").read()
            print("\n" + text)
            # Get language
            # (12 spaces: inside the for loop)


            # Get entities


            # Get PII


    except Exception as ex:
        print(f"\nError: {ex}")
        print("See docs/troubleshooting.md")


if __name__ == "__main__":
    main()
