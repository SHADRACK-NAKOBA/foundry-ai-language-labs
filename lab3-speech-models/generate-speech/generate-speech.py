import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces



# Folder of this app (works whether you run the starter or solution/ version)
APP_DIR = Path(__file__).resolve().parent
if APP_DIR.name == "solution":
    APP_DIR = APP_DIR.parent


def get_settings():
    """Read .env. Keep only https://<host> from the endpoint, since a full Target URI breaks the client."""
    load_dotenv(APP_DIR / ".env")
    value = os.getenv("MODEL_ENDPOINT", "")
    model = os.getenv("MODEL_NAME", "")
    if not value or "<" in value:
        sys.exit("MODEL_ENDPOINT is not set. Copy .env.example to .env, paste your endpoint, save and run again.")
    parts = urlparse(value.strip())
    return f"{parts.scheme}://{parts.netloc}/", model


def play(path):
    """Play audio if this machine has sound; otherwise just say where the file is."""
    try:
        playsound(str(path))
    except Exception as ex:
        print(f"\n(Could not play audio on this machine: {ex}. Open the file yourself: {path})")


def main():
    try:
        # Clear the console
        os.system("cls" if os.name == "nt" else "clear")

        # Get Configuration Settings
        endpoint, model_deployment = get_settings()
        speech_file_path = APP_DIR / "speech.mp3"

        # Create the Azure OpenAI client
        # (8 spaces: inside main's try block)


        # Generate speech and save to file


        # Play the generated speech file
        print(f"Speech saved to {speech_file_path}")
        play(speech_file_path)

    except Exception as ex:
        print(f"\nError: {ex}")
        print("See docs/troubleshooting.md")


if __name__ == "__main__":
    main()
