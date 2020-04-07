import psycopg2

def insert_user(user=[]):
    """ insert a new vendor into the vendors table """
    connect_str = "dbname='amizone' user='neel' host='localhost' " + \
                  "password='9870154473'"
    sql = """INSERT INTO users(username,password)
             VALUES(%s,%s) RETURNING id;"""
    conn = None
    id = None
    try:
        # read database configuration
        #params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(connect_str)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (user[0],user[1]))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id