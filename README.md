# Sistema Automatizado de Correção de Redações ENEM

## Descrição do Projeto

Este projeto desenvolve um sistema distribuído utilizando múltiplos agentes de Inteligência Artificial para correção automatizada de redações do ENEM, fornecendo feedback personalizado e recomendações de conteúdo para melhoria da escrita.

## Validação do Problema

### A Dor que o Projeto Pretende Resolver

A correção de redações do ENEM é um processo complexo e demorado que envolve milhões de textos anualmente. Estudantes frequentemente enfrentam dificuldades para receber feedback detalhado e personalizado sobre suas redações, especialmente considerando as cinco competências específicas avaliadas no exame.

O sistema educacional brasileiro enfrenta desafios significativos na preparação de estudantes para a redação do ENEM, que representa 20% da nota final do exame. A falta de feedback imediato e personalizado limita a capacidade dos estudantes de melhorarem suas habilidades de escrita de forma eficiente.

### Relevância do Problema

Segundo dados do INEP, mais de 5 milhões de candidatos participam anualmente do ENEM [1]. A redação é um dos componentes mais desafiadores, com uma taxa significativa de notas baixas. Em 2022, apenas 0,16% dos participantes obtiveram nota máxima na redação [2].

A implementação de um sistema automatizado pode:
- Democratizar o acesso a feedback de qualidade
- Reduzir custos de correção manual
- Fornecer feedback imediato aos estudantes
- Personalizar recomendações de estudo
- Escalar o processo de avaliação

## Arquitetura do Sistema

### Visão Geral

O sistema é composto por múltiplos microserviços containerizados que trabalham em conjunto:

1. **Frontend**: Interface web para upload de redações e visualização de resultados
2. **Backend/API**: Orquestrador principal que coordena os serviços
3. **Tesseract OCR**: Extração de texto de imagens de redações manuscritas
4. **Trained Model**: Análise das competências do ENEM
5. **Llama**: Geração de feedback personalizado e recomendações

### Tecnologias Utilizadas

- **Containerização**: Docker e Docker Compose
- **Backend**: Python Flask
- **Frontend**: React.js
- **OCR**: Tesseract
- **IA**: Modelos de linguagem para análise e feedback
- **Comunicação**: APIs REST entre microserviços

## Estrutura do Projeto

```
redaction_corrector/
├── backend/                    # API principal
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── frontend/                   # Interface React
│   ├── Dockerfile
│   ├── package.json
│   └── nginx.conf
├── services/                   # Microserviços de IA
│   ├── tesseract-ocr/         # Serviço OCR
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── trained-model/         # Análise de competências
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   └── llama/                 # Geração de feedback
│       ├── Dockerfile
│       ├── app.py
│       └── requirements.txt
├── docker-compose.yml         # Orquestração dos serviços
├── .env                       # Variáveis de ambiente
├── .gitignore
└── README.md
```

## Como Executar

### Pré-requisitos

- Docker
- Docker Compose
- Git

### Instalação e Execução

1. Clone o repositório:
```bash
git clone <repository-url>
cd redaction_corrector
```

2. Execute o sistema completo:
```bash
docker-compose up --build
```

3. Acesse a aplicação:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Status dos serviços: http://localhost:5000/services-status

### Serviços Individuais

- **Tesseract OCR**: http://localhost:5001
- **Trained Model**: http://localhost:5002
- **Llama Service**: http://localhost:5003
- 
## Funcionalidades

### Competências Avaliadas

O sistema avalia as cinco competências do ENEM:

1. **Competência 1**: Domínio da modalidade escrita formal da língua portuguesa
2. **Competência 2**: Compreender a proposta de redação e aplicar conceitos
3. **Competência 3**: Selecionar, relacionar, organizar e interpretar informações
4. **Competência 4**: Demonstrar conhecimento dos mecanismos linguísticos
5. **Competência 5**: Elaborar proposta de intervenção para o problema abordado

### Fluxo de Processamento

1. **Upload**: Usuário envia redação (texto ou imagem)
2. **OCR**: Extração de texto se necessário
3. **Análise**: Avaliação das competências
4. **Feedback**: Geração de recomendações personalizadas
5. **Resultado**: Apresentação de pontuação e sugestões

## Segurança e Arquitetura

### Medidas de Segurança Implementadas

- Containerização para isolamento de serviços
- Comunicação interna entre containers via rede Docker
- Validação de entrada em todos os endpoints
- Tratamento de erros e logs de segurança

### Arquitetura Distribuída

O sistema implementa uma arquitetura de microserviços com:
- Separação de responsabilidades
- Escalabilidade horizontal
- Tolerância a falhas
- Monitoramento de saúde dos serviços

## Desenvolvimento e Contribuição

### Estrutura de Desenvolvimento

O projeto segue as melhores práticas de desenvolvimento:
- Versionamento com Git
- Containerização para consistência de ambiente
- Documentação técnica completa
- Testes de saúde dos serviços

### Próximos Passos

1. Implementação de autenticação e autorização
2. Melhorias no modelo de análise de competências
3. Interface web mais robusta
4. Sistema de cache para melhor performance
5. Monitoramento e logging avançados

## Referências

[1] Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP). "Microdados do ENEM 2022". Disponível em: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem

[2] INEP. "Relatório de Resultados ENEM 2022". Disponível em: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem/resultados

[3] Ministério da Educação. "Competências e Habilidades da Redação do ENEM". Disponível em: https://www.gov.br/mec/pt-br

[4] Silva, A. et al. "Automated Essay Scoring in Portuguese: Challenges and Opportunities". Journal of Educational Technology, 2023.

[5] Santos, M. "Inteligência Artificial na Educação Brasileira: Perspectivas e Desafios". Revista Brasileira de Informática na Educação, 2023.

---

**Desenvolvido por**: Lucas, Pedro, Gustavo, Thiago
**Data**: 2025
**Licença**: MIT