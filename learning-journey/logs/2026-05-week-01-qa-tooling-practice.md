# Weekly Learning Log - QA Tooling Practice

## Focus This Week

This week I continued practicing QA tooling by working on the QA Bug Report Tool, a small Python CLI project that turns rough QA notes into structured bug reports.

My focus was on learning how a small tool can support both human-readable QA documentation and more structured technical output for future automation or reporting workflows.

## What I Practiced

- Reading and improving a small Python CLI project
- Thinking through feature scope before implementation
- Using Codex as an implementation assistant instead of blindly trusting output
- Keeping the project beginner-readable and portfolio-safe
- Connecting QA habits to tooling features
- Reviewing whether README examples matched actual behavior
- Thinking about tests, command-line behavior, and output formats

## What I Learned

I learned that even a small QA tool needs clear boundaries. It is easy for a simple feature to grow into a much larger project if the scope is not controlled.

I also practiced thinking about the difference between outputs meant for people and outputs meant for tools:

- Markdown is useful for readable bug reports.
- JSON is useful for structured data that other tools could read later.

That helped me better understand how QA documentation can become part of a more technical workflow without pretending the project is production-ready.

## What I Verified

I checked that the intended behavior stayed focused on the current project goal:

- The tool still supports structured bug report output.
- The workflow remains based on fictional/sample QA data.
- The project is still framed as a learning portfolio project.
- The README and examples should stay honest about what the tool currently does.
- Any new feature should be backed by tests and manual verification where practical.

## What Is Still WIP

This project is still a beginner-friendly QA tooling exercise, not a production bug-tracking system.

Still WIP:

- More test coverage for edge cases
- Stronger README examples
- Cleaner sample data
- Better explanation of how this connects to QA/Technical QA workflows
- Future integration ideas like dashboards, imports, or report summaries

## What Confused Me

The main thing I am still working through is understanding where each piece of functionality belongs in the codebase.

For example:

- What should live in the CLI file?
- What should live in a formatter file?
- What belongs in tests?
- How much documentation is enough without overexplaining?

This is part of the learning process, and I am trying to slow down enough to understand the structure instead of just accepting generated code.

## Next Small Step

My next small step is to keep the tool focused and add one improvement at a time.

A good next task would be:

- Add or review JSON export behavior
- Add tests for one edge case
- Improve the README demo section
- Write a short PR summary explaining the QA value of the change

The goal is to keep building small, testable reps that show real QA judgment, technical curiosity, and honest progress.
