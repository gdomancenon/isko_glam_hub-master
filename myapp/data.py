import sqlite3

db_path = 'glms.db'

# This function connects to the DB and returns a conn and cur objects
def connect_to_db(path):
    conn = sqlite3.connect(path)
    # Converting tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# This function returns glams by glam_type
def read_glams_by_glam_type(glam_type):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM glams WHERE glam_type = ?'
    value = glam_type.capitalize()
    results = cur.execute(query,(value,)).fetchall()
    conn.close()
    return results

# This function retrieves 1 glam by glam_id
def read_glam_by_glam_id(glam_id):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM glams WHERE id = ?'
    value = glam_id
    result = cur.execute(query,(value,)).fetchone()
    conn.close()
    return result

# This function inserts 1 glam data
def insert_glam(glam_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO glams (glam_type, name, date_established, location, description, url) VALUES (?,?,?,?,?,?)'
    values = (glam_data['glam_type'], glam_data['name'],
              glam_data['date_established'], glam_data['location'],
              glam_data['description'], glam_data['url'])
    cur.execute(query,values)
    conn.commit()
    conn.close()

# This function updates a record
def update_glam(glam_data):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE glams SET glam_type=?, name=?, date_established=?, location=?, description=?, url=? WHERE id=?"
    values = (glam_data['glam_type'], glam_data['name'],
              glam_data['date_established'], glam_data['location'],
              glam_data['description'], glam_data['url'],
              glam_data['glam_id'])
    cur.execute(query,values)
    conn.commit()
    conn.close()

#This function deletes a record
def delete_glam(glam_id):
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM glams WHERE id=?"
    cur.execute(query, (glam_id,))
    conn.commit()
    conn.close()

# This function creates the "glams" table if it doesn't exist
def create_glams_table():
    conn, cur = connect_to_db(db_path)
    query = '''
        CREATE TABLE IF NOT EXISTS glams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            glam_type TEXT,
            name TEXT,
            date_established INTEGER,
            location TEXT,
            description TEXT,
            url TEXT
            ) '''
    result = cur.execute(query).fetchone()
    conn.close()
    return result


