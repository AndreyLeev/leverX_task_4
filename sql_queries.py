CREATE_TABLE_QUERIES_SQL = [
    {
        "table_name": "rooms",
        "create_table_sql": 
            """
            CREATE TABLE IF NOT EXISTS rooms(
                    id INT PRIMARY KEY, 
                    name VARCHAR(255) NOT NULL
                );
            """
    },
    {
        "table_name": "students",
        "create_table_sql": 
            """
            CREATE TABLE IF NOT EXISTS students(
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                birthday DATE NOT NULL, 
                room_id INT,
                sex ENUM('M','F'),
                FOREIGN KEY (room_id)
                    REFERENCES rooms (id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                );
            """
    },
]

SELECT_QUERIES_SQL = [
    """
    SELECT rooms.id, rooms.name, COUNT(students.id) as students
    FROM rooms JOIN students
    ON rooms.id = students.room_id
    GROUP BY rooms.id, rooms.name;
    """
    ,
    """
    SELECT rooms.id, rooms.name,
    FROM rooms JOIN students ON rooms.id = students.room_id
    GROUP BY rooms.id, rooms.name
    ORDER BY avg_age
    LIMIT 5;
    """
    ,
    """
    SELECT rooms.id, rooms.name,
    MAX(ABS(YEAR(st1.birthday)-YEAR(st2.birthday))) as age_difference 
    FROM students as st1 JOIN students as st2 
    ON st1.room_id = st2.room_id
    LEFT JOIN rooms ON st1.room_id = rooms.id
    GROUP BY rooms.id, rooms.name
    ORDER BY age_difference DESC
    LIMIT 5;
    """
    ,
    """
    SELECT DISTINCT rooms.id, rooms.name
    FROM students as st1 JOIN students as st2
    ON st1.room_id = st2.room_id AND st1.sex != st2.sex
    LEFT JOIN rooms ON rooms.id=st1.room_id;
    """
]

CREATE_INDEX_SQL = [
    "CREATE INDEX roomid ON students(room_id);",
]