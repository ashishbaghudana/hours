import peewee as pw

from hours.db_secret import USERNAME, PASSWORD, HOST, PORT, DB_NAME

mysql_db = pw.MySQLDatabase(DB_NAME,
                            user=USERNAME,
                            password=PASSWORD,
                            host=HOST,
                            port=PORT)


class BaseModel(pw.Model):
    class Meta:
        database = mysql_db