

import random

import random

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.peca import Peca
from app.models.usuario import Usuario, Base as UsuarioBase
from app.crud.usuario import get_password_hash

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

# Lista realista de peças Toyota (nome, modelo, categoria_id, descrição)
pecas_modelos = [
    ("Filtro de Óleo", "Corolla", 1001, "Filtro de óleo genuíno para motores Toyota Corolla."),
    ("Filtro de Ar", "Corolla", 1001, "Filtro de ar genuíno para motores Toyota Corolla."),
    ("Pastilha de Freio Dianteira", "Corolla", 1004, "Pastilha dianteira original para sistema de freios do Corolla."),
    ("Pastilha de Freio Traseira", "Corolla", 1004, "Pastilha traseira original para sistema de freios do Corolla."),
    ("Amortecedor Dianteiro", "Hilux", 1003, "Amortecedor dianteiro genuíno para Toyota Hilux."),
    ("Amortecedor Traseiro", "Hilux", 1003, "Amortecedor traseiro genuíno para Toyota Hilux."),
    ("Bateria", "Yaris", 1005, "Bateria original para Toyota Yaris."),
    ("Velas de Ignição", "Etios", 1005, "Velas de ignição genuínas para Toyota Etios."),
    ("Correia Dentada", "Hilux", 1001, "Correia dentada original para motores Hilux."),
    ("Radiador", "Corolla Cross", 1006, "Radiador genuíno para sistema de arrefecimento do Corolla Cross."),
    ("Alternador", "Hilux", 1005, "Alternador genuíno para Toyota Hilux."),
    ("Motor de Partida", "Corolla", 1005, "Motor de partida original para Toyota Corolla."),
    ("Disco de Freio Dianteiro", "Corolla Cross", 1004, "Disco dianteiro original para sistema de freios do Corolla Cross."),
    ("Disco de Freio Traseiro", "Corolla Cross", 1004, "Disco traseiro original para sistema de freios do Corolla Cross."),
    ("Bomba de Combustível", "Etios", 1010, "Bomba de combustível genuína para Toyota Etios."),
    ("Sensor de Oxigênio", "Yaris", 1010, "Sensor de oxigênio genuíno para Toyota Yaris."),
    ("Injetor", "Corolla", 1010, "Injetor de combustível original para Toyota Corolla."),
    ("Kit Embreagem", "Hilux", 1008, "Kit de embreagem genuíno para Toyota Hilux."),
    ("Parabrisa", "Yaris", 1006, "Parabrisa genuíno para Toyota Yaris."),
    ("Retrovisor", "Corolla Cross", 1007, "Retrovisor genuíno para Toyota Corolla Cross."),
    ("Catalisador", "Corolla", 1009, "Catalisador original para sistema de escape do Corolla."),
    ("Sensor ABS", "Hilux", 1004, "Sensor ABS genuíno para sistema de freios da Hilux."),
    ("Bomba de Óleo", "Corolla", 1001, "Bomba de óleo genuína para motores Corolla."),
    ("Coxim do Motor", "Yaris", 1001, "Coxim do motor genuíno para Toyota Yaris."),
    ("Módulo de Injeção", "Etios", 1010, "Módulo de injeção eletrônica para Toyota Etios."),
    ("Cabo de Vela", "Corolla", 1005, "Cabo de vela genuíno para Toyota Corolla."),
    ("Reservatório de Expansão", "Corolla Cross", 1006, "Reservatório de expansão genuíno para Corolla Cross."),
    ("Bomba de Direção Hidráulica", "Hilux", 1007, "Bomba de direção hidráulica genuína para Hilux."),
    ("Sensor de Temperatura", "Yaris", 1006, "Sensor de temperatura genuíno para Toyota Yaris."),
]

anos = [
    "2005-2007",
    "2008-2010",
    "2011-2013",
    "2014-2016",
    "2017-2019",
    "2020-2022",
    "2023-2024",
]


def gerar_codigo_oem(categoria_id, serial):
    # Exemplo: 1001-0001
    return f"{categoria_id:04d}-{serial:04d}"

def resetar_id_pecas(db):
    # PostgreSQL: resetar sequência de id para 1
    db.execute(text("ALTER SEQUENCE pecas_id_seq RESTART WITH 1"))
    db.commit()

def criar_tabelas():
    from app.models.peca import Base as PecaBase
    PecaBase.metadata.create_all(bind=engine)
    UsuarioBase.metadata.create_all(bind=engine)

def criar_admin(db):
    if not db.query(Usuario).filter(Usuario.username == "admin").first():
        admin = Usuario(
            username="admin",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe.")


def gerar_pecas(qtd):
    db: Session = SessionLocal()

    criar_tabelas()
    criar_admin(db)

    # Limpa a tabela de peças
    db.query(Peca).delete()
    db.commit()
    resetar_id_pecas(db)
    print("Tabela 'pecas' esvaziada e IDs resetados.")

    registros = []
    usados = set()
    serials_categoria = {cat: 1 for cat in CATEGORIAS.keys()}
    for i in range(1, qtd + 1):
        nome, modelo, categoria_id, descricao = random.choice(pecas_modelos)
        serial = serials_categoria[categoria_id]
        codigo_oem = gerar_codigo_oem(categoria_id, serial)
        while codigo_oem in usados:
            serials_categoria[categoria_id] += 1
            serial = serials_categoria[categoria_id]
            codigo_oem = gerar_codigo_oem(categoria_id, serial)
        usados.add(codigo_oem)
        serials_categoria[categoria_id] += 1
        ano = random.choice(anos)
        quantidade = random.randint(5, 50)
        preco_custo = round(random.uniform(50, 600), 2)
        preco_venda = round(preco_custo * random.uniform(1.3, 2.5), 2)
        localizacao = f"A{random.randint(1, 5)}-{random.randint(1, 10):02d}"

        peca = Peca(
            nome=f"{nome} - {modelo}",
            codigo_oem=codigo_oem,
            descricao=f"{descricao} Compatível com {modelo} ({ano}). Categoria: {CATEGORIAS[categoria_id]}",
            localizacao=localizacao,
            quantidade=quantidade,
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            modelo_carro=modelo,
            ano_carro=ano,
            rfid_uid=None,  # deixa nulo para associar depois
        )
        registros.append(peca)

    db.add_all(registros)
    db.commit()
    print(f"{qtd} registros inseridos com sucesso.")
    db.close()


if __name__ == "__main__":
    gerar_pecas(100)
