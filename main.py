from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

#Filmes
class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=True)
    genero = Column(String(100), nullable=True)
    ano_lancamento = Column(Integer, nullable=True)
    nota = Column(Float)
    disponivel = Column(Boolean, default=True)

    def __init__(self, nome_filme, genero_filme, ano_filme, nota_filme, disponivel=True):
        self.titulo = nome_filme
        self.genero = genero_filme
        self.ano_lancamento = ano_filme
        self.nota = nota_filme
        self.disponivel = disponivel

engine = create_engine("sqlite:///catalogo_filmes.db")

#Criar as tabelas
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# Criar funções CRUD
def cadastrar_filme():
    print(f"\n--- CADASTRAR FILMES ---")
    nome_filme = input("Digite o título do filme: ")
    genero = input("Digite o gênero do filme: ")
    ano = int(input("Digite o ano de lançamento do filme: "))
    nota = float(input("Digite a nota do filme: "))

    with Session() as session:
        try:
            #Verificar o titulo duplicado
            buscar_filme = session.query(Filme).filter_by(titulo=nome_filme, ano_lancamento=ano).first()
            if buscar_filme == None:
                novo_filme = Filme(nome_filme, genero, ano, nota)
                session.add(novo_filme)
                session.commit()
                print("Filme cadastrado com sucesso")
            else:
                print("Já existe um filme com esse título e ano")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def listar_filme():

    with Session() as session:
        try:
            buscar_filme = session.query(Filme).all()
            for filme in buscar_filme:
                print(f"Título: {filme.titulo} | Gênero: {filme.genero} | Ano: {filme.ano_lancamento} | Nota: {filme.nota}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
listar_filme()

def atualizar_filme():
    id_filme = int(input("\n Digite o ID do filme que deseja atualizar: "))    
    with Session() as session:
        try:
            filme = session.query(Filme).filter_by(id=id_filme).first()
            if filme:
                filme.titulo = input(f"Novo título: ")
                filme.genero = input(f"Novo gênero: ")
                filme.ano_lancamento = int(input(f"Novo ano: "))
                filme.nota = float(input(f"Nova nota: "))

                session.commit()
                print("Filme atualizado com sucesso!")
                print(f"Título: {filme.titulo} | Gênero: {filme.genero} | Ano: {filme.ano_lancamento} | Nota: {filme.nota}")
            else:
                print("Filme não encontrado.")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")

atualizar_filme()



#Criar as funções listar, atualizar e deletar
cadastrar_filme()


