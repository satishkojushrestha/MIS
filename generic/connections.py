from django.db import connection


class DatabaseConnection:
    __cursor = ""
    __per_page = 10
    __page = 1

    def execute_query(self, query, params=None):
        self.__cursor = connection.cursor()
        if not params:
            self.__cursor.execute(query)
        else:
            self.__cursor.execute(query, params)

    def execute_paginate_query(self, table_name, per_page=None, page=None): 
        if not table_name:
            raise Exception("Table name is required")
        paginate_query = f"""SELECT * FROM {table_name}"""
        count_query = f""" SELECT COUNT(id) FROM {table_name} """
        if not per_page:
            per_page = self.__per_page
        if not page:
            page = self.__page
        offset = (page-1) * per_page
        paginated_query = paginate_query + f""" ORDER BY id ASC LIMIT {per_page} OFFSET {offset}"""
        self.execute_query(paginated_query)
        context = {}
        columns = [col[0] for col in self.__cursor.description]
        context['datas'] = [dict(zip(columns, row)) for row in self.__cursor.fetchall()]
        context['per_page'] = per_page
        context['page'] = page     
        self.execute_query(count_query)
        total_data = self.__cursor.fetchone()[0]
        context['total_pages'] = (total_data + per_page - 1) // per_page
        return context
                    
    def save(self):
        connection.commit()

    # def get_query(self):
    #     columns = [col[0] for col in self.__cursor.description]
    #     data = self.__cursor.fetchone()
    #     return [dict(zip(columns, str(row) if str(row) else '')) for row in data]

    def get_id(self):
        try:
            return {f'{self.__cursor.description[0].name}' : f'{self.__cursor.fetchone()[0]}'}
        except:
            return None

    def filter_query(self):
        columns = [col[0] for col in self.__cursor.description]
        return [dict(zip(columns, row)) for row in self.__cursor.fetchall()]
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__cursor.close()
