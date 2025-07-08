# Dockerfile para o Frontend (React)
FROM node:18-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código da aplicação
COPY . .

# Build da aplicação
RUN npm run build

# Usar nginx para servir arquivos estáticos
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html

# Copiar configuração customizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta
EXPOSE 3000

# Comando para executar
CMD ["nginx", "-g", "daemon off;"]

