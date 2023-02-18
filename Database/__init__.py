import sqlite3

class Database:
  """
  Violet's Main Database class
  User for almost everything that saves data
  """
  
  def __init__(self,path,user_id):
    self.path = path
    self.user = f"DATABASE_{user_id}"
    self.conn = sqlite3.connect(f"{self.path}.db")
    self.cursor = self.conn.cursor()
      
    main_table = f'''
    CREATE TABLE IF NOT EXISTS {self.user} (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
    );
    '''
    self.cursor.execute(main_table)

  
  def add_data(self, key, value):
    input = f'''
    INSERT INTO {self.user} (
    key, value)
    VALUES (?,?);
    '''
    self.cursor.execute(input,(key,value))

  
  def del_data(self,key):
    input = f'''
    DELETE FROM {self.user}
    WHERE lower(key) =lower(?);
    '''
    self.cursor.execute(input,(key,))


  def get_data(self,key):
    input = f'''
    SELECT value FROM {self.user}
    WHERE lower(key) = lower(?);
    '''
    self.cursor.execute(input,(key,))
    value = self.cursor.fetchone()[0]
    return value


  def get_like(self,key):
    input = f'''
        SELECT * FROM {self.user}
        WHERE {" AND ".join([f"key LIKE '%' || ? || '%'" for _ in key])}
    '''
    self.cursor.execute(input,key)
    data = self.cursor.fetchall()
    dictionary = {key:value for key, value in data}
    return dictionary
  
  def edit_data(self,key,value):
    input = f'''
    UPDATE {self.user}
    SET value = ?
    WHERE lower(key) = lower(?);
    '''
    self.cursor.execute(input,(value,key,))


  def clean_data(self):
    input = f'''
    DELETE FROM {self.user};
    '''
    self.cursor.execute(input)


  def list_data(self):
    input = f'''
    SELECT * FROM {self.user};
    '''
    self.cursor.execute(input)
    data = self.cursor.fetchall()
    dictionary = {key:value for key,value in data}
    return dictionary


  def __del__(self):
    self.conn.commit()
    self.conn.close()
    
