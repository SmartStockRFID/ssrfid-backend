import random
from sqlalchemy.orm import Session
from app.models.peca import Peca, Base
from app.database import engine, SessionLocal

nomes = [f"Peça {i}" for i in range(1, 101)]
descricoes = [f"Descrição da peça {i}" for i in range(1, 101)]
modelos_carro = [f"Modelo {chr(65 + i%10)}" for i in range(100)]
anos_carro = [f"{2000 + i%20}-{2000 + i%20 + 1}" for i in range(100)]
localizacoes = [f"A{random.randint(1,5)}-{str(random.randint(1,10)).zfill(2)}" for _ in range(100)]

Base.metadata.create_all(bind=engine)

def gerar_pecas():
    db: Session = SessionLocal()
    pecas = []
    for i in range(100):
        preco_custo = round(random.uniform(10, 500), 2)
        preco_venda = round(preco_custo + random.uniform(5, 100), 2)
        peca = Peca(
            nome=nomes[i],
            codigo_oem=f"OEM-{random.randint(10000,99999)}-{i}",
            descricao=descricoes[i],
            localizacao=localizacoes[i],
            quantidade=random.randint(1, 50),
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            modelo_carro=modelos_carro[i],
            ano_carro=anos_carro[i],
            rfid_uid=f"RFID-{random.randint(10000000,99999999)}"
        )
        pecas.append(peca)
    db.bulk_save_objects(pecas)
    db.commit()
    db.close()

if __name__ == "__main__":
    gerar_pecas()
