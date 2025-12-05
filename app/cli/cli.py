from typing import Annotated

import typer

from app.cli import utils
from app.crud.usuario import get_password_hash
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import RoleEnum
from app.seed import gerar_dados

cli = typer.Typer(
    name="SSRFID-Backend CLI",
    pretty_exceptions_show_locals=False,
    no_args_is_help=True,
)


@cli.command("createsuperuser")
def createsuperuser():
    """Cria um superusuário no banco de dados."""

    db = SessionLocal()

    username = typer.prompt("Insira seu username: ", default="admin")

    if not utils.validate_username(username):
        typer.echo("O nome de usuário deve ter pelo menos 3 caracteres.")
        raise typer.Exit(code=1)

    password = typer.prompt("Insira sua senha: ", hide_input=True)
    confirm_password = typer.prompt("Confirme a senha: ", hide_input=True)
    if password != confirm_password:
        typer.echo("As senhas não coincidem. Tente novamente.")
        raise typer.Exit(code=1)

    admin = Usuario(username=username, password_hash=get_password_hash(password), role=RoleEnum.admin)
    db.add(admin)
    db.commit()
    typer.echo(f"Usuário {username} criado com sucesso!")
    db.close()


@cli.command("seed_db")
def seed_db(amount: Annotated[int, typer.Argument(help="Quantidade de produtos a serem criados")] = 50):
    """
    Gera dados de produtos aleatórios no banco de dados
    """
    gerar_dados(amount)
    typer.echo(f"Banco de dados populado com {amount} produtos")


if __name__ == "__main__":
    cli()
