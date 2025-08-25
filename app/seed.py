import random

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.peca import Peca

# Categorias principais
CATEGORIAS = {"FILTRO": "Filtro", "FREIO": "Freio", "SUSP": "Suspensão", "ELETR": "Elétrico", "MOTOR": "Motor"}

pecas_modelos = [
    ("Filtro de Óleo", "Corolla", "FILTRO"),
    ("Filtro de Ar", "Corolla", "FILTRO"),
    ("Pastilha de Freio Dianteira", "Corolla", "FREIO"),
    ("Pastilha de Freio Traseira", "Corolla", "FREIO"),
    ("Amortecedor Dianteiro", "Hilux", "SUSP"),
    ("Amortecedor Traseiro", "Hilux", "SUSP"),
    ("Bateria", "Yaris", "ELETR"),
    ("Velas de Ignição", "Etios", "ELETR"),
    ("Correia Dentada", "Hilux", "MOTOR"),
    ("Radiador", "Corolla Cross", "MOTOR"),
    ("Alternador", "Hilux", "ELETR"),
    ("Motor de Partida", "Corolla", "ELETR"),
    ("Disco de Freio Dianteiro", "Corolla Cross", "FREIO"),
    ("Disco de Freio Traseiro", "Corolla Cross", "FREIO"),
    ("Bomba de Combustível", "Etios", "MOTOR"),
    ("Sensor de Oxigênio", "Yaris", "ELETR"),
    ("Injetor", "Corolla", "MOTOR"),
    ("Kit Embreagem", "Hilux", "MOTOR"),
    ("Parabrisa", "Yaris", "SUSP"),
    ("Retrovisor", "Corolla Cross", "SUSP"),
]

anos = ["2005-2007", "2008-2010", "2011-2013", "2014-2016", "2017-2019", "2020-2022", "2023-2024"]


def gerar_codigo_oem(categoria, modelo, serial):
    # Exemplo: FREIO-COROLLA-001
    return f"{categoria}-{modelo.upper().replace(' ', '')}-{serial:03d}"


def gerar_pecas(qtd):
    db: Session = SessionLocal()

    # Limpa a tabela
    db.query(Peca).delete()
    db.commit()
    print("Tabela 'pecas' esvaziada.")

    registros = []
    usados = set()
    for i in range(1, qtd + 1):
        nome, modelo, categoria = random.choice(pecas_modelos)
        serial = i
        codigo_oem = gerar_codigo_oem(categoria, modelo, serial)

        while codigo_oem in usados:
            serial += 1
            codigo_oem = gerar_codigo_oem(categoria, modelo, serial)
        usados.add(codigo_oem)

        ano = random.choice(anos)
        localizacao = f"S{random.randint(1, 5)}-P{random.randint(1, 20):02d}"

        peca = Peca(
            nome=f"{nome} - {modelo}",
            codigo_produto=codigo_oem,
            descricao=f"Peça genuína Toyota {nome}, compatível com {modelo} ({ano}). Categoria: {CATEGORIAS[categoria]}",
            localizacao=localizacao,
        )
        registros.append(peca)

    db.add_all(registros)
    db.commit()
    print(f"{qtd} categorias de produto inseridas com sucesso.")


if __name__ == "__main__":
    gerar_pecas(100)
