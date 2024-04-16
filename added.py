import sqlite3 as sq


def export(added_shoes):
    clear()
    con = sq.connect("sneakers.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS added_shoes (
            title TEXT,
            link TEXT
            )""")
    for row in range(0, len(added_shoes)):
        con.execute("INSERT INTO added_shoes VALUES (?, ?);",
                    (added_shoes[row].split('tabulation')[0], added_shoes[row].split('tabulation')[1]))
    con.commit()
    con.close()


def clear():
    con = sq.connect("sneakers.db")
    cur = con.cursor()
    cur.execute("DELETE FROM added_shoes")
    con.commit()
    con.close()
