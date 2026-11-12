# Lab 2 · Build a text analysis agent with the Azure Language MCP tool

[⬅ Lab 1](../lab1-analyze-text/README.md) · [Next: Lab 3 ➡](../lab3-speech-models/README.md)

**Scenario:** you're an AI engineer at a travel technology company building a customer support assistant. Instead of hard-coding API calls, you give an **AI agent** the **Azure Language MCP server** as a tool. The agent understands the request and **chooses the right analysis itself**: entities, sentiment, language, PII.

**Time:** ~45 min · **Folder:** `lab2-text-analysis-agent/text-agent`

## 1. Create the agent

1. In the Foundry portal (your `prince-language-project`), select **Build** → **Agents** (or **Create agents** on the home page).
2. Create an agent named exactly:

   ```text
   Text-Analysis-Agent
   ```

3. In the playground, check the **model** drop-down shows a deployed model (e.g. **gpt-5** or gpt-4.1-mini). If it's empty, select a model and **Deploy** it with default settings.
4. **Instructions**:

   ```text
   You are an AI agent that assists users by helping them analyze text.
   ```

5. Select **Save**. Test in the **Chat** pane:

   ```text
   What can you help me with?
   ```

   ✅ The agent describes what it can do.

## 2. Connect the Azure Language tool (MCP)

1. In the left menu, select **Tools**, then the **Tools** tab → **Connect a tool**.
2. In the **Catalog**, select **Azure Language in Foundry Tools** and fill in:

   | Field | Value |
   |---|---|
   | **Name** | `prince-language-tool` |
   | **Remote MCP Server endpoint** | `https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview` |
   | **Parameters → foundry-resource-name** | your **Foundry resource name** (from [setup](../docs/01-create-foundry-project.md#write-down-three-values)), e.g. `prince-language-project-resource` |
   | **Authentication** | **Key-based** |
   | **Ocp-Apim-Subscription-Key** | your project **API key** |

   > If key-based auth is blocked by policy in your subscription, choose **Microsoft Entra ID** authentication instead.

3. Select **Connect** and wait for the connection to be created; its details page opens.
4. On the details page select **Use in an agent** → **Text-Analysis-Agent**.
5. The agent opens in the playground. ✅ Under **Tools**, **Azure Language in Foundry Tools** is listed.
   Not listed? Select **Add** under Tools and add it manually.

## 3. Test the tool in the playground

1. Update the **Instructions** and **Save**:

   ```text
   You are an AI agent that assists users by helping them analyze text. Use the Azure Language tool to perform text analysis tasks.
   ```

2. In **Chat**, send:

   ```text
   Identify the PII entities in this article, and generate a redacted version:

   Microsoft was founded on April 4, 1975, by childhood friends Bill Gates (then 19) and Paul Allen (22) after they were inspired by the Altair 8800, one of the first personal computers, featured on the cover of Popular Electronics. They contacted the Altair's maker, MITS, and successfully developed a version of the BASIC programming language, despite initially not owning the machine themselves. The pair formed a partnership called "Micro-Soft" in Albuquerque, New Mexico, close to MITS's headquarters, with the goal of writing software for emerging microcomputers.

   In the late 1970s, Microsoft grew by supplying programming languages to multiple hardware vendors, then relocated to the Seattle area in 1979. A pivotal moment came in 1980 when Microsoft partnered with IBM to provide an operating system for the IBM PC, leading to MS-DOS and establishing the company's dominance in personal computing. Gates guided the company's long-term strategy as CEO, while Allen contributed key technical vision in its early years, setting Microsoft on a path that would reshape the software industry.
   ```

3. When asked, select **Always approve all Azure Language in Foundry Tools tools**. You may be asked twice (two tasks: identify PII, then redact).
   > A **403**, **502** or other error right after approving is usually temporary: refresh the page and send the same prompt again.
4. ✅ The answer lists PII (names, ages, dates…) and a redacted version of the article.
5. Open the chat **Logs** and confirm the **Azure Language** tool was called.

## 4. Set tool approval to automatic (required for the Python app)

Your Python app can't click "Approve", so the agent must not wait for approval.

1. In the playground, under **Tools**, open the **⋯** menu of the Azure Language tool → **Configure**.
2. **Approval setting for tools in this MCP server for this agent** → **Always auto-approve all tools**.
3. **Save** the agent.

> Skipping this is the #1 reason the app prints no answer. The app detects it and tells you.

## 5. Configure the client app

1. In the VS Code terminal (`(labenv)` active), from the repo's top folder:

   ```powershell
   cd lab2-text-analysis-agent\text-agent   # macOS/Linux: cd lab2-text-analysis-agent/text-agent
   Copy-Item .env.example .env             # macOS/Linux: cp .env.example .env
   ```

   (Coming from lab 1? First `cd ..\..` to the top folder.)
2. Open **text-agent/.env**:

   ```text
   FOUNDRY_ENDPOINT="https://<your-resource>.services.ai.azure.com/api/projects/prince-language-project"
   AGENT_NAME="Text-Analysis-Agent"
   ```

   Here you need the **full project endpoint** (with `/api/projects/...`). `AGENT_NAME` is **case-sensitive**.
3. **Ctrl+S**.

## 6. Add the code

Open **text-agent.py** and add under each comment (8 spaces: inside `main`'s `try`).

**Under `# Import namespaces`** (no indentation):

```python
# Import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
```

**Under `        # Get project client`**:

```python
        # Get project client
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )
```

**Under `        # Get an OpenAI client`**:

```python
        # Get an OpenAI client
        openai_client = project_client.get_openai_client()
```

**Under `        # Use the agent to get a response`**:

```python
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
```

Save.

## 7. Run it

```powershell
python text-agent.py
```

At **User prompt:** enter:

```text
Extract named entities from the following text: "Pierre and I went to Paris on July 14th."
```

✅ The agent lists **Pierre** (Person), **Paris** (Location) and **July 14th** (DateTime).

## 8. See which tools the agent chose

1. Add this line **right after** the `else:` block's `print(...)`, at **8 spaces** (same level as `approvals = ...`):

   ```python
           # Show response details
           print(f"\nResponse Details: {response.model_dump_json(indent=2)}")
   ```

2. Save and run `python text-agent.py` again. Prompt:

   ```text
   Tell me what entities and dates are mentioned in this review, and whether it is positive or negative: "I booked my flight to Paris in July with Margie's Travel, and it was fantastic!"
   ```

3. ✅ The answer gives the entities, the date and **positive** sentiment. Scroll up through the JSON: you'll find the tools the agent called, such as `extract_named_entities_from_text` and `detect_sentiment_from_text`.

📸 **Screenshot** the playground with the tool connected and the terminal answer.

Stuck? Compare with [`solution/text-agent.py`](text-agent/solution/text-agent.py), or run `python solution/text-agent.py`.

## What you built

An agent that **decides** which language analyses a request needs and calls them through a standard MCP tool, wrapped in a Python client with Entra ID sign-in. The same agent can be reused by any app.

[Next: Lab 3, Speech models ➡](../lab3-speech-models/README.md)
