# Usar uma imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY ./app /app/app

# Expor a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação com Uvicorn
# O host 0.0.0.0 é essencial para que a aplicação seja acessível de fora do contêiner
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]