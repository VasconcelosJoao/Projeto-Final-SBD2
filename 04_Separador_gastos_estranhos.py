import requests
import mysql.connector

# Conectando ao banco de dados
conn = mysql.connector.connect(
    database="TFBD",
    user="root",
    password="unbMySQL#21",
    host="localhost",
    port="3306"
)
cur = conn.cursor()

# Criando a tabela gastos se ela não existir
cur.execute("""
    CREATE TABLE IF NOT EXISTS gastos_estranhos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_deputado INT,
        data DATE,
        valor FLOAT,
        tipoDespesa VARCHAR(255),
        codDocumento INT,
        partido VARCHAR(50),
        FOREIGN KEY (id_deputado) REFERENCES deputados(id),
        FOREIGN KEY (partido) REFERENCES partidos(sigla)
    )
""")
conn.commit()

# Encontrando as linhas com valores estranhos
cur.execute("""
    SELECT * FROM gastos WHERE YEAR(data) != 2023 OR codDocumento = 0 OR valor <= 0
""")
rows = cur.fetchall()

# Inserindo as linhas estranhas na nova tabela e removendo da tabela original
for row in rows:
    cur.execute("""
        INSERT INTO gastos_estranhos (id_deputado, data, valor, tipoDespesa, codDocumento, partido) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row[1], row[2], row[3], row[4], row[5], row[6]))
    cur.execute("""
        DELETE FROM gastos WHERE id = %s
    """, (row[0],))
    conn.commit()

# Fechando o cursor e a conexão
cur.close()
conn.close()