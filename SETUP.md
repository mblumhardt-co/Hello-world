# Running the Sell Agent

The sell agent is a command-line program that talks to the live Anthropic
API, so it needs a real terminal with internet access — an iPad's Safari
browser on its own can't run it. The easiest way to get a terminal from an
iPad is **GitHub Codespaces**, a full Linux computer that runs in your
browser tab. If you have access to a Mac or Windows PC, skip to that
section below instead — it's simpler and has no usage limits.

## Get an API key first (one-time)

1. In Safari, go to **console.anthropic.com** and sign in
2. Add a payment method under **Billing** (the API is pay-as-you-go)
3. Go to **API Keys** → **Create Key**, copy it somewhere safe
4. Treat this key like a password — never paste it into a chat message or
   commit it to the repo. If a key is ever exposed that way, revoke it in
   the Console and create a new one.

## From an iPad (or any browser): GitHub Codespaces

1. Go to `github.com/mblumhardt-co/Hello-world` in Safari and log in
2. Tap the green **`< > Code`** button, then the **Codespaces** tab
3. If you want the branch with the sell agent on it, tap the branch
   dropdown first and pick it — otherwise tap **Create codespace on main**
4. Wait about 30-60 seconds for it to spin up. You'll land in an editor
   with a black panel at the bottom — that's the terminal
5. In that terminal, type each of these and press Enter after each one:

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   export ANTHROPIC_API_KEY=your-key-here
   ```

   ```bash
   python3 -m sell_agent.cli
   ```
6. Chat with it right there in the terminal. Type `quit` to exit
7. Close the browser tab when you're done — Codespaces auto-pauses idle
   sessions

## On a Mac you own

1. **Check for Python 3.** Open **Terminal** (Spotlight search — Cmd+Space —
   then type "Terminal"). Type `python3 --version` and press Enter.
   - If it prints a version number (e.g. `Python 3.11.x`), you're set —
     skip to step 3.
   - If it says "command not found," install Python from
     **python.org/downloads** (download the macOS installer, open it, click
     through the installer).
2. **Check for Git.** Type `git --version`. If it's not installed, macOS
   will pop up a prompt to install the "Command Line Developer Tools" —
   click **Install** and wait for it to finish.
3. **Get the code:**
   ```bash
   git clone https://github.com/mblumhardt-co/Hello-world.git
   cd Hello-world
   ```
4. **Install dependencies and run it:**
   ```bash
   pip3 install -r requirements.txt
   export ANTHROPIC_API_KEY=your-key-here
   python3 -m sell_agent.cli
   ```
5. Chat with it right there in Terminal. Type `quit` to exit. Next time,
   you only need steps 3 (skip the `git clone`, just `cd Hello-world`) and
   4's `export` + `python3 -m sell_agent.cli` lines — `pip3 install` only
   needs to happen once (or again after pulling new code with `git pull`).

## On a Windows PC you own

1. **Install Git for Windows** from **git-scm.com/download/win** — download
   the installer, run it, and click "Next" through the defaults. This also
   installs **Git Bash**, a terminal that understands the same commands as
   Mac/Linux (recommended over Command Prompt/PowerShell so the commands
   below just work as written).
2. **Install Python 3** from **python.org/downloads** — download the
   Windows installer, run it, and **check the box "Add python.exe to
   PATH"** on the first screen before clicking Install. This step is easy
   to miss and causes the most confusion later if skipped.
3. **Open Git Bash** (search for it in the Start menu).
4. **Get the code:**
   ```bash
   git clone https://github.com/mblumhardt-co/Hello-world.git
   cd Hello-world
   ```
5. **Install dependencies and run it:**
   ```bash
   pip install -r requirements.txt
   export ANTHROPIC_API_KEY=your-key-here
   python -m sell_agent.cli
   ```
   (On Windows, the command is `python`, not `python3`.)
6. Chat with it right there in Git Bash. Type `quit` to exit. Next time,
   open Git Bash, `cd Hello-world`, then just the `export` and `python -m
   sell_agent.cli` lines.

## Troubleshooting

- **"No Anthropic credentials found"** -- the `export ANTHROPIC_API_KEY=...`
  step didn't run, or you started a new terminal after running it (the
  `export` only lasts for that one terminal session).
- **Invalid API key** -- double-check you copied the whole key from the
  Console, with no extra spaces.
- Orders you place are saved under `orders/<PON>.json` in the repo -- you
  can look up an order again by PON in a later session.
