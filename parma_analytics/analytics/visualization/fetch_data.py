import psycopg2
import polars as pl


def fetch_int_data(db_params, source_measurement_id):
    # connect DB
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL query
    # cursor.execute("SELECT * FROM source_measurement")
    # cursor.execute("SELECT * FROM measurement_int_value WHERE source_measurement_id = %s", (source_measurement_id,))
    cursor.execute(
        """
        SELECT c.name AS company_name, sm.source_module_id AS module_id, miv.*
        FROM measurement_int_value miv
        JOIN source_measurement sm ON miv.source_measurement_id = sm.id
        JOIN company c ON sm.company_id = c.id
        WHERE miv.source_measurement_id = %s
    """,
        (source_measurement_id,),
    )

    # get results
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()
    return pl.DataFrame(rows, schema=column_names)
