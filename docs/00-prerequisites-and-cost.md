# Prerequisites and cost

[⬅ README](../README.md) · [Next: Create a Foundry project ➡](01-create-foundry-project.md)

You can work on your **own computer** or a Windows VM in Azure; both work.

| Item | Notes |
|---|---|
| **Azure subscription** | Free Trial or paid, with **Owner** or **Contributor**. |
| **Visual Studio Code** | <https://code.visualstudio.com/> + the **Python** extension (Microsoft). |
| **Python 3.13** | <https://www.python.org/downloads/>. ⚠️ **Not 3.14**: some packages have no 3.14 build yet. Tick **Add python.exe to PATH**. Tested with 3.13. |
| **Git** | <https://git-scm.com/downloads> |
| **Azure CLI** | <https://learn.microsoft.com/cli/azure/install-azure-cli>: the apps sign in through it. |
| **Speakers or headphones** | Lab 3 plays audio (optional: the files are saved either way). |

### Check your tools

Close and reopen VS Code after installing anything. Then **Terminal → New Terminal**:

```powershell
python --version
git --version
az --version
```

`python --version` must show **3.13.x** (3.12 also works). On 3.14, see [Troubleshooting](troubleshooting.md#python-314).

## Cost

| Lab | What you pay for | Approx. |
|---|---|---|
| 1 · Analyze text | Azure Language: 5 reviews × 3 calls = 15 text records | < US $0.02 |
| 2 · Text analysis agent | Agent model tokens + Azure Language tool calls | ~ US $0.03 |
| 3 · Speech models | gpt-4o-mini-tts + gpt-4o-mini-transcribe (a few seconds of audio) | < US $0.05 |
| **All three** | if you [clean up](cleanup.md) at the end | **≈ US $0.10** |

Pricing: [Azure Language](https://azure.microsoft.com/pricing/details/cognitive-services/language-service/) · [Foundry models](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). A cloud VM, if you use one, is billed separately: stop it when you're done.

> 💡 Set a **budget alert**: Azure portal → **Cost Management** → **Budgets** → **+ Add** → $5 → alert at 80%.
