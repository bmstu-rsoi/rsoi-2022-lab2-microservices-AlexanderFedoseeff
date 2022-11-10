import psycopg2
from psycopg2 import Error

class LoyaltyDB:
    def __init__(self):
        self.DB_URL = "postgres://cypubjqljpvvrt:932ead6c14327f40eb1b43bb285b7c76dbfaa929c99b6ae25f7b8915f0ac301d@ec2-52-49-201-212.eu-west-1.compute.amazonaws.com:5432/d3spo9noe4jbtd"
        
        if not self.check_existing_table_loyalty():
            self.create_table_loyalty()


    def check_existing_table_loyalty(self):
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            if table[0] == "loyalty":
                cursor.close()
                return True
        cursor.close()
        connection.close()
        return False


    def create_table_loyalty(self):
        q1 = '''
                    CREATE TABLE loyalty
                    (
                        id                SERIAL PRIMARY KEY,
                        username          VARCHAR(80) NOT NULL UNIQUE,
                        reservation_count INT         NOT NULL DEFAULT 0,
                        status            VARCHAR(80) NOT NULL DEFAULT 'BRONZE'
                            CHECK (status IN ('BRONZE', 'SILVER', 'GOLD')),
                        discount          INT         NOT NULL
                    );
                    '''
        q2 = '''
                    INSERT INTO loyalty
                    (
                        id,
                        username,
                        reservation_count,
                        status,
                        discount
                    )
                    VALUES 
                    (
                        1,
                        'Test Max',
                        25,
                        'GOLD',
                        10
                    );
                    '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(q1)
        cursor.execute(q2)
        connection.commit()
        cursor.close()
        connection.close()

    
    def get_loyalty(self):
        result = list()
        try:
            connection = psycopg2.connect(self.DB_URL, sslmode="require")
            cursor = connection.cursor()
            #cursor.execute("SELECT id, username, reservation_count, status, discount FROM loyalty")
            cursor.execute("SELECT reservation_count, status, discount FROM loyalty")
            record = cursor.fetchall()
            for i in record:
                i = list(i)
                #result.append({"id": i[0], "username": i[1], "reservation_count": i[2], "status": i[3], "discount": i[4]})
                result.append({"reservation_count": i[0], "status": i[1], "discount": i[2]})
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")
        return result
