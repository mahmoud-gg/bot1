import pyodbc

def search_person(first_name, father_name, grand_name, birth, place):
    # Connect to the database
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Users\Administrator\Desktop\s\\'+place+'.accdb;')
    
    cursor = conn.cursor()

    sql_command = f"SELECT * FROM PERSON WHERE P_FIRST LIKE '{first_name}%' AND P_FATHER LIKE '{father_name}%' AND P_GRAND LIKE '{grand_name}%' AND P_BIRTH LIKE '{birth}%'"
    print(sql_command)
    cursor.execute(sql_command)
    rows = cursor.fetchall()
  
    column_names = [column[0] for column in cursor.description]

    data = []
    for row in rows:
        data_row = {}
        for column_name, value in zip(column_names, row):
            if column_name in ["P_FIRST", "P_FATHER", "P_GRAND", "FAM_NO"]:
                data_row[column_name] = str(value).strip().replace("\x84", "")
            if column_name == "P_BIRTH":
                data_row["BIRTH"] = str(value).strip()

        data.append(data_row)
    
    cursor.close()
    conn.close()
    return data


def search_card(card, place):
  conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Users\Administrator\Desktop\s\\'+place+'.accdb;')
    
  print("started")
  cursor = conn.cursor()
  card = f"'{card}'" if card.startswith("0") else f"{card}"
  cursor.execute(f"SELECT * FROM PERSON WHERE FAM_NO = {card}")
  rows = cursor.fetchall()
  print("ended")
  column_names = [column[0] for column in cursor.description]
  data = []
  
  for row in rows:
        data_row = {}
        for column_name, value in zip(column_names, row):
            if column_name in ["P_FIRST", "P_FATHER", "P_GRAND", "FAM_NO"]:
                data_row[column_name] = str(value).strip().replace("\x84", "")
            if column_name == "P_BIRTH":
                data_row["BIRTH"] = str(value).strip()
        
        data.append(data_row)
        
    
  cursor.close()
  conn.close()
  print(data)
  return data
"""
for person in search_person(input("first_name: "),input("father_name: "),input("grand_name: "),input("birth: "),input("place: ")):
  name = person["P_FIRST"] + " " + person["P_FATHER"] + " " +  person["P_GRAND"] + " : " + person["BIRTH"][:4] + " : " +person["FAM_NO"]
  print(name)


for person in search_card(input("family number: "),input("place: ")):
  name = person["P_FIRST"] + " " + person["P_FATHER"] + " " +  person["P_GRAND"] + " : " + person["BIRTH"][:4] + " : " +person["FAM_NO"]
  print(name)
"""
