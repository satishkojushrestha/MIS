from django.db import connection


class DatabaseConnection:
    __cursor = ""

    def execute_query(self, query, params=None):
        self.__cursor = connection.cursor()
        if not params:
            self.__cursor.execute(query)
        else:
            self.__cursor.execute(query, params)

            
    def save(self):
        connection.commit()

    def get_query(self):
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
