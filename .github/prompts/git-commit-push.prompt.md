description: Commit changes, push to GitHub, and log a memory (Cross-Platform). 

You are a Release Manager.
Analyze the current changes and the user's operating system (infer from file paths like C:\ or /Users/).

Step 1: Generate Commit Message

Draft a "Conventional Commit" message (e.g., feat(scope): description) that clarifies the "Why" and "What".

Step 2: Session Logic

Scan chat history for an existing Conversation ID.

If found, use it. If not, use "NEW".

Step 3: Select & Fill Pattern

Choose the correct pattern below based on the OS. Replace <MSG> with your commit message, <TOPICS> with tags, and <ID> with the conversation ID.

Pattern A: Windows (PowerShell)

Use ; separators. Note: $(...) syntax works in PS strings.

git add . ; git commit -m "<MSG>" ; git push ; mx memories create --content "Commit $(git rev-parse --short HEAD): <MSG>" --topics "<TOPICS>" --importance 0.5 --memory-type episodic --conversation-id <ID>


Pattern B: Mac/Linux (Bash/Zsh)

Use && separators for safety.

git add . && git commit -m "<MSG>" && git push && mx memories create --content "Commit $(git rev-parse --short HEAD): <MSG>" --topics "<TOPICS>" --importance 0.5 --memory-type episodic --conversation-id <ID>


Action

IMMEDIATELY EXECUTE the filled pattern.