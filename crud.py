from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Banco de dados
db = create_engine("sqlite:///banco.db", echo=True)
Session = sessionmaker(bind=db)()
Base = declarative_base()

# Tabela Aluno
class Aluno(Base):
    __tablename__ = "Alunos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String, nullable=False)
    nome = Column(String, nullable=False)

    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome

# Tabela Media
class Media(Base):
    __tablename__ = "Medias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nota1 = Column(Numeric, nullable=True)
    nota2 = Column(Numeric, nullable=True)
    media = Column(Numeric, nullable=True)
    aluno_id = Column(Integer, ForeignKey("Alunos.id"), nullable=False)

    def __init__(self, nota1, nota2, media, aluno_id):
        self.nota1 = nota1
        self.nota2 = nota2
        self.media = media
        self.aluno_id = aluno_id

Base.metadata.create_all(db)

# Menu
def menu_crud():
    os.system("cls" if os.name == "nt" else "clear")
    print("Funções: [1]-Criar [2]-Ler [3]-Atualizar [4]-Deletar")
    escolha = int(input("Qual função você deseja iniciar: "))
    if escolha == 1:
        criacao()
    elif escolha == 2:
        ler()
    elif escolha == 3:
        update()
    elif escolha == 4:
        delete()
    else:
        print("Função não encontrada!!!")

# Criar
def criacao():
    os.system("cls" if os.name == "nt" else "clear")
    print("Apresente o Aluno")
    nome = input("Informe o nome do aluno: ")
    cpf = input("Informe o CPF do aluno: ")
    
    novoaluno = Aluno(cpf=cpf, nome=nome)
    Session.add(novoaluno)
    Session.commit()
    Session.refresh(novoaluno)

    try:
        nota1 = float(input("Qual nota o aluno tirou na primeira avaliação: "))
        nota2 = float(input("Qual a segunda nota do aluno: "))
    except ValueError:
        print("Valor inválido.")
        return menu_crud()

    media = (nota1 + nota2) / 2
    print(f"O aluno {nome} portador do CPF {cpf} ficou com média {media:.2f}")
    
    adicao_das_notas = Media(
        nota1=nota1, 
        nota2=nota2, 
        media=media,
        aluno_id=novoaluno.id
    )
    Session.add(adicao_das_notas)
    Session.commit()
    menu_crud()

# Ler
def ler():
    cpf = input("Informe o CPF do aluno: ")
    aluno = Session.query(Aluno).filter_by(cpf=cpf).first()
    if not aluno:
        print("Nenhum usuário encontrado.")
    else:
        print(f"Nome: {aluno.nome} | CPF: {aluno.cpf}")
        notas = Session.query(Media).filter_by(aluno_id=aluno.id).first()
        if notas:
            print(f"Nota 1: {notas.nota1} | Nota 2: {notas.nota2} | Média: {notas.media}")
    input("Pressione Enter para continuar...")
    menu_crud()

# Atualizar
def update():
    cpf = input("Informe o CPF do aluno: ")
    aluno = Session.query(Aluno).filter_by(cpf=cpf).first()
    if not aluno:
        print("Aluno não encontrado.")
        return menu_crud()

    notas = Session.query(Media).filter_by(aluno_id=aluno.id).first()
    if not notas:
        print("Notas não encontradas para esse aluno.")
        return menu_crud()

    nota1 = float(input("Nova nota 1: "))
    nota2 = float(input("Nova nota 2: "))
    notas.nota1 = nota1
    notas.nota2 = nota2
    notas.media = (nota1 + nota2) / 2
    Session.commit()
    print("Notas atualizadas com sucesso!")
    menu_crud()

# Deletar
def delete():
    cpf = input("Informe o CPF do aluno: ")
    aluno = Session.query(Aluno).filter_by(cpf=cpf).first()
    if not aluno:
        print("Aluno não encontrado.")
    else:
        Session.query(Media).filter_by(aluno_id=aluno.id).delete()
        Session.delete(aluno)
        Session.commit()
        print("Aluno e notas deletados com sucesso!")
    menu_crud()

# Iniciar o menu
menu_crud()
