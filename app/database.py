import mysql.connector
from app.config import db_host, db_user, db_password, db_name

mydb = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_password,
  database=db_name
)
