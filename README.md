# Task Safety Observatory

Build a sleek, modern, dark-themed dashboard for an AI execution platform named "AQLYNTOR — Trustworthy AI Execution".

Include 4 main sections:

1. Top Stats Bar: Verified Success Rate (88%), Active Tasks (2), Bounded Recoveries (4), Policy Violations Blocked (0).

2. Live Task Execution Pipeline: Interactive step-by-step flowchart displaying: User Goal -> Planner -> Policy Gate -> Tool Adapter -> Outcome Verifier -> Bounded Recovery -> Audit Log.

3. Execution Log Table: Columns for Task ID, Goal Description, Timestamp, Status Badges (VERIFIED, RECOVERING, STOPPED), and Evidence Output. Include mock evidence for a file inspection task (e.g., summary.md verified).

4. Safety & Policy Rules Panel: Toggles for "Least Privilege Sandbox", "Strict Postcondition Check", and "Human Approval for Destructive Actions".

Make the UI look clean, fast, and high-tech using Tailwind CSS, glassmorphism cards, and green/amber/cyan indicator tags.

This project was built with [Lovable](https://lovable.dev).

**Live app**: https://task-safety-observatory.lovable.app

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/3d25efca-859e-4a91-9580-4272c6b35073).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
