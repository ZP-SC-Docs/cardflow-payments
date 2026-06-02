"""Monthly finance export: cards on file per customer, written to the shared drive."""
import csv
import sqlite3

from app import config

OUT = "/mnt/finance/cards_on_file.csv"


def main():
    conn = sqlite3.connect(config.SQLITE_PATH)
    rows = conn.execute(
        "SELECT c.email, k.cardholder_name, k.pan, k.expiry, k.cvv FROM cards k JOIN customers c ON c.id = k.customer_id"
    ).fetchall()
    with open(OUT, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["email", "cardholder", "pan", "expiry", "cvv"])
        writer.writerows(rows)
    print("exported %d cards to %s" % (len(rows), OUT))


if __name__ == "__main__":
    main()
