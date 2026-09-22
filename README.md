# TravelPlan - Trip Service (API Secundária)

## Descrição

API responsável pela regra de negócio do TravelPlan: recebe uma cidade e um
período de datas, consulta a previsão do tempo na API externa Open-Meteo
e calcula o melhor dia da janela informada (menor chance de chuva), além de
uma sugestão simples de bagagem. Os planos de viagem são persistidos em um
banco SQLite.

Este componente é consumido pela API Principal (gateway), que atua como
proxy com cache para as rotas abaixo.

## Rotas

| Método | Rota | Descrição |
|---|---|---|
| POST | /trips | Cria uma viagem e calcula o plano (melhor dia + bagagem) |
| GET | /trips | Lista todas as viagens salvas |
| GET | /trips/{id} | Detalha uma viagem |
| PUT | /trips/{id} | Atualiza cidade/datas e recalcula o plano |
| DELETE | /trips/{id} | Remove uma viagem |

Documentação interativa (Swagger) disponível em /docs após subir a aplicação.

## Execução via Docker

Passo 1: Construa a imagem:

```
docker build -t trip-service .
```

Passo 2: Rode o container:

```
docker run -p 8001:8001 --name trip-service trip-service
```

Passo 3: Acesse a documentação em http://localhost:8001/docs

Para rodar em conjunto com a API Principal (gateway), veja as instruções
completas no README do gateway: https://github.com/matheus-rmds/gateway

## Instalação e execução local (sem Docker)

Passo 1: Crie e ative um ambiente virtual:

```
python -m venv .venv
.venv\Scripts\activate
```

Passo 2: Instale as dependências:

```
pip install -r requirements.txt
```

Passo 3: Suba a aplicação:

```
uvicorn app.main:app --reload --port 8001
```

Passo 4: Acesse a documentação em http://localhost:8001/docs
