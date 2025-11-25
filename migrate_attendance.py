import MySQLdb
from config import Config

def migrate_db():
    try:
        conn = MySQLdb.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB
        )
        cursor = conn.cursor()
        
        subjects = ['ada', 'dbms', 'sepm', 'rmk', 'cc', 'esk', 'sdk']
        
        for sub in subjects:
            try:
                print(f"Adding column {sub} to attendance table...")
                cursor.execute(f"ALTER TABLE attendance ADD COLUMN {sub} FLOAT DEFAULT 0")
                print(f"Column {sub} added successfully.")
            except MySQLdb.OperationalError as e:
                if e.args[0] == 1060: # Duplicate column name
                    print(f"Column {sub} already exists.")
                else:
                    raise e
                    
        conn.commit()
        cursor.close()
        conn.close()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_db()
