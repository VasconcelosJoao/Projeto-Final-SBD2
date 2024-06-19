import mysql.connector
import csv

def export_to_csv(table_name, file_name):
    try:
        # Conectando ao banco de dados MySQL
        conn = mysql.connector.connect(
            database="TFBD",
            user="root",
            password="root",
            host="localhost",
            port="3306",
            charset='utf8',  # Define o charset como utf8
            use_unicode=True  # Usa unicode
        )
        # Criando um cursor para executar as operações SQL
        cur = conn.cursor()
        
        # Executando a consulta SQL para selecionar todos os dados da tabela especificada
        cur.execute(f"SELECT * FROM {table_name}")

        # Abrindo um arquivo CSV para escrever os dados
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:  # Define a codificação do arquivo como utf-8
            csvwriter = csv.writer(csvfile)
            
            # Escrevendo o cabeçalho no CSV (nomes das colunas)
            csvwriter.writerow([i[0] for i in cur.description])
            
            # Escrevendo os dados no CSV
            csvwriter.writerows(cur)

        print(f"Dados da tabela {table_name} exportados com sucesso para {file_name}")
        
    except mysql.connector.Error as e:
        # Tratando erros de conexão ou execução de SQL
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        # Fechando a conexão com o banco de dados
        if conn.is_connected():
            cur.close()
            conn.close()

# Exportando os dados das tabelas 'partidos', 'deputados', 'gastos' e 'gastos_estranhos' para arquivos CSV
export_to_csv('partidos', 'partidos.csv')
export_to_csv('deputados', 'deputados.csv')
export_to_csv('gastos', 'gastos.csv')
export_to_csv('gastos_estranhos', 'gastos_estranhos.csv')

