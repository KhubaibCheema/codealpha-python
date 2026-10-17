"""CodeAlpha Task 2 — Stock Portfolio Tracker.

Add/remove holdings and view a simple performance summary.
Holdings are saved to portfolio.json next to this script.

Run:  python tracker.py

Note: live prices need a finance API key (e.g. yfinance). This version runs
in DEMO mode with fixed prices; get_price() is the hook to plug a live
API in later.
"""
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("portfolio.json")

# Demo prices (USD). Replace get_price() with a live API call to go live.
DEMO_PRICES = {"AAPL": 230.0, "TSLA": 250.0, "INFY": 19.5, "OGDC": 145.0}


def load_portfolio():
    """Read DATA_FILE if it exists, else return {}."""
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            print("Warning: portfolio file was unreadable — starting fresh.")
    return {}


def save_portfolio(portfolio):
    """Write portfolio as JSON to DATA_FILE."""
    DATA_FILE.write_text(json.dumps(portfolio, indent=2))


def get_price(symbol):
    """Return the current price for symbol (demo data for now)."""
    return DEMO_PRICES.get(symbol.upper())


def add_holding(portfolio, symbol, shares, buy_price):
    """Insert or update the holding for symbol."""
    symbol = symbol.upper()
    if symbol in portfolio:
        old = portfolio[symbol]
        total_shares = old["shares"] + shares
        avg_price = ((old["shares"] * old["buy_price"] + shares * buy_price)
                     / total_shares)
        portfolio[symbol] = {"shares": total_shares, "buy_price": round(avg_price, 2)}
    else:
        portfolio[symbol] = {"shares": shares, "buy_price": buy_price}
    return portfolio


def remove_holding(portfolio, symbol):
    """Delete symbol from portfolio if present. Returns True if removed."""
    symbol = symbol.upper()
    if symbol in portfolio:
        del portfolio[symbol]
        return True
    return False


def show_summary(portfolio):
    """Print a table: symbol, shares, buy/current price, value, gain/loss."""
    if not portfolio:
        print("Portfolio is empty. Add a holding first.")
        return

    print(f"\n{'Symbol':<8}{'Shares':<8}{'Buy $':<10}{'Now $':<10}"
          f"{'Value $':<12}{'Gain/Loss $':<12}")
    print("-" * 60)
    total_value = 0.0
    total_gain = 0.0
    for symbol, holding in sorted(portfolio.items()):
        shares = holding["shares"]
        buy = holding["buy_price"]
        now = get_price(symbol)
        if now is None:
            print(f"{symbol:<8}{'n/a price':<52}")
            continue
        value = shares * now
        gain = (now - buy) * shares
        total_value += value
        total_gain += gain
        print(f"{symbol:<8}{shares:<8}{buy:<10.2f}{now:<10.2f}"
              f"{value:<12.2f}{gain:<+12.2f}")
    print("-" * 60)
    print(f"{'TOTAL':<26}{total_value:<12.2f}{total_gain:<+12.2f}\n")


def main():
    """Simple menu loop — add / remove / summary / quit."""
    portfolio = load_portfolio()
    print("Stock Portfolio Tracker (demo prices). Commands: add, remove, summary, quit.")

    while True:
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            save_portfolio(portfolio)
            print("Portfolio saved. Bye!")
            break
        elif cmd == "summary":
            show_summary(portfolio)
        elif cmd == "add":
            try:
                symbol = input("Symbol (e.g. AAPL): ").strip().upper()
                shares = int(input("Shares: ").strip())
                buy_price = float(input("Buy price per share: ").strip())
                if shares <= 0 or buy_price <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input — shares and price must be positive numbers.")
                continue
            add_holding(portfolio, symbol, shares, buy_price)
            save_portfolio(portfolio)
            print(f"Added {shares} x {symbol} @ {buy_price}.")
        elif cmd == "remove":
            symbol = input("Symbol to remove: ").strip().upper()
            if remove_holding(portfolio, symbol):
                save_portfolio(portfolio)
                print(f"Removed {symbol}.")
            else:
                print(f"{symbol} is not in your portfolio.")
        elif cmd == "":
            continue
        else:
            print("Unknown command. Use: add, remove, summary, quit.")


if __name__ == "__main__":
    main()
