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

# Criando a conexão com o banco de dados
conn = mysql.connector.connect(
    database="TFBD",
    user="root",
    password="unbMySQL#21",
    host="localhost",
    port="3306"
)

# Lendo os dados do banco de dados
df = pd.read_sql(
    "SELECT gastos.*, deputados.nome FROM gastos INNER JOIN deputados ON gastos.id_deputado = deputados.id", conn)
conn.close()

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
top_spending_deputies = df.groupby('id_deputado')['valor'].sum(
).sort_values(ascending=False).reset_index()
top_spending_deputies = top_spending_deputies.merge(
    df[['id_deputado', 'nome']].drop_duplicates(), on='id_deputado')
top_spending_deputies['nome'] = le.inverse_transform(
    top_spending_deputies['nome'])

# Calculando os itens de despesa com maior valor
top_spending_items = df.groupby('tipoDespesa')[
    'valor'].sum().sort_values(ascending=False)

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

# Imprimindo os resultados
print("Deputados que mais gastaram:")
print(top_spending_deputies)
print("\nItens/grupos de gastos com maior valor:")
print(top_spending_items)
print("\nCoeficientes do modelo de regressão linear:")
print(coef)
print("\nErro quadrático médio das previsões:")
print(mse)

