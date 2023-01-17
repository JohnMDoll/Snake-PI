import sqlite3
from models import Species, Snake, Owner

def get_all_things(resource):
    """gets all contents of a table based on passed resource value"""
    with sqlite3.connect("./SPI.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        things = []
        thing = {}
        if resource == "owners":
            db_cursor.execute( """SELECT * FROM Owners """ )
            dataset = db_cursor.fetchall()
            for row in dataset:
                thing = Owner(
                    row['id'],
                    row['first_name'],
                    row['last_name'],
                    row['email']
                )
                things.append(thing.__dict__)
        elif resource == "snakes":
            db_cursor.execute( """SELECT * FROM Snakes """ )
            dataset = db_cursor.fetchall()
            for row in dataset:
                thing = Snake(
                    row['id'],
                    row['name'],
                    row['owner_id'],
                    row['species_id'],
                    row['gender'],
                    row['color']
                )
                things.append(thing.__dict__)
        elif resource == "species":
            db_cursor.execute( """SELECT * FROM Species """ )
            dataset = db_cursor.fetchall()
            for row in dataset:
                thing = Species(
                    row['id'],
                    row['name']
                )
                things.append(thing.__dict__)
    return things

def get_one_thing(resource, id):
    """returns 1 thing from db based on requested resource and associated id"""
    with sqlite3.connect("./SPI.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        if resource == "owners":
            db_cursor.execute("SELECT * FROM Owners WHERE id = ?", (id,))
            try:
                data = db_cursor.fetchone()
                thing = Owner(
                    data['id'],
                    data['first_name'],
                    data['last_name'],
                    data['email']
                    )
            except TypeError:
                return False
        elif resource == "species":
            db_cursor.execute("SELECT * FROM Species WHERE id = ?", (id,))
            try:
                data = db_cursor.fetchone()
                thing = Species(
                    data['id'],
                    data['name']
                    )
            except TypeError:
                return False
        elif resource == "snakes":
            db_cursor.execute(
                """
                    SELECT
                        s.*, sp.name species
                    FROM Snakes s
                    JOIN Species sp ON sp.id = s.species_id
                    WHERE s.id = ?
                """, (id,))
            try:
                data = db_cursor.fetchone()
                thing = Snake(
                    data['id'],
                    data['name'],
                    data['owner_id'],
                    data['species_id'],
                    data['gender'],
                    data['color'],
                    data['species']
                    )
            except TypeError:
                return False
            if thing.species_name == "Aonyx cinerea":
                return None
    return thing.__dict__

def get_snakes_by_species(species_id):
    """returns all snakes of passed in species"""
    with sqlite3.connect("./SPI.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
                SELECT
                    *
                FROM Snakes
                WHERE species_id = ?
            """, (species_id,))
        things = []
        thing = {}
        try:
            dataset = db_cursor.fetchall()
            for row in dataset:
                thing = Snake(
                    row['id'],
                    row['name'],
                    row['owner_id'],
                    row['species_id'],
                    row['gender'],
                    row['color']
                    )
                things.append(thing.__dict__)
        except TypeError:
            return None
    return things

def create_snake(new_snake):
    """POSTs new snake to db if all properties provided"""
    try:
        if (new_snake['name'] and new_snake['owner_id'] and new_snake['species_id'] and new_snake['gender'] and new_snake['color']):

            with sqlite3.connect("./SPI.sqlite3") as conn:
                # Just use these. It's a Black Box.
                conn.row_factory = sqlite3.Row
                db_cursor = conn.cursor()
                db_cursor.execute( "SELECT MAX(id) FROM Snakes" )
                new_snake['id'] = db_cursor.fetchone()[0] + 1
                db_cursor.execute(
                    """
                    INSERT INTO Snakes
                        (id, name, owner_id, species_id, gender, color)
                    VALUES
                        ( ?, ?, ?, ?, ?, ?)
                    """, (new_snake['id'], new_snake['name'], new_snake['owner_id'], new_snake['species_id'], new_snake['gender'], new_snake['color'])
                )
                return new_snake
    except KeyError:
        expected_keys = ['name', 'owner_id', 'species_id', 'gender', 'color']
        return_message = "New snake missing the following information: "
        for key in expected_keys:
            if key not in new_snake:
                return_message += key + ", "
        return return_message
