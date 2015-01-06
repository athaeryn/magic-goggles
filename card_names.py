import sqlite3


def _sanitize_title(title):
    return title.replace(u'\xc6', "AE").encode("ascii", "ignore")


def load_card_names(card_db_path):
    connection = sqlite3.connect(card_db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM cards")
    card_names = cursor.fetchall()
    connection.close()

    return map(lambda x: _sanitize_title(x[0]), card_names)
