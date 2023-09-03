import sqlite3

CONN = sqlite3.connect("lib/dogs.db")
CURSOR = CONN.cursor()


class Dog:

    all = []

    def __init__(self, name, breed) -> None:
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS dogs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        breed TEXT
        )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS dogs"""

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = """INSERT INTO dogs(name, breed) VALUES(?, ?)"""
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()

            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

        else:
            sql = """UPDATE dogs SET name=?, breed=? WHERE id=?"""
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

        return self

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]

    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM dogs"""

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]

    @classmethod
    def find_by_name(cls, name):
        sql = """SELECT * FROM dogs WHERE name = ?"""

        result = CURSOR.execute(sql, (name,)).fetchone()

        if result:
            dog = cls(result[0], result[1])
            dog.id = result[0]
            return dog
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        sql = """SELECT * FROM dogs WHERE id = ?"""

        result = CURSOR.execute(sql, (id,)).fetchone()

        if result is not None:
            dog = cls(result[1], result[2])
            dog.id = result[0]
            return dog
        
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """SELECT * FROM dogs WHERE name = ? AND breed = ?"""
        result = CURSOR.execute(sql, (name, breed)).fetchone()

        if result:
            dog = cls(result[1], result[2])
            dog.id = result[0]
            return dog
        else:
            new_dog = cls(name, breed)
            new_dog.save()
            return new_dog
        
    def update(self, new_name):
        if self.id is not None:
            sql = """UPDATE dogs SET name=? WHERE id=?"""
            CURSOR.execute(sql, (new_name, self.id))
            CONN.commit()

            self.name = new_name
        
    


