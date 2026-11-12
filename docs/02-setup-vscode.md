# Set up VS Code and Python (once for all labs)

[⬅ Create a Foundry project](01-create-foundry-project.md) · [Next: Lab 1 ➡](../lab1-analyze-text/README.md)

## Clone this repo

1. Open **VS Code**. In **Extensions** (**Ctrl+Shift+X**), install **Python** (Microsoft) if you don't have it.
2. **Ctrl+Shift+P** (Mac **⌘+Shift+P**) → **Git: Clone** → paste:

   ```text
   https://github.com/SHADRACK-NAKOBA/foundry-ai-language-labs.git
   ```

3. Choose a folder → **Select as Repository Destination** → **Open**. If asked whether you trust the authors, select **Yes**.

## One virtual environment for all three labs

1. **Terminal → New Terminal**. It opens in the repo's top folder (`foundry-ai-language-labs`).
2. Run, one line at a time:

   **Windows (PowerShell)**

   ```powershell
   python -m venv labenv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\labenv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   **macOS / Linux**

   ```bash
   python3 -m venv labenv
   source labenv/bin/activate
   pip install -r requirements.txt
   ```

   The prompt now starts with `(labenv)`. The `Set-ExecutionPolicy` line fixes *"running scripts is disabled on this system"* for this terminal only.

3. Tell VS Code to use it: **Ctrl+Shift+P** → **Python: Select Interpreter** → pick the one in `labenv`.

## Sign in to Azure (CLI)

```powershell
az login
```

Pick your account, then select the **subscription that holds your Foundry project**. Several tenants, MFA or no browser? Use `az login --use-device-code` or `az login --tenant <tenant-id>`.

> Every new terminal needs `(labenv)` active again: `.\labenv\Scripts\Activate.ps1` from the top folder.

✅ **Checkpoint:** `(labenv)` in the prompt and `az login` succeeded. Go to [Lab 1](../lab1-analyze-text/README.md).
