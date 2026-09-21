# TravelPlan - Trip Service (API Secundária)

## Descrição

API responsável pela regra de negócio do TravelPlan: recebe uma cidade e um
período de datas, consulta a previsão do tempo na API externa **Open-Meteo**
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

Documentação interativa (Swagger) disponível em `/docs` após subir a aplicação.

## Instalação e execução local (sem Docker)

1. Crie e ative um ambiente virtual:

python -m venv .venv

.venv\Scripts\activate

2. Instale as dependências:

pip install -r requirements.txt

3. Suba a aplicação:

uvicorn app.main:app --reload --port 8001

4. Acesse a documentação em http://localhost:8001/docs

## Execução via Docker

docker build -t trip-service .

docker run -p 8001:8001 --name trip-service trip-service
