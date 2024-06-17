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
