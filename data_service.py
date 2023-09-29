import pymysql
import os


class MySQLDataService:

    def __init__(self):
        self.conn = None

    def _get_connection(self):
        self.conn = pymysql.connect(
            user=os.environ["db_user"],
            password=os.environ["db_password"],
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
            host=os.environ["db_host"],
            port=3306
        )
        print("Connected!, conn=", self.conn.host)
        return self.conn

    def get_student_info(self, email):

        conn = None

        try:
            sql = "select * from aa_classes_projects.coupon_to_student where email=%s"
            conn = self._get_connection()
            cur = conn.cursor()
            full_sql = cur.mogrify(sql, email)
            print("Full SQL = ", full_sql)
            res = cur.execute(sql, email)
            result = cur.fetchall()
            if result:
                result = result[0]
            else:
                result = None
            conn = None
        except Exception as e:
            print("Exception = ", e)
            if conn:
                conn.close()
            result = None

        return result







