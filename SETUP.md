# Running the Sell Agent

The sell agent is a command-line program that talks to the live Anthropic
API, so it needs a real terminal with internet access — an iPad's Safari
browser on its own can't run it. The easiest way to get a terminal from an
iPad is **GitHub Codespaces**, a full Linux computer that runs in your
browser tab. (If you have a Mac, Windows PC, or Chromebook, skip to
"On a computer you own" below instead — it's simpler.)

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

## On a computer you own (Mac / Windows / Linux)

1. Open the Terminal app (Mac: Spotlight search "Terminal"; Windows: search
   "Command Prompt" or "PowerShell")
2. Clone the repo and step into it:
   ```bash
   git clone https://github.com/mblumhardt-co/Hello-world.git
   cd Hello-world
   ```
3. Run the same three commands as above (`pip install -r requirements.txt`,
   `export ANTHROPIC_API_KEY=...`, `python3 -m sell_agent.cli`)

## Troubleshooting

- **"No Anthropic credentials found"** -- the `export ANTHROPIC_API_KEY=...`
  step didn't run, or you started a new terminal after running it (the
  `export` only lasts for that one terminal session).
- **Invalid API key** -- double-check you copied the whole key from the
  Console, with no extra spaces.
- Orders you place are saved under `orders/<PON>.json` in the repo -- you
  can look up an order again by PON in a later session.
