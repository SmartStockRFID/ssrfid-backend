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

anos = [
    "2005-2007", "2008-2010", "2011-2013", "2014-2016", "2017-2019",
    "2020-2022", "2023-2024"
]

def gerar_codigo_oem(indice):
    """Gera código OEM curto e único, ex: 123-001"""
    return f"{random.randint(100, 999)}-{indice:03d}"

def gerar_pecas(qtd):
    db: Session = SessionLocal()

    # Limpa a tabela
    db.query(Peca).delete()
    db.commit()
    print("Tabela 'pecas' esvaziada.")

    registros = []
    for i in range(1, qtd + 1):
        nome, modelo = random.choice(pecas_modelos)
        codigo_oem = gerar_codigo_oem(i)
        ano = random.choice(anos)
        quantidade = random.randint(5, 50)
        preco_custo = round(random.uniform(50, 600), 2)
        preco_venda = round(preco_custo * random.uniform(1.3, 2.5), 2)
        localizacao = f"A{random.randint(1,5)}-{random.randint(1,10):02d}"

        peca = Peca(
            nome=f"{nome} - {modelo}",
            codigo_oem=codigo_oem,
            descricao=f"Peça genuína Toyota {nome}, compatível com {modelo} ({ano}).",
            localizacao=localizacao,
            quantidade=quantidade,
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            modelo_carro=modelo,
            ano_carro=ano,
            rfid_uid=None  # deixa nulo para associar depois
        )
        registros.append(peca)

    db.add_all(registros)
    db.commit()
    print(f"{qtd} registros inseridos com sucesso.")

if __name__ == "__main__":
    gerar_pecas(100)