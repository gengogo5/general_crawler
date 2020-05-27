# -*- coding: utf-8 -*-
import textwrap, MySQLdb
import json
from scrapy.utils.project import get_project_settings

class RuleLoader:

    @classmethod
    def find(cls, id):
        settings = get_project_settings()
        db_info = settings.get('DATABASE')
        conn = MySQLdb.connect(**db_info)

        sql = textwrap.dedent('''\
        SELECT  
            rules
        FROM
            crawl_requests
        WHERE
            id = %s
        ''')

        c = conn.cursor()
        c.execute(sql, (id,))
        row = c.fetchone()

        conn.close()
        return json.loads(row[0])