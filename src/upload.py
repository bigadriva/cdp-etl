import os

def toPostgre(dataframe, table):
    from sqlalchemy import create_engine
    import io

    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DBNAME')}")
    dataframe.head(0).to_sql(table, engine, index=False, if_exists='replace')

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    dataframe.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, table, null="")  # null values become ''
    conn.commit()
