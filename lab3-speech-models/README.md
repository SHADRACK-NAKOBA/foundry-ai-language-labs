# Lab 3 · Generate and transcribe speech with gpt-4o-mini-tts and gpt-4o-mini-transcribe

[⬅ Lab 2](../lab2-text-analysis-agent/README.md) · [Next: Share your learnings ➡](../docs/share-your-learnings.md)

**Scenario:** you're an AI engineer at a customer support company building a voice assistant. It needs two building blocks: **text-to-speech** (the assistant speaks, with a chosen voice and tone) and **speech-to-text** (it understands what the caller says). You'll build both with speech-capable generative models in Microsoft Foundry and the OpenAI SDK, with Entra ID sign-in.

**Time:** ~40 min · **Folders:** `lab3-speech-models/generate-speech`, `lab3-speech-models/transcribe-speech`

> ⚠️ These models are available in a few regions only. Your project must be in **East US 2** ([setup](../docs/01-create-foundry-project.md)).

## 1. Deploy the two models

1. In the Foundry portal select **Discover** → **Models** (or **Find models** on the home page).
2. Search **gpt-4o-mini-tts** → open the model card → **Deploy** → keep defaults → **Deploy**.
3. Select **Build** → **Models** → **Deploy a base model** → search **gpt-4o-mini-transcribe** → **Deploy** with defaults.
4. ✅ **Build** → **Models** lists both deployments.
5. Open each deployment and copy its **Endpoint** / **Target URI**, and note the **deployment name**.

> The app needs only the start of the URI (`https://<resource>.openai.azure.com/` or `https://<resource>.cognitiveservices.azure.com/`). Paste the full Target URI if you like; the app trims it. A project URL (`…/api/projects/…`) is **not** the right value here.

## 2. Speech generation (text-to-speech)

### Configure

From the repo's top folder, with `(labenv)` active:

```powershell
cd lab3-speech-models\generate-speech     # macOS/Linux: cd lab3-speech-models/generate-speech
Copy-Item .env.example .env              # macOS/Linux: cp .env.example .env
```

Open **generate-speech/.env**:

```text
MODEL_ENDPOINT="https://<your-resource>.openai.azure.com/"
MODEL_NAME="gpt-4o-mini-tts"
```

`MODEL_NAME` is your **deployment** name. Save.

### Add the code

Open **generate-speech.py**.

**Under `# Import namespaces`** (no indentation):

```python
# Import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
```

**Under `        # Create the Azure OpenAI client`** (8 spaces):

```python
        # Create the Azure OpenAI client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2025-03-01-preview"
        )
```

**Under `        # Generate speech and save to file`** (8 spaces):

```python
        # Generate speech and save to file
        with client.audio.speech.with_streaming_response.create(
            model=model_deployment,
            voice="alloy",
            input="My voice is my passport!",
            instructions="Speak in a serious tone.",
        ) as response:
            response.stream_to_file(speech_file_path)
```

### Run

```powershell
python generate-speech.py
```

✅ `Speech saved to ...speech.mp3` and you hear *"My voice is my passport!"* in a serious tone.
No sound (e.g. on a VM without audio)? The app tells you, and you can open `speech.mp3` yourself.

Try it: change `voice` (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`), `input` and `instructions` (e.g. *"Speak cheerfully, like a sports commentator."*) and run again.

## 3. Speech transcription (speech-to-text)

### Configure

```powershell
cd ..\transcribe-speech                   # macOS/Linux: cd ../transcribe-speech
Copy-Item .env.example .env              # macOS/Linux: cp .env.example .env
```

Open **transcribe-speech/.env**:

```text
MODEL_ENDPOINT="https://<your-resource>.openai.azure.com/"
MODEL_NAME="gpt-4o-mini-transcribe"
```

Save. (Same environment as before; nothing new to install.)

### Add the code

Open **transcribe-speech.py**.

**Under `# Import namespaces`** (no indentation): the same two imports as above.

**Under `        # Create the Azure OpenAI client`** (8 spaces): the same client code as above.

**Under `        # Call model to transcribe audio file`** (8 spaces):

```python
        # Call model to transcribe audio file
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model_deployment,
                file=audio_file,
                response_format="text"
            )

        print(transcription)
```

### Run

```powershell
python transcribe-speech.py
```

✅ The app plays `speech.wav`, then prints its transcript.

Try it: record your own short `.wav` (e.g. with Windows **Sound Recorder**, saved as WAV or MP3), replace `speech.wav`, and run again.

📸 **Screenshot** both deployments in the portal and the transcript in the terminal.

Stuck? Compare with the `solution/` folder in each app, or run `python solution/generate-speech.py` / `python solution/transcribe-speech.py`.

## What you built

The two halves of a voice assistant: a model that **speaks** with a controllable voice and tone, and a model that **listens** and turns speech into text, both called keylessly with Entra ID. Put an LLM (or the agent from lab 2) between them and you have a full voice loop.

[Next: Share your learnings ➡](../docs/share-your-learnings.md)
