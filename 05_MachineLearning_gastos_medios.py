# Importando as bibliotecas necessárias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import mysql.connector
import json

# Criando a conexão com o banco de dados
# ======================================================================
# CODIGO NOVO
# ======================================================================
# Criando as tabelas se elas não existirem
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
    CREATE TABLE IF NOT EXISTS resultados_regressao (
        id INT AUTO_INCREMENT PRIMARY KEY,
        coeficientes TEXT,
        erro_quadratico_medio FLOAT
    ) ENGINE = InnoDB AUTO_INCREMENT = 1;
""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS top_spending_deputies (
    id_deputado INT PRIMARY KEY,
    valor FLOAT,
    nome VARCHAR(255)
) ENGINE=InnoDB;
""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS top_spending_items (
    tipoDespesa VARCHAR(255) PRIMARY KEY,
    valor FLOAT
) ENGINE=InnoDB;
""")
conn.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS gasto_medio_mensal (
    id_deputado INT,
    ano INT,
    mes INT,
    valor FLOAT,
    PRIMARY KEY (id_deputado, ano, mes)
) ENGINE=InnoDB;
""")
conn.commit()

# ======================================================================
# ======================================================================


# Lendo os dados do banco de dados
df = pd.read_sql(
    "SELECT gastos.*, deputados.nome FROM gastos INNER JOIN deputados ON gastos.id_deputado = deputados.id", conn)
#conn.close()

# Codificando a coluna 'nome' para números
le = LabelEncoder()
df['nome'] = le.fit_transform(df['nome'])

# Convertendo a coluna 'data' para o formato datetime e criando novas colunas para o ano, mês e dia
df['data'] = pd.to_datetime(df['data'])
df['year'] = df['data'].dt.year
df['month'] = df['data'].dt.month
df['day'] = df['data'].dt.day

# Removendo a coluna 'data'
df = df.drop('data', axis=1)

# Calculando os deputados que mais gastaram
top_spending_deputies = df.groupby('id_deputado')['valor'].sum().reset_index()
top_spending_deputies = top_spending_deputies.merge(
    df[['id_deputado', 'nome']].drop_duplicates(), on='id_deputado')
top_spending_deputies['nome'] = le.inverse_transform(
    top_spending_deputies['nome'])

# Ordenando os deputados que mais gastaram por valor decrescente
top_spending_deputies = top_spending_deputies.sort_values(by='valor', ascending=True)

# Calculando os itens de despesa com maior valor
top_spending_items = df.groupby('tipoDespesa')['valor'].sum().reset_index()
top_spending_items = top_spending_items.sort_values(by='valor', ascending=True)


# Calculando o gasto médio mensal por deputado
monthly_spending = df.groupby(['id_deputado', 'year', 'month'])['valor'].sum().reset_index()
average_monthly_spending = monthly_spending.groupby(['id_deputado', 'year', 'month'])['valor'].mean().reset_index()
average_monthly_spending.rename(columns={'valor': 'gasto_medio_mensal'}, inplace=True)

# Inserindo os dados em top_spending_deputies no banco de dados
for _, row in top_spending_deputies.iterrows():
    cur.execute("""
    INSERT INTO top_spending_deputies (id_deputado, valor, nome)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    valor=VALUES(valor), nome=VALUES(nome)
    """, (row['id_deputado'], row['valor'], row['nome']))

# Inserindo os dados em top_spending_items no banco de dados
for _, row in top_spending_items.iterrows():
    cur.execute("""
    INSERT INTO top_spending_items (tipoDespesa, valor)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
    valor=VALUES(valor)
    """, (row['tipoDespesa'], row['valor']))

# Inserindo os dados de gasto médio mensal no banco de dados
for _, row in average_monthly_spending.iterrows():
    cur.execute("""
    INSERT INTO gasto_medio_mensal (id_deputado, ano, mes, valor)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    valor=VALUES(valor)
    """, (row['id_deputado'], row['year'], row['month'], row['gasto_medio_mensal']))

# Comitando as mudanças no banco de dados
conn.commit()


# Preparando os dados para o modelo de aprendizado de máquina
X = df.drop('valor', axis=1)
y = df['valor']

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Criando o transformador de colunas para codificar as colunas categóricas
column_trans = make_column_transformer(
    (OneHotEncoder(), ['partido', 'tipoDespesa']),
    remainder='passthrough')

# Criando o pipeline para o modelo de regressão linear
pipe = make_pipeline(column_trans, LinearRegression())

# Treinando o modelo
pipe.fit(X_train, y_train)

# Obtendo os coeficientes do modelo
coef = pipe.named_steps['linearregression'].coef_

# Fazendo previsões com o conjunto de teste
y_pred = pipe.predict(X_test)

# Calculando o erro quadrático médio das previsões
mse = mean_squared_error(y_test, y_pred)


# Inserindo os dados de gasto médio mensal por deputado
cur = conn.cursor()

# Inserindo os resultados da regressão linear
coef_json = json.dumps(coef.tolist())
cur.execute(
    "INSERT INTO resultados_regressao (coeficientes, erro_quadratico_medio) VALUES (%s, %s)",
    (coef_json, float(mse))
)
conn.commit()
cur.close()
conn.close()
# ======================================================================
# ======================================================================

# Imprimindo os resultados
print("Deputados que mais gastaram:")
print(top_spending_deputies)
print("\nItens/grupos de gastos com maior valor:")
print(top_spending_items)
print("\nCoeficientes do modelo de regressão linear:")
print(coef)
print("\nErro quadrático médio das previsões:")
print(mse)

