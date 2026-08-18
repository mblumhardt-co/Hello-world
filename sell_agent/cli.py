"""Terminal chat with the sell agent: python3 -m sell_agent.cli"""

import anthropic

from .agent import SellAgent


def main() -> None:
    agent = SellAgent(client=anthropic.Anthropic())

    print("Ethernet sales desk -- how can I help? (type 'quit' to exit)\n")

    try:
        reply = agent.send(
            "Say hello and ask whether I'd like to place a new order or check on an existing one."
        )
        print(f"Agent: {reply}\n")

        while True:
            user_text = input("You: ").strip()
            if user_text.lower() in {"quit", "exit"}:
                break
            if not user_text:
                continue
            reply = agent.send(user_text)
            print(f"\nAgent: {reply}\n")
    except (KeyboardInterrupt, EOFError):
        pass
    except anthropic.AuthenticationError:
        print("\nInvalid API key. Check ANTHROPIC_API_KEY and try again.")
    except anthropic.APIConnectionError:
        print("\nNetwork error reaching the Anthropic API. Check your connection.")
    except TypeError as e:
        if "authentication" in str(e).lower():
            print("\nNo Anthropic credentials found. Set ANTHROPIC_API_KEY (or run `ant auth login`) and try again.")
        else:
            raise

    print("\nGoodbye.")


if __name__ == "__main__":
    main()
