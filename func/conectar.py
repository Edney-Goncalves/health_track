def conectar():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # Cria a tabela se não existir
    cur.execute("""
		CREATE TABLE IF NOT EXISTS pacient (
			id SERIAL PRIMARY KEY,
			name VARCHAR(100) NOT NULL,
			cpf VARCHAR(11) UNIQUE NOT NULL,
			rg VARCHAR(20) UNIQUE NOT NULL,
			health_state TEXT,
			age INTEGER NOT NULL,
			gender VARCHAR(20),
			disease_history JSONB
		);
	""")

    conn.commit()
    return conn, cur