from .Database import Database
from datetime import datetime

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    @staticmethod
    def insert_value_sensoren(value,sensor):
        now = datetime.now()
        sql = "INSERT INTO tblWaarde (Value,Sensor,Date) VALUES (%s,%s,%s)"
        params = [value,sensor,now]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_value_sensoren(sensor):
        params = [sensor]
        sql = "SELECT idWaarde, Value, Sensor, cast(Date as char) as datum FROM project1.tblWaarde WHERE Sensor = %s ORDER BY idWaarde desc LIMIT 1;"
        return Database.get_rows(sql,params)
