from dotenv import load_dotenv
load_dotenv()
from itertools import islice
import csv
from src.elastic import es
from elasticsearch.helpers import bulk
from src.mongo import mongo
from pathlib import Path

if not Path('estabelecimentos.csv').is_file():
    raise SystemExit('Erro: arquivo estabelecimentos.csv não encontrado')

def gen_data(records):
    for rec in records:
        yield {
            "_index": "estabelecimentos",
        } | rec


with open('estabelecimentos.csv', newline='', encoding='latin-1') as f:
    reader = csv.reader(f, delimiter=';')
    rows = list(islice(reader, 0, 10))
    records = [
        {
        'cnpj': row[0]+row[1]+row[2],
        'nome_fantasia': row[4],
        'cep': row[18],
        'telefone': row[21]+row[22],
        'email': row[27]
        } for row in rows
    ]
    bulk(es, gen_data(records))

    coll = mongo.estabelecimentos
    coll.insert_many(records)
