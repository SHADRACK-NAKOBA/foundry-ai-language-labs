# Create one Foundry project for all three labs

[⬅ Prerequisites](00-prerequisites-and-cost.md) · [Next: Set up VS Code ➡](02-setup-vscode.md)

One project in **East US 2** supports everything in these labs: Azure Language, agents with tools, and the gpt-4o-mini speech models.

1. Open <https://ai.azure.com> and sign in. Close any tips or quick-start panes.
2. At the top, turn the **New Foundry** toggle **On**.
3. If prompted, select **Create a new project** (otherwise: project drop-down, upper left → **Create new project**).
4. **Project name**: `prince-language-project`
5. Expand **Advanced options** and set:

   | Setting | Value |
   |---|---|
   | **Foundry resource** | keep the default (`prince-language-project-resource` or similar) |
   | **Subscription** | yours |
   | **Resource group** | **Create new** → `rg-prince-language` |
   | **Region** | **East US 2** |

   > Why East US 2: lab 3's speech models are only offered in a few regions, and the agent tool in lab 2 doesn't work in West US 3. East US 2 covers all three labs.

6. Select **Create** and wait 1–3 minutes until the project home page opens.

## Write down three values

On the project **home page** you'll see them. Paste each one into Notepad:

| Value | Looks like | Used in |
|---|---|---|
| **Project endpoint** | `https://<resource>.services.ai.azure.com/api/projects/prince-language-project` | Labs 1 and 2 |
| **API key** | a long string; select the copy icon | Lab 2 (tool connection) |
| **Foundry resource name** | the `<resource>` part of the endpoint, e.g. `prince-language-project-resource` | Lab 2 |

> 🔐 Treat the API key like a password: never commit it or post it in screenshots.

✅ **Checkpoint:** the project home page shows your endpoint and key, and you've saved the three values.
