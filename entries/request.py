import sqlite3
import json
from models import Entry, Mood, Tag

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label
        FROM entry e
        JOIN mood m
            ON m.id = e.moodId
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Entry class above.
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['date'], row['moodId'])
            mood = Mood(row['moodId'], row['label'])
            entry.mood = mood.__dict__

            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM Entry_Tag et
            JOIN Tag t
                ON t.id = et.tag_id
            WHERE et.entry_id = ?
            """, ( entry.id, ))

            tag_data = db_cursor.fetchall()

            tags = []

            for tag in tag_data:
                tag = Tag(tag['id'], tag['name'])
                tags.append(tag.__dict__)

            entry.tags = tags
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label
        FROM entry e
        JOIN mood m
            ON m.id = e.moodId
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['date'], data['moodId'])
        mood = Mood(data['moodId'], data['label'])
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)

def get_entries_by_search(terms):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM entry e
        WHERE e.entry LIKE ?
        """, ( f'%{terms}%', ))

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Entry class above.
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['date'], row['moodId'])

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, date, moodId )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], 
                new_entry['entry'],
                new_entry['date'], 
                new_entry['moodId'],))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        for tagId in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO Entry_Tag
                ( entry_id, tag_id )
            VALUES
                ( ?, ? );
            """, ( id, tagId ))


        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id
    return new_entry

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entry
            SET
                concept = ?,
                entry = ?,
                date = ?,
                moodId = ?
        WHERE id = ?
        """, (new_entry['concept'],
                new_entry['entry'],
                new_entry['date'],
                new_entry['moodId'],
                id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


    return json.dumps(new_entry)