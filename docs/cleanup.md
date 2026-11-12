# Clean up

[⬅ Share your learnings](share-your-learnings.md) · [Next: Troubleshooting ➡](troubleshooting.md)

1. Open <https://portal.azure.com> → search **Resource groups** → open **`rg-prince-language`**.
2. Check it only holds this lab's resources (the Foundry resource and its project).
3. **Delete resource group** → type the name → **Delete**.
4. Wait for the *Deleted resource group* notification. It can take **20–30 minutes**; check before you close the portal.
5. Using a cloud VM for these labs? **Stop** (deallocate) it, or delete it if you no longer need it.

Locally you can delete the `labenv` folder and the generated `speech.mp3`.

> Deleting the resource group also deletes the agent, the tool connection and the model deployments.
