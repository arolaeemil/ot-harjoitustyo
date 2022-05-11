from database_make import get_database_connection

class Recordhandler:
    def __init__(self, connection):
        self._connection = connection

    def find_high_score(self):
        """Finds top score from the records database
        """
        cursor = self._connection.cursor()
        cursor.execute("""SELECT MAX(score) FROM records""")
        top_score = cursor.fetchone()
        cursor.close()
        return top_score

    def create_new_score(self, score):
        """Creates a new score into the recoords database
        """
        cursor = self._connection.cursor()
        cursor.execute("""INSERT INTO records (score) VALUES (?)""", [int(score)])
        self._connection.commit()
        cursor.close()

def make_record_handler():
    """creates itself and returns itself
    Return: record_handler object
    """
    record_handler = Recordhandler(get_database_connection())
    return record_handler
