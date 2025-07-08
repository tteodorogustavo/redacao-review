# Dockerfile para o serviço Llama
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para modelos
RUN mkdir -p /app/models

# Expor porta
EXPOSE 5003

# Comando para executar a aplicação
CMD ["python", "app.py"]

