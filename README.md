# Diário Oficial Scraper

[![CI Coverage](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgbdecastro%2Fdo-scray%2Frefs%2Fheads%2Fmain%2Fbadges%2Fcoverage.json&query=%24.message)](https://github.com/gbdecastro/do-scray/actions/workflows/ci-coverage.yml)

Crawler em Python para monitorar diários oficiais, extrair texto de PDFs, procurar termos de interesse e enviar notificações no Telegram.

## O que ele faz

- Lê a página inicial de cada diário oficial configurado.
- Baixa os PDFs das edições encontradas.
- Extrai texto com PyMuPDF e faz fallback para `pdftotext` quando necessário.
- Procura termos globais definidos no projeto.
- Salva PDFs com match e registra estado de processamento.
- Envia mensagens para o Telegram sem bloquear o processamento principal.

## Estrutura

- `diario_oficial/`
  - `apps/`: entrypoints de cada diário e do orquestrador.
  - `crawlers/`: lógica de scraping por município.
  - `helpers/`: utilitários compartilhados, como extração de texto e termos padrão.
  - `models/`: dataclasses de domínio.
  - `services/`: estado local e Telegram.
  - `jobs.py`: lista de crawlers executados pelo orquestrador.
  - `runner.py`: bootstrap comum de execução.
- `diario_oficial-boituva/` e `diario_oficial-sorocaba/`: exemplos HTML usados para referência da estrutura.
- `run_crawlers.sh`: comando recomendado para executar todos os crawlers.
- `requirements.txt`: dependências Python.

## Requisitos

- Python 3.12 ou compatível com `venv`
- `pip`
- `requests`
- `pymupdf`
- Opcional: `pdftotext` para fallback de extração

## Instalação

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Se preferir usar o Python do sistema, garanta que ele permita instalação de pacotes ou use um ambiente virtual local.

## Docker

O projeto tem um `docker-compose.yml` com dois serviços:

- `crawler`: executa o `run_crawlers.sh`
- `dashboard`: exibe os logs persistidos, os estados e os PDFs gerados via Streamlit

### Subir tudo

```bash
docker compose up --build
```

### Acessar o dashboard

Abra `http://localhost:8501`.

### Variáveis de ambiente

O serviço `crawler` usa:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

Você pode exportar essas variáveis antes de subir o Compose ou usar um arquivo `.env`.

### Persistência

Os diretórios `logs/`, `state/` e `DO/` são montados como volumes para preservar logs, estado e PDFs entre execuções.

## Execução

### Rodar todos os crawlers

```bash
./run_crawlers.sh
```

### Rodar um crawler específico

```bash
python3 -m diario_oficial.apps.boituva
python3 -m diario_oficial.apps.sorocaba
```

### Sobrescrever termos

```bash
python3 -m diario_oficial.apps.boituva --term "nome" --term "matrícula"
```

## Como funciona

- Cada crawler tem seu próprio parser HTML e regra de extração.
- O estado de edições processadas é salvo em `state/`.
- Os logs vão para `logs/`.
- Os PDFs com match ficam em `DO/<cidade>/`.
- O Telegram recebe o título com o nome da origem, como `Diário Oficial Boituva` ou `Diário Oficial Sorocaba`.

## Adicionando um novo crawler

1. Crie o parser em `diario_oficial/crawlers/`.
2. Crie o entrypoint em `diario_oficial/apps/`.
3. Registre o job em `diario_oficial/jobs.py`.
4. Reaproveite `extract_pdf_text`, `JsonStateStore` e `TelegramNotifier`.
5. Adicione um exemplo HTML na pasta do novo diário, se isso ajudar na manutenção.

## Observações

- O projeto usa PyMuPDF primeiro e cai para `pdftotext` se necessário.
- O envio ao Telegram roda em background para não travar o processamento dos PDFs.
- `source_name` é usado para montar mensagens por origem.


## Prompt para criação de uma novo crawler

```prompt
Agora usando o [playbooks](.agents/playbooks/) [skills](.agents/skills/) referentes a criação de um novo crawler. Eu preciso criar um para o example: [indaiatuba.html](diario_oficial/examples/indaiatuba.html). Que pode ser encontrado no site:https://www.indaiatuba.sp.gov.br/comunicacao/imprensa-oficial/edicoes/
```
