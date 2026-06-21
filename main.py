import json
import os
import csv
import webbrowser

# MNQ multiplier ($2 per point per contract)
MULTIPLIER = 2

# store trades in memory
trades = []

# load saved data
if os.path.exists("trades.json"):
    with open("trades.json", "r") as f:
        trades = json.load(f)


# ---------------- MENU ----------------
def show_menu():
    print("\n==============================")
    print("MNQ TRADING JOURNAL (PRO)")
    print("==============================")
    print("1. Add Trade")
    print("2. View All Trades")
    print("3. Search Trade")
    print("4. Edit Trade")
    print("5. Delete Trade")
    print("6. Filter Trades")
    print("7. Trading Statistics")
    print("8. Daily Summary")
    print("9. Equity Curve")
    print("10. Save Data")
    print("11. Export CSV")   
    print("12. Exit")


# ---------------- ADD TRADE ----------------
def add_trade():
    print("\n--- Add MNQ Trade ---")

    trade_id = input("Trade ID: ")
    date = input("Date (YYYY-MM-DD): ")
    trade_type = input("Type (Buy/Sell): ")

    try:
        entry = float(input("Entry Price: "))
        exit_price = float(input("Exit Price: "))
        lot = float(input("Lot Size: "))
    except:
        print("Invalid input!")
        return

    notes = input("Notes: ")
    image_url = input("Image URL (optional): ")

    # MNQ profit calculation
    if trade_type.lower() == "buy":
        profit = (exit_price - entry) * MULTIPLIER * lot
    else:
        profit = (entry - exit_price) * MULTIPLIER * lot

    trade = {
        "id": trade_id,
        "date": date,
        "type": trade_type,
        "entry": entry,
        "exit": exit_price,
        "lot": lot,
        "profit": profit,
        "notes": notes,
        "image": image_url
    }

    trades.append(trade)
    print("Trade added successfully!")


# ---------------- VIEW ----------------
def view_trades():
    print("\n--- ALL TRADES ---")

    if not trades:
        print("No trades found.")
        return

    print("ID | Type | Entry | Exit | Profit")
    print("-----------------------------------")

    for t in trades:
        print(f"{t['id']} | {t['type']} | {t['entry']} | {t['exit']} | {t['profit']}")

        if t.get("image"):
            print("Image:", t["image"])


# ---------------- SEARCH ----------------
def search_trade():
    tid = input("Enter Trade ID: ")

    for t in trades:
        if t["id"] == tid:
            print("\n--- TRADE FOUND ---")

            for k, v in t.items():
                print(f"{k}: {v}")

            if t.get("image"):
                open_img = input("Open image? (y/n): ")
                if open_img.lower() == "y":
                    webbrowser.open(t["image"])

            return

    print("Trade not found.")


# ---------------- EDIT ----------------
def edit_trade():
    tid = input("Enter Trade ID: ")

    for t in trades:
        if t["id"] == tid:

            print("Leave blank to keep same value")

            new_entry = input("New Entry: ")
            new_exit = input("New Exit: ")
            new_lot = input("New Lot: ")
            new_notes = input("New Notes: ")
            new_image = input("New Image URL: ")

            if new_entry:
                t["entry"] = float(new_entry)
            if new_exit:
                t["exit"] = float(new_exit)
            if new_lot:
                t["lot"] = float(new_lot)
            if new_notes:
                t["notes"] = new_notes
            if new_image:
                t["image"] = new_image

            # recalc profit
            if t["type"].lower() == "buy":
                t["profit"] = (t["exit"] - t["entry"]) * MULTIPLIER * t["lot"]
            else:
                t["profit"] = (t["entry"] - t["exit"]) * MULTIPLIER * t["lot"]

            print("Trade updated!")
            return

    print("Trade not found.")


# ---------------- DELETE ----------------
def delete_trade():
    tid = input("Enter Trade ID: ")

    for t in trades:
        if t["id"] == tid:

            confirm = input("Are you sure? (Y/N): ")

            if confirm.lower() == "y":
                trades.remove(t)
                print("Trade deleted.")
            else:
                print("Cancelled.")

            return

    print("Trade not found.")


# ---------------- FILTER ----------------
def filter_trades():
    print("\n1. Winning Trades")
    print("2. Losing Trades")

    choice = input("Choose: ")

    if choice == "1":
        for t in trades:
            if t["profit"] > 0:
                print(t)

    elif choice == "2":
        for t in trades:
            if t["profit"] <= 0:
                print(t)


# ---------------- STATISTICS ----------------
def statistics():
    if not trades:
        print("No trades.")
        return

    wins = losses = total = 0
    best = worst = trades[0]["profit"]

    for t in trades:
        p = t["profit"]
        total += p

        if p > 0:
            wins += 1
        else:
            losses += 1

        if p > best:
            best = p
        if p < worst:
            worst = p

    print("\n--- STATS ---")
    print("Total Trades:", len(trades))
    print("Win Rate:", (wins/len(trades))*100, "%")
    print("Total Profit:", total)
    print("Best Trade:", best)
    print("Worst Trade:", worst)


# ---------------- DAILY SUMMARY ----------------
def daily_summary():
    summary = {}

    for t in trades:
        d = t["date"]
        summary[d] = summary.get(d, 0) + t["profit"]

    print("\n--- DAILY SUMMARY ---")
    for k, v in summary.items():
        print(k, ":", v)


# ---------------- EQUITY CURVE ----------------
def equity_curve():
    print("\n--- EQUITY CURVE ---")

    total = 0

    for i, t in enumerate(trades, 1):
        total += t["profit"]
        print(f"{i}: {total}")


# ---------------- SAVE JSON ----------------
def save_data():
    with open("trades.json", "w") as f:
        json.dump(trades, f, indent=4)

    print("Saved!")


# ---------------- EXPORT CSV ----------------
def export_csv():
    if not trades:
        print("No data to export.")
        return

    with open("trades.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # headers
        writer.writerow(["ID", "Date", "Type", "Entry", "Exit", "Lot", "Profit", "Notes", "Image"])

        # rows
        for t in trades:
            writer.writerow([
                t["id"],
                t["date"],
                t["type"],
                t["entry"],
                t["exit"],
                t["lot"],
                t["profit"],
                t["notes"],
                t.get("image", "")
            ])

    print("CSV exported successfully!")


# ---------------- MAIN LOOP ----------------
while True:
    show_menu()
    choice = input("\nChoose: ")

    if choice == "1":
        add_trade()
    elif choice == "2":
        view_trades()
    elif choice == "3":
        search_trade()
    elif choice == "4":
        edit_trade()
    elif choice == "5":
        delete_trade()
    elif choice == "6":
        filter_trades()
    elif choice == "7":
        statistics()
    elif choice == "8":
        daily_summary()
    elif choice == "9":
        equity_curve()
    elif choice == "10":
        save_data()
    elif choice == "11":
        export_csv()   
    elif choice == "12":
        save_data()
        print("Bye!")
        break
    else:
        print("Invalid choice")