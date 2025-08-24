
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.peca import Peca

# 10 categorias principais Toyota
CATEGORIAS = {
    1001: "Motor",
    1002: "Transmissão",
    1003: "Suspensão",
    1004: "Freios",
    1005: "Elétrica",
    1006: "Arrefecimento",
    1007: "Direção",
    1008: "Embreagem",
    1009: "Escape",
    1010: "Injeção"
}

pecas_modelos = [
    ("Filtro de Óleo", "Corolla", 1001),
    ("Filtro de Ar", "Corolla", 1001),
    ("Pastilha de Freio Dianteira", "Corolla", 1004),
    ("Pastilha de Freio Traseira", "Corolla", 1004),
    ("Amortecedor Dianteiro", "Hilux", 1003),
    ("Amortecedor Traseiro", "Hilux", 1003),
    ("Bateria", "Yaris", 1005),
    ("Velas de Ignição", "Etios", 1005),
    ("Correia Dentada", "Hilux", 1001),
    ("Radiador", "Corolla Cross", 1006),
    ("Alternador", "Hilux", 1005),
    ("Motor de Partida", "Corolla", 1005),
    ("Disco de Freio Dianteiro", "Corolla Cross", 1004),
    ("Disco de Freio Traseiro", "Corolla Cross", 1004),
    ("Bomba de Combustível", "Etios", 1010),
    ("Sensor de Oxigênio", "Yaris", 1010),
    ("Injetor", "Corolla", 1010),
    ("Kit Embreagem", "Hilux", 1008),
    ("Parabrisa", "Yaris", 1006),
    ("Retrovisor", "Corolla Cross", 1007),
    ("Catalisador", "Corolla", 1009),
    ("Sensor ABS", "Hilux", 1004),
    ("Bomba de Óleo", "Corolla", 1001),
    ("Coxim do Motor", "Yaris", 1001),
    ("Módulo de Injeção", "Etios", 1010),
    ("Cabo de Vela", "Corolla", 1005),
    ("Reservatório de Expansão", "Corolla Cross", 1006),
    ("Bomba de Direção Hidráulica", "Hilux", 1007),
    ("Sensor de Temperatura", "Yaris", 1006),
]

anos = [
    "2005-2007", "2008-2010", "2011-2013", "2014-2016", "2017-2019",
    "2020-2022", "2023-2024"
]

def gerar_dados(qtd):
    db: Session = SessionLocal()

    # Limpa tabela
    db.query(Peca).delete()
    db.commit()
    print("Tabela 'pecas' esvaziada.")

    pecas_criadas = 0

    for i in range(1, qtd + 1):
        nome, modelo, categoria_id = random.choice(pecas_modelos)
        ano = random.choice(anos)
        quantidade = random.randint(5, 50)
        preco_custo = round(random.uniform(50, 600), 2)
        preco_venda = round(preco_custo * random.uniform(1.3, 2.5), 2)
        localizacao = f"A{random.randint(1,5)}-{random.randint(1,10):02d}"
        
        peca = Peca(
            nome=f"{nome} - {modelo}",
            descricao=f"Peça genuína Toyota {nome}, compatível com {modelo} ({ano}). Categoria: {CATEGORIAS[categoria_id]}",
            localizacao=localizacao,
            quantidade=quantidade,
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            modelo_carro=modelo,
            ano_carro=ano,
            codigo_tipo=categoria_id
        )
        db.add(peca)
        pecas_criadas += 1

    db.commit()
    print(f"{pecas_criadas} peças inseridas com sucesso.")
    db.close()

if __name__ == "__main__":
    gerar_dados(100)