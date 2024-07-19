import psycopg2


conn = psycopg2.connect(
    dbname="feedParser",
    user="postgres",
    password="jordan",
    host="127.0.0.1",
    port="5432"
)

cur = conn.cursor()
if conn:
    print("Db Connected")

cur.close()
conn.close()
