from parma_analytics.db.prod.database_utils import get_connection, close_connection

import pandas as pd


def fetch_data() -> pd.DataFrame:
    connection = get_connection()
    query = """
    SELECT
        csm.company_measurement_id,
        c.id AS company_id,
        c.description AS company_description,
        c.name AS company_name,
        ds.id AS source_module_id,
        ds.source_name,
        sm.id,
        sm.measurement_name,
        sm.type,
        csm.company_measurement_id AS company_source_measurement_id
    FROM
        company_source_measurement csm
    JOIN
        company c ON csm.company_id = c.id
    JOIN
        source_measurement sm ON csm.source_measurement_id = sm.id
    JOIN
        data_source ds ON sm.source_module_id = ds.id
    ORDER BY
        c.id, ds.id, sm.id;
    """

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        connection.commit()
        print(df)
        return df

    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

    finally:
        close_connection(connection, cursor)


def fetch_measurement_data(
    measurement_ids: list, measurement_table: str
) -> pd.DataFrame:
    # Create a database connection
    connection = get_connection()

    # Create named bind parameters
    placeholders = ",".join(["%s" for _ in measurement_ids])

    query = f"""
    SELECT
        company_measurement_id,
        value,
        created_at
    FROM
        {measurement_table}
    WHERE
        company_measurement_id IN ({placeholders})
    ORDER BY
        company_measurement_id, created_at;
    """

    cursor = connection.cursor()
    try:
        cursor.execute(query, measurement_ids)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        connection.commit()
        return df

    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

    finally:
        close_connection(connection, cursor)
