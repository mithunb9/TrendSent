from dotenv import load_dotenv
import os
import MySQLdb
import dcf
import api

load_dotenv()

try:
    connection = MySQLdb.connect(
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

    with connection.cursor() as cursor:
        drop_table_sql = "DROP TABLE IF EXISTS data"
        cursor.execute(drop_table_sql)

        # Create the table if it doesn't exist
        create_table_sql = (
            "CREATE TABLE IF NOT EXISTS data "
            "(id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), comp VARCHAR(255), dcf VARCHAR(255))"
        )
        cursor.execute(create_table_sql)
        
        for company in api.get_companies():
            for data_point in dcf.get_dcf(company["ticker"]):
                date = data_point["date"]
                dcf_value = data_point["dcf"]

                # Use parameterized query to prevent SQL injection
                insert_sql = "INSERT INTO data (date, comp, dcf) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (date, company["ticker"], dcf_value))

        # Print the first row of the table
        cursor.execute("SELECT * FROM data")
        result = cursor.fetchall()
        print(result)

except MySQLdb.Error as e:
    print(f"Database error: {e}")

finally:
    if connection:
        connection.close()
