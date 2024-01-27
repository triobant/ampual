import sqlite3


def main():
    print(search_db())


# Search with a month as input from user
# Display which vegetables can be raise, planted or harvested for the given month
def search_db():
    connection = sqlite3.connect("plants.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vegetables")
    rows = cursor.fetchall()


if __name__ == "__main__":
    main()
