import pymysql
import os


class MySQLDataService:

    def __init__(self):
        self.conn = pymysql.connect(
            user=os.environ["db_user"],
            password=os.environ["db_password"],
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
            host=os.environ["db_host"],
            port=3306
        )
        print("Connected!, conn=", self.conn.host)

    def get_student_info(self, email):

        try:
            sql = "select * from aa_classes_projects.student_coupon_assigned where email=%s"
            cur = self.conn.cursor()
            full_sql = cur.mogrify(sql, email)
            print("Full SQL = ", full_sql)
            res = cur.execute(sql, email)
            result = cur.fetchall()
            if result:
                result = result[0]
            else:
                result = None
        except Exception as e:
            print("Exception = ", e)
            self.conn.rollback()
            result = None

        return result







