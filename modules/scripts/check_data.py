# scripts/check_data.py
from modules.utils.data_handler import DataRepository
repo = DataRepository()

print(repo.healthcheck())              # contagens por tabela
print(repo.load_financas().head(3))    # amostra
print(repo.load_estoque_snapshot().head(3))
print(repo.load_publico_alvo().head(3))
print(repo.load_rh().head(3))
print(repo.load_fornecedores().head(3))