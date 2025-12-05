import random

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.peca import Peca

pecas_modelos = [
    ("Filtro de Óleo", "Corolla"),
    ("Filtro de Ar", "Corolla"),
    ("Pastilha de Freio Dianteira", "Corolla"),
    ("Pastilha de Freio Traseira", "Corolla"),
    ("Amortecedor Dianteiro", "Hilux"),
    ("Amortecedor Traseiro", "Hilux"),
    ("Bateria", "Yaris"),
    ("Velas de Ignição", "Etios"),
    ("Correia Dentada", "Hilux"),
    ("Radiador", "Corolla Cross"),
    ("Alternador", "Hilux"),
    ("Motor de Partida", "Corolla"),
    ("Disco de Freio Dianteiro", "Corolla Cross"),
    ("Disco de Freio Traseiro", "Corolla Cross"),
    ("Bomba de Combustível", "Etios"),
    ("Sensor de Oxigênio", "Yaris"),
    ("Injetor", "Corolla"),
    ("Kit Embreagem", "Hilux"),
    ("Parabrisa", "Yaris"),
    ("Retrovisor", "Corolla Cross"),
]

anos = ["2005-2007", "2008-2010", "2011-2013", "2014-2016", "2017-2019", "2020-2022", "2023-2024"]


def gerar_dados(qtd):
    db: Session = SessionLocal()
    db.query(Peca).delete()
    db.commit()
    print("Tabela 'pecas' esvaziada.")

    usados = set()
    pecas_criadas = 0
    for i in range(1, qtd + 1):
        nome, modelo = random.choice(pecas_modelos)
        ano = random.choice(anos)
        codigo_produto = f"{nome[:3].upper()}{modelo[:3].upper()}{ano[-2:]}{i:03d}"
        if codigo_produto in usados:
            continue
        usados.add(codigo_produto)
        descricao = f"Peça genuína Toyota {nome}, compatível com {modelo} ({ano})."
        localizacao = f"A{random.randint(1, 5)}-{random.randint(1, 10):02d}"
        peca = Peca(
            nome=f"{nome} - {modelo}",
            codigo_produto=codigo_produto,
            descricao=descricao,
            localizacao=localizacao,
        )
        db.add(peca)
        pecas_criadas += 1
    db.commit()
    print(f"{pecas_criadas} peças inseridas com sucesso.")
    db.close()


if __name__ == "__main__":
    gerar_dados(100)
