# Troubleshooting

[⬅ Clean up](cleanup.md) · [Next: Interview questions ➡](interview-questions.md)

| # | Symptom | Lab | Jump to |
|---|---|---|---|
| 1 | `pip install` fails building a package | all | [Python 3.14](#python-314) |
| 2 | *running scripts is disabled on this system* | all | [Activate.ps1 blocked](#activateps1-blocked) |
| 3 | `ModuleNotFoundError` | all | [Environment not active](#environment-not-active) |
| 4 | `IndentationError` / `SyntaxError` / `NameError` | all | [Indentation](#indentation) |
| 5 | *DefaultAzureCredential failed*, *Please run az login* | all | [Sign-in](#sign-in) |
| 6 | 401 / 403 / *PermissionDenied* / *does not have permission* | 1, 3 | [Missing role](#missing-role) |
| 7 | 404 / *Resource not found* | 1, 3 | [Wrong endpoint](#wrong-endpoint) |
| 8 | App prints no answer / *waiting for tool approval* | 2 | [Tool approval](#tool-approval) |
| 9 | Agent not found | 2 | [Agent name](#agent-name) |
| 10 | 403 / 502 in the playground after approving the tool | 2 | [Transient tool errors](#transient-tool-errors) |
| 11 | Tool connection fails / key-based auth blocked | 2 | [Tool connection](#tool-connection) |
| 12 | Model not found in catalog / can't deploy / *DeploymentNotFound* | 3 | [Speech models](#speech-models) |
| 13 | No sound | 3 | [Audio playback](#audio-playback) |

---

### Python 3.14

Install Python 3.13, then from the repo's top folder:

```powershell
deactivate
Remove-Item -Recurse -Force labenv
py -3.13 -m venv labenv
.\labenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Activate.ps1 blocked

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\labenv\Scripts\Activate.ps1
```

### Environment not active

The prompt must start with `(labenv)`. Activate it from the **top folder** (`.\labenv\Scripts\Activate.ps1`), then `cd` into the lab folder. In VS Code: **Python: Select Interpreter** → `labenv`.

### Indentation

Code you add inside `main` goes at **8 spaces**; code inside lab 1's `for` loop at **12**; imports at **0**. Use **Tab** / **Shift+Tab** to fix a selection. Or run the finished version from the app folder: `python solution/<file>.py`.

### Sign-in

```powershell
az login                      # or: az login --use-device-code
az account show               # check it's the subscription with your Foundry project
az account set --subscription "<name or id>"
az login --tenant <tenant-id> # if your account is in several tenants
```

Installed Azure CLI after opening VS Code? Close and reopen VS Code.

### Missing role

Keyless (Entra ID) calls need a **data-plane role** on the Foundry resource, which subscription Owner alone doesn't always grant.

1. Azure portal → open your **Foundry resource** (in `rg-prince-language`) → **Access control (IAM)** → **+ Add** → **Add role assignment**.
2. Add **Cognitive Services User** (lab 1) and **Cognitive Services OpenAI User** (lab 3) → **Members**: your account → **Review + assign**.
3. Wait ~5 minutes, run `az login` again, then rerun the app.

### Wrong endpoint

- **Lab 1:** `https://<resource>.services.ai.azure.com` (the app trims a project URL for you).
- **Lab 3:** the model's Endpoint / Target URI (`https://<resource>.openai.azure.com/` or `.cognitiveservices.azure.com/`), **not** a project URL.
- Check `.env` is saved, named exactly `.env` (not `.env.txt`) and in the same folder as the `.py` file.

### Tool approval

The agent stopped to ask for approval, which a script can't give. Playground → Tools → Azure Language tool → **Configure** → **Always auto-approve all tools** → **Save** the agent. Run again.

### Agent name

`AGENT_NAME` in `.env` must match the portal **exactly** (`Text-Analysis-Agent`, case-sensitive), and `FOUNDRY_ENDPOINT` must be the **project** endpoint ending in `/api/projects/<project>`.

### Transient tool errors

Refresh the playground page and send the same prompt again. These usually clear on retry.

### Tool connection

- Endpoint: `https://{foundry-resource-name}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview` with the **resource** name (not the project name) as the parameter.
- Key: the API key from the project home page, in **Ocp-Apim-Subscription-Key**.
- Key auth disabled by policy: use **Microsoft Entra ID** authentication.
- Region: the project must not be in **West US 3**.

### Speech models

- The project must be in **East US 2**; elsewhere the models may not appear or can't be deployed. Create a new project there if needed.
- Quota error: try again later or request quota; deploy with default settings.
- *DeploymentNotFound*: `MODEL_NAME` must be the **deployment** name shown under **Build → Models**.

### Audio playback

On a machine without speakers (or a VM without audio), playback fails. The app says so and prints the file path. Open `speech.mp3` / `speech.wav` yourself; the model calls still worked.

---

Still stuck? Post the **lab and step** with a screenshot of the **full** error (hide keys, endpoints and subscription IDs) in the **Prince** community lab thread.
