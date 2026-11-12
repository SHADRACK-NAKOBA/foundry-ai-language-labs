from dotenv import load_dotenv
from pathlib import Path
import os
import sys

# Import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


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
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )

        # Get an OpenAI client
        openai_client = project_client.get_openai_client()

        # Use the agent to get a response
        prompt = input("User prompt: ")
        response = openai_client.responses.create(
            input=[{"role": "user", "content": prompt}],
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )

        approvals = [item for item in response.output if item.type == "mcp_approval_request"]
        if approvals:
            print("The agent is waiting for tool approval. In the portal set the Azure Language tool to "
                  "'Always auto-approve all tools', save the agent and run again (lab 2, step 4).")
        else:
            print(f"{agent_name}: {response.output_text}")

        # Show response details
        print(f"\nResponse Details: {response.model_dump_json(indent=2)}")

    except Exception as ex:
        print(f"\nError: {ex}")
        print("See docs/troubleshooting.md")


if __name__ == "__main__":
    main()
