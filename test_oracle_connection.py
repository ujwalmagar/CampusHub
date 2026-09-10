# pyrefly: ignore [missing-import]
import oracledb
import sys

# Update these variables if you change the setup in 00_setup_user.sql
# or if your Oracle database is running on a different port/service.
DB_USER = "campushub"
DB_PASSWORD = "campushub123"
DB_DSN = "localhost:1521/XEPDB1" # Updated to match your SQL Developer SID 'xe'

def test_connection():
    try:
        print(f"Attempting to connect to Oracle Database at {DB_DSN} as '{DB_USER}'...")
        
        # Connect to Oracle Database
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        
        print("\n✅ SUCCESS: Successfully connected to Oracle Database!")
        print(f"Oracle Database Version: {connection.version}")
        
        # Test a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT sysdate FROM dual")
            result = cursor.fetchone()
            print(f"Database System Time: {result[0]}")
            
        connection.close()
        sys.exit(0)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"\n❌ ERROR: Failed to connect to Oracle Database.")
        print(f"Error Code: {error.code}")
        print(f"Message: {error.message}")
        print("\nPlease verify:")
        print("1. Is the Oracle Database service running?")
        print("2. Did you run the database/00_setup_user.sql script in SQL Developer?")
        print(f"3. Is the DSN '{DB_DSN}' correct for your database?")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
