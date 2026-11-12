# Interview questions

[⬅ Troubleshooting](troubleshooting.md) · [Back to README](../README.md)

**1. What's the difference between entity recognition and PII detection?**
NER finds named things (people, places, organizations, dates) for analytics. PII detection targets personal data (names, emails, phone numbers, IDs) so it can be **redacted** for privacy and compliance, e.g. before storing reviews or sending text to other systems.

**2. Why detect language first?**
To route multilingual content: pick the right downstream model, translate, or apply language-specific rules. It's also a quality signal.

**3. Why connect Azure Language to an agent through MCP instead of calling the API directly?**
The agent interprets free-form requests and **chooses** the right analysis (entities, sentiment, redaction) itself. MCP is a standard interface, so the same tool works across agents and frameworks without custom glue code.

**4. Why did the Python client need auto-approval for the tool?**
Tool calls can require human approval. A non-interactive client can't approve, so the run stops with an approval request. For trusted, read-only tools you auto-approve; for risky actions you keep approval and build an approval flow.

**5. How do these apps authenticate, and why?**
`DefaultAzureCredential` (Entra ID via `az login` locally, managed identity in Azure). No keys in code; access is controlled with RBAC roles such as *Cognitive Services User*.

**6. How would you build a full voice assistant from lab 3?**
Speech-to-text (gpt-4o-mini-transcribe) → reasoning (an LLM or the lab 2 agent) → text-to-speech (gpt-4o-mini-tts). For low latency, stream audio and responses, or use a realtime/voice-live API.

**7. What's special about gpt-4o-mini-tts compared with classic TTS?**
You steer delivery with natural-language **instructions** (tone, emotion, pace), not only voice selection and SSML.

**8. How would you run the review pipeline at scale?**
Batch documents per request (the SDK accepts lists), process asynchronously from a queue, handle per-document errors, store only redacted text, and monitor cost and latency.

### 60-second pitch

> "I built three language AI capabilities on Microsoft Foundry. First, a review pipeline with Azure Language that detects language, extracts entities and redacts PII before anything is stored. Second, an agent connected to the Azure Language MCP server that chooses the right NLP tool on its own, called from a Python client. Third, voice in and out with gpt-4o-mini-tts and gpt-4o-mini-transcribe. Everything uses keyless Entra ID authentication. The pattern: specialized services for accuracy and compliance, LLM reasoning for flexibility."
