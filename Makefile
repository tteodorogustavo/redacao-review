# Makefile para o Sistema de Correção de Redações ENEM

.PHONY: help build up down logs clean test status

# Variáveis
COMPOSE_FILE = docker-compose.yml
PROJECT_NAME = redaction_corrector

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Constrói todas as imagens Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Inicia todos os serviços
	docker-compose -f $(COMPOSE_FILE) up -d

up-build: ## Constrói e inicia todos os serviços
	docker-compose -f $(COMPOSE_FILE) up --build -d

down: ## Para todos os serviços
	docker-compose -f $(COMPOSE_FILE) down

logs: ## Mostra logs de todos os serviços
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-service: ## Mostra logs de um serviço específico (uso: make logs-service SERVICE=backend)
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE)

status: ## Mostra status dos serviços
	docker-compose -f $(COMPOSE_FILE) ps

restart: ## Reinicia todos os serviços
	docker-compose -f $(COMPOSE_FILE) restart

restart-service: ## Reinicia um serviço específico (uso: make restart-service SERVICE=backend)
	docker-compose -f $(COMPOSE_FILE) restart $(SERVICE)

clean: ## Remove containers, redes e volumes não utilizados
	docker-compose -f $(COMPOSE_FILE) down -v
	docker system prune -f

clean-all: ## Remove tudo incluindo imagens
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	docker system prune -a -f

test-health: ## Testa a saúde de todos os serviços
	@echo "Testando saúde dos serviços..."
	@curl -s http://localhost:5000/health || echo "Backend: FALHOU"
	@curl -s http://localhost:5001/health || echo "Tesseract OCR: FALHOU"
	@curl -s http://localhost:5002/health || echo "Trained Model: FALHOU"
	@curl -s http://localhost:5003/health || echo "Llama Service: FALHOU"
	@echo "Teste de saúde concluído"

test-services: ## Testa o status de todos os serviços via backend
	@curl -s http://localhost:5000/services-status | python3 -m json.tool

dev-up: ## Inicia em modo desenvolvimento com logs
	docker-compose -f $(COMPOSE_FILE) up --build

prod-up: ## Inicia em modo produção
	FLASK_ENV=production docker-compose -f $(COMPOSE_FILE) up -d --build

backup: ## Cria backup dos volumes (se houver)
	@echo "Criando backup..."
	@mkdir -p backups
	@docker run --rm -v $(PROJECT_NAME)_models_data:/data -v $(PWD)/backups:/backup alpine tar czf /backup/models_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz -C /data .

install-deps: ## Instala dependências locais para desenvolvimento
	@echo "Instalando dependências do frontend..."
	@cd frontend && npm install
	@echo "Dependências instaladas"

format: ## Formata código Python
	@find . -name "*.py" -not -path "./frontend/*" -not -path "./.git/*" | xargs python3 -m black

lint: ## Executa linting no código Python
	@find . -name "*.py" -not -path "./frontend/*" -not -path "./.git/*" | xargs python3 -m flake8

# Comandos de desenvolvimento individual
dev-backend: ## Executa apenas o backend em modo desenvolvimento
	cd backend && python3 app.py

dev-frontend: ## Executa apenas o frontend em modo desenvolvimento
	cd frontend && npm start

# Comandos de teste
test-ocr: ## Testa o serviço OCR com uma imagem de exemplo
	@echo "Para testar OCR, use: curl -X POST -F 'image=@exemplo.jpg' http://localhost:5001/extract-text"

test-analysis: ## Testa o serviço de análise com texto de exemplo
	@curl -X POST -H "Content-Type: application/json" -d '{"text":"Esta é uma redação de exemplo para testar o sistema de análise de competências do ENEM."}' http://localhost:5002/analyze-competencies

# Comandos de monitoramento
monitor: ## Monitora recursos dos containers
	docker stats

top: ## Mostra processos dos containers
	docker-compose -f $(COMPOSE_FILE) top

