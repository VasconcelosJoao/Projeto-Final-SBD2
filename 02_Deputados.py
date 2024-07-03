import requests
import mysql.connector

# Fazendo a requisição

url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'

params = {'idLegislatura': '57', 'ordenarPor': 'id'}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    exit()

data = response.json()

# Conectando ao banco de dados
try:
    with mysql.connector.connect(
        database="TFBD",
        user="user",
        password="password",
        host="localhost",
        port="3306"
    ) as conn:
        with conn.cursor() as cur:
            # Criando a tabela
            table_create_query = """
            CREATE TABLE IF NOT EXISTS deputados (
                id INT PRIMARY KEY,
                nome VARCHAR(255),
                partido VARCHAR(50),
                FOREIGN KEY (partido) REFERENCES partidos(sigla)
            )
            """
            cur.execute(table_create_query)

            # Inserindo os dados na tabela
            for deputado in data['dados']:
                insert_query = """
                    INSERT INTO deputados (id, nome, partido) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE id=id
                """
                cur.execute(
                    insert_query, (deputado['id'], deputado['nome'], deputado['siglaPartido']))

            conn.commit()
except mysql.connector.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")