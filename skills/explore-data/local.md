# Local additions to explore-data

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Read `data-context` before any query,** and write back what you learn
  about grain, keys, freshness and traps, with its source.
- **Large local files** (CSV, Parquet, JSON) go through DuckDB, so profiling
  does not load them into memory.
- **Personal data.** Flag columns that hold personal data and never print
  their values; show only counts and patterns for them.
- **Where the profile goes.** When the profile serves a change, save it as
  `profile.md` in the change folder. Otherwise return it in the reply.
- **Next questions.** End with the questions worth asking next, as the
  instructions below describe.
