from dotenv import load_dotenv
import os
import MySQLdb
import dcf
import api

DATA_DIR = "data/"

load_dotenv()

try:
    db_connection = MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("USERNAME"),
        passwd=os.getenv("PASSWORD"),
        db=os.getenv("DB_NAME"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "/etc/ssl/cert.pem"
        }
    )

    with db_connection.cursor() as cursor:
        for company in api.get_companies():
            company['ticker'] = company['ticker'].upper()

            cursor.execute(f"SELECT * FROM {company['ticker']}")

            with open(DATA_DIR + f"{company['ticker']}.csv", "w") as f:
                for row in cursor.fetchall():
                    # print(row)
                    f.write(f"{row[0]},{row[1]},{row[2]}\n")

    

except MySQLdb.Error as e:
    print(f"Database error: {e}")
