from mysql.connector import connect,Error

def db_creating(db_name):
    try:
        with connect(host="localhost",user="root",password="") as db:
            myCursor=db.cursor()

            myCursor.execute("create database "+str(db_name))
            db.commit()
    
    except Error as error:
        print(error)
        db.rollback()
        db.close()
    else:
        print(f"'{db_name}' has been created successfully")


creating_db = db_creating("upload_file_manager")