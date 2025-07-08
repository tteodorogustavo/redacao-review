# Documentação Arquitetônica - Sistema de Correção de Redações ENEM

## Visão Arquitetônica Inicial (Pré-Modelagem de Ameaças)

### 1. Visão Geral da Arquitetura

O sistema de correção automatizada de redações do ENEM foi projetado seguindo uma arquitetura de microserviços distribuídos, onde cada componente possui responsabilidades específicas e bem definidas. Esta abordagem permite escalabilidade, manutenibilidade e isolamento de falhas.

### 2. Componentes Principais

#### 2.1 Frontend (React.js)
- **Responsabilidade**: Interface de usuário para upload de redações e visualização de resultados
- **Tecnologia**: React.js com nginx para servir arquivos estáticos
- **Porta**: 3000
- **Comunicação**: HTTP/REST com o Backend via API

#### 2.2 Backend/API (Flask)
- **Responsabilidade**: Orquestração dos serviços e coordenação do fluxo de processamento
- **Tecnologia**: Python Flask
- **Porta**: 5000
- **Comunicação**: HTTP/REST com todos os microserviços

#### 2.3 Serviço Tesseract OCR
- **Responsabilidade**: Extração de texto de imagens de redações manuscritas
- **Tecnologia**: Python Flask + Tesseract OCR
- **Porta**: 5001
- **Comunicação**: HTTP/REST recebendo imagens e retornando texto

#### 2.4 Serviço Trained Model
- **Responsabilidade**: Análise das cinco competências do ENEM
- **Tecnologia**: Python Flask + Modelos de ML
- **Porta**: 5002
- **Comunicação**: HTTP/REST recebendo texto e retornando análise

#### 2.5 Serviço Llama
- **Responsabilidade**: Geração de feedback personalizado e recomendações
- **Tecnologia**: Python Flask + Modelo de linguagem
- **Porta**: 5003
- **Comunicação**: HTTP/REST recebendo análise e retornando feedback

### 3. Fluxo de Dados

```
[Frontend] → [Backend/API] → [Tesseract OCR] (se imagem)
                ↓
[Frontend] ← [Backend/API] ← [Trained Model]
                ↓
[Frontend] ← [Backend/API] ← [Llama Service]
```

### 4. Tecnologias e Ferramentas

#### 4.1 Containerização
- **Docker**: Containerização de cada serviço
- **Docker Compose**: Orquestração e gerenciamento dos containers
- **Redes Docker**: Comunicação segura entre containers

#### 4.2 Linguagens e Frameworks
- **Python 3.11**: Linguagem principal para todos os serviços backend
- **Flask**: Framework web para APIs
- **React.js**: Framework frontend
- **Nginx**: Servidor web para o frontend

#### 4.3 Bibliotecas Especializadas
- **Tesseract**: OCR para extração de texto
- **NLTK**: Processamento de linguagem natural
- **Transformers**: Modelos de linguagem
- **OpenCV**: Processamento de imagens

### 5. Padrões Arquiteturais

#### 5.1 Microserviços
- Cada serviço é independente e pode ser desenvolvido, testado e implantado separadamente
- Comunicação via APIs REST
- Isolamento de falhas e escalabilidade independente

#### 5.2 API Gateway Pattern
- O Backend/API atua como gateway centralizando as requisições
- Roteamento inteligente para os serviços apropriados
- Agregação de respostas de múltiplos serviços

#### 5.3 Health Check Pattern
- Cada serviço implementa endpoint `/health`
- Monitoramento contínuo da saúde dos serviços
- Recuperação automática em caso de falhas

### 6. Comunicação Entre Serviços

#### 6.1 Protocolo
- HTTP/REST para todas as comunicações
- JSON como formato de dados
- Comunicação síncrona entre serviços

#### 6.2 Endpoints Principais

**Backend/API (5000)**:
- `POST /process-redaction`: Endpoint principal para processamento
- `GET /services-status`: Status de todos os serviços
- `GET /health`: Health check do backend

**Tesseract OCR (5001)**:
- `POST /extract-text`: Extração de texto de imagens
- `GET /health`: Health check

**Trained Model (5002)**:
- `POST /analyze-competencies`: Análise das competências
- `GET /health`: Health check

**Llama Service (5003)**:
- `POST /generate-feedback`: Geração de feedback
- `GET /health`: Health check

### 7. Armazenamento e Persistência

#### 7.1 Dados Temporários
- Imagens e textos processados temporariamente em memória
- Sem persistência de dados pessoais por questões de privacidade

#### 7.2 Modelos de IA
- Modelos armazenados localmente em cada container
- Volume Docker para modelos grandes (se necessário)

### 8. Escalabilidade e Performance

#### 8.1 Escalabilidade Horizontal
- Cada serviço pode ser escalado independentemente
- Load balancing pode ser implementado conforme necessário

#### 8.2 Otimizações
- Cache de modelos em memória
- Processamento assíncrono para operações pesadas
- Compressão de dados nas comunicações

### 9. Monitoramento e Observabilidade

#### 9.1 Health Checks
- Verificação automática da saúde de todos os serviços
- Timeout configurável para detecção de falhas

#### 9.2 Logging
- Logs estruturados em cada serviço
- Rastreamento de requisições entre serviços

### 10. Considerações de Segurança (Pré-Modelagem)

#### 10.1 Isolamento
- Containers isolados com recursos limitados
- Rede Docker interna para comunicação entre serviços

#### 10.2 Validação de Entrada
- Validação de dados em todos os endpoints
- Sanitização de uploads de arquivos

#### 10.3 Tratamento de Erros
- Tratamento adequado de exceções
- Não exposição de informações sensíveis em erros

### 11. Limitações Conhecidas

#### 11.1 Segurança
- Ausência de autenticação e autorização
- Comunicação não criptografada entre serviços
- Falta de rate limiting

#### 11.2 Persistência
- Sem banco de dados para histórico
- Sem cache distribuído

#### 11.3 Monitoramento
- Logging básico sem agregação centralizada
- Ausência de métricas de performance

### 12. Próximas Iterações

Esta documentação representa a visão inicial da arquitetura. Após a implementação das medidas de mitigação de segurança e melhorias identificadas na modelagem de ameaças, uma nova versão desta documentação será criada refletindo as mudanças implementadas.

---

**Versão**: 1.0 (Pré-Modelagem de Ameaças) 
**Data**: Junho 2025  
**Desenvolvido por**: Lucas, Pedro, Gustavo, Thiago