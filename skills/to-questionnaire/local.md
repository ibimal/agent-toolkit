# Local additions to to-questionnaire

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **The user sends it.** Write the file and stop. Sending a message to a
  person is the user's action, never the agent's.
- **Answers attach to an intent.** When the answers come back and they
  inform an intent, add them to that intent as a note in
  `docs/sdlc/intents/`, rather than starting a new document.
