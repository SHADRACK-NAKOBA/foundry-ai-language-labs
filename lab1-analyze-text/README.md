# Lab 1 · Analyze text with Azure Language

[⬅ Set up VS Code](../docs/02-setup-vscode.md) · [Next: Lab 2 ➡](../lab2-text-analysis-agent/README.md)

**Scenario:** you're an AI engineer at a digital travel agency. Hotel reviews arrive in many languages and sometimes contain customers' personal details. Before storing or publishing them, your app must **detect the language**, **extract entities** (places, organizations, dates…) and **find and redact PII** (names, emails, phone numbers).

You'll call **Azure Language in Foundry Tools** from Python with the `azure-ai-textanalytics` SDK and Entra ID sign-in (no keys).

**Time:** ~30 min · **Folder:** `lab1-analyze-text/text-analysis` (`reviews/` holds 5 sample reviews)

## 1. Configure the app

1. In the terminal (with `(labenv)` active), go to the lab folder:

   ```powershell
   cd lab1-analyze-text\text-analysis      # macOS/Linux: cd lab1-analyze-text/text-analysis
   Copy-Item .env.example .env             # macOS/Linux: cp .env.example .env
   ```

2. Open **text-analysis/.env** and paste your endpoint:

   ```text
   FOUNDRY_ENDPOINT="https://<your-resource>.services.ai.azure.com"
   ```

   Pasting the full **project endpoint** (ending in `/api/projects/...`) is fine too: the app keeps only the `https://<resource>.services.ai.azure.com` part the Language service needs.
3. **Ctrl+S** to save.

## 2. Connect to Azure Language

Open **text-analysis.py**. The loading of settings and reviews is already written. You add code under each comment. **Indentation matters**; each block says how much.

**Under `# Import namespaces`** (no indentation):

```python
# Import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
```

**Under `        # Create client using endpoint`** (8 spaces):

```python
        # Create client using endpoint
        credential = DefaultAzureCredential()
        ai_client = TextAnalyticsClient(endpoint=foundry_endpoint, credential=credential)
```

Save, then run:

```powershell
python text-analysis.py
```

✅ Each review's text is printed with no errors. (The client is created but not used yet.)

## 3. Detect the language

**Under `            # Get language`** (12 spaces: inside the `for` loop):

```python
            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print("\nLanguage: {}".format(detectedLanguage.primary_language.name))
```

Save and run `python text-analysis.py` again. ✅ Each review now shows a **Language:** line (e.g. *English*, *French*).

> Each review is sent in its own call. You could also send all reviews in one call (a list of documents); the response is always a list, which is why the code takes `[0]`.

## 4. Extract entities

**Under `            # Get entities`** (12 spaces):

```python
            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print("\t{} ({})".format(entity.text, entity.category))
```

Run again. ✅ You see entities such as `London (Location)`, `Buckingham Palace (Location)`, `3/2/2018 (DateTime)`.

## 5. Find and redact PII

**Under `            # Get PII`** (12 spaces):

```python
            # Get PII
            pii_result = ai_client.recognize_pii_entities(documents=[text])[0]
            pii_entities = pii_result.entities
            if len(pii_entities) > 0:
                print("\nPII Entities")
                for pii_entity in pii_entities:
                    print("\t{} ({})".format(pii_entity.text, pii_entity.category))
                print("Redacted Text:\n {}".format(pii_result.redacted_text))
```

Run again. ✅ For review 1 you'll see `alex@contoso.com (Email)` listed as PII, and a **Redacted Text** where it's replaced by `****************`.

📸 **Screenshot** one review's full output (language, entities, PII, redacted text).

Stuck? Compare with [`solution/text-analysis.py`](text-analysis/solution/text-analysis.py), or run it: `python solution/text-analysis.py`.

## What you built

A privacy-aware text pipeline: language detection for routing multilingual content, entity extraction for analytics, and PII redaction so personal data never reaches storage or publication.

[Next: Lab 2, Text analysis agent ➡](../lab2-text-analysis-agent/README.md)
