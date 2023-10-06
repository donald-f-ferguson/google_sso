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
            split_email = email.split('@')
            uni = split_email[0]

            sql = "select * from aa_classes_projects.coupon_to_student where email=%s or Uni=%s"
            conn = self._get_connection()
            cur = conn.cursor()
            full_sql = cur.mogrify(sql, (email,uni))
            print("Full SQL = ", full_sql)
            res = cur.execute(sql, (email, uni))

            if res == 1:
                result = cur.fetchall()
                result = result[0]
                if uni != result['Uni']:
                    raise Exception("WTF?")
            else:
                result = None
            conn.close()
        except Exception as e:
            print("Exception = ", e)
            if conn:
                conn.close()
            result = None

        return result







