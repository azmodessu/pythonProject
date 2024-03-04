import sqlite3 as sq

def export():
    con = sq.connect("sneakers.db")
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS sneakers (
    title TEXT,
    price TEXT,
    image TEXT
    )""")

    import openpyxl

    book = openpyxl.open("sneakers.xlsx", read_only=True)

    sheet = book.active


    for row in range(2, sheet.max_row + 1):
        data = []
        for col in range(1, 4):
            value = sheet.cell(row, col).value
            data.append(value)
        cur.execute("INSERT INTO sneakers VALUES (?, ?, ?);", (data[0], data[1], data[2]))

    con.commit()
    con.close()

def clear():
    con = sq.connect("sneakers.db")
    cur = con.cursor()
    cur.execute("DELETE FROM sneakers")
    con.commit()
    con.close()