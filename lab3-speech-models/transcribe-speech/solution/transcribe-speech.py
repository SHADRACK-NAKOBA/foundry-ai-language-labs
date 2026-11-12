import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


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
        file_path = APP_DIR / "speech.wav"

        # Play the speech file
        play(file_path)

        # Create the Azure OpenAI client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2025-03-01-preview"
        )

        # Call model to transcribe audio file
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model_deployment,
                file=audio_file,
                response_format="text"
            )

        print(transcription)

    except Exception as ex:
        print(f"\nError: {ex}")
        print("See docs/troubleshooting.md")


if __name__ == "__main__":
    main()
