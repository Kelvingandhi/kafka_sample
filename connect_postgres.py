
"""
Twitter API/Realtime Data -> FastAPI -> Kafka Producer -> Kafka Message Queue 
-> Kafka Counsumer -> PostgresDB -> Streamlit
"""


from matplotlib import use
import psycopg2

#Connect to existing database
conn = psycopg2.connect(
    database = "daily_practice",
    user = "root",
    password = "root",
    host = "localhost"
)

cur = conn.cursor()

cur.execute("select * from event_status")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()

