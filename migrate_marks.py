import MySQLdb
from config import Config

def migrate_marks():
    try:
        conn = MySQLdb.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB
        )
        cursor = conn.cursor()
        
        subjects = ['ada', 'dbms', 'sepm', 'rmk', 'cc', 'esk', 'sdk']
        exam_types = ['int1', 'int2', 'sem']
        
        for sub in subjects:
            for et in exam_types:
                col_name = f"{sub}_{et}"
                try:
                    print(f"Adding column {col_name} to marks table...")
                    cursor.execute(f"ALTER TABLE marks ADD COLUMN {col_name} INT DEFAULT 0")
                    print(f"Column {col_name} added successfully.")
                except MySQLdb.OperationalError as e:
                    if e.args[0] == 1060: # Duplicate column name
                        print(f"Column {col_name} already exists.")
                    else:
                        raise e
                    
        conn.commit()
        cursor.close()
        conn.close()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_marks()
