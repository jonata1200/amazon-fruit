# scripts/migrate_excel_to_sqlite.py

import sqlite3
from pathlib import Path
import pandas as pd
import re
from functools import lru_cache
from calendar import monthrange

# ==============================================================================
# --- MUDANÇA: A classe DataRepository foi movida para DENTRO deste script ---
# Agora este script é autossuficiente e não depende mais do 'data_handler.py'
# ==============================================================================
project_root = Path(__file__).resolve().parents[1]
BASE_DIR = project_root / "data"
MESES = {"Jan":1,"Fev":2,"Mar":3,"Abr":4,"Mai":5,"Jun":6,"Jul":7,"Ago":8,"Set":9,"Out":10,"Nov":11,"Dez":12}
SHEET_RGX = re.compile(r"^(\d{2})-([A-Za-z]{3})$")
def _sheet_to_period(sheet_name: str) -> tuple[int, int]:
    m = SHEET_RGX.match(str(sheet_name).strip());
    if not m: raise ValueError(f"Aba fora do padrão 'MM-Mmm': {sheet_name}");
    mm, mmm = int(m.group(1)), m.group(2).title();
    return MESES.get(mmm, mm), MESES.get(mmm, mm)
def _last_day(ano: int, mes: int) -> str:
    return f"{ano:04d}-{mes:02d}-{monthrange(ano, mes)[1]:02d}"

class DataRepository:
    def __init__(self, base_dir: Path | str | None = None):
        self.base_dir: Path = Path(base_dir) if base_dir is not None else BASE_DIR
    def _iter_year_files(self, subdir: str, filename: str):
        raiz = self.base_dir / subdir
        if not raiz.exists(): return
        for ano_dir in sorted(raiz.iterdir()):
            if not ano_dir.is_dir(): continue
            fp = ano_dir / filename
            if fp.exists():
                try: ano_int = int(ano_dir.name)
                except ValueError: continue
                yield ano_int, fp
    @lru_cache(maxsize=1)
    def load_fornecedores(self) -> pd.DataFrame:
        path = self.base_dir / "fornecedores" / "fornecedores.xlsx"; df = pd.read_excel(path, sheet_name=0, engine="openpyxl"); df["ID_Fornecedor"] = pd.to_numeric(df["ID_Fornecedor"], errors="coerce").astype("Int64"); df["Avaliacao"] = pd.to_numeric(df["Avaliacao"], errors="coerce"); return df
    @lru_cache(maxsize=1)
    def load_rh(self) -> pd.DataFrame:
        path = self.base_dir / "recursos_humanos" / "recursos_humanos.xlsx"; df = pd.read_excel(path, sheet_name=0, engine="openpyxl"); df["ID_Funcionario"] = pd.to_numeric(df["ID_Funcionario"], errors="coerce").astype("Int64"); df["Data_Contratacao"] = pd.to_datetime(df["Data_Contratacao"], errors="coerce"); df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce"); return df
    @lru_cache(maxsize=1)
    def load_financas(self) -> pd.DataFrame:
        frames = []
        for ano, fp in self._iter_year_files("financas", "financas.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names:
                mes, _ = _sheet_to_period(sheet)
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Data"] = pd.to_datetime(df.get("Data"), errors="coerce")
                df["Ano"] = ano
                df["Mes"] = mes
                frames.append(df)
        if not frames: return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True); df["ID_Lancamento"] = pd.to_numeric(df.get("ID_Lancamento"), errors="coerce").astype("Int64"); df["Valor"] = pd.to_numeric(df.get("Valor"), errors="coerce")
        if "ID_Produto" in df.columns: df["ID_Produto"] = pd.to_numeric(df["ID_Produto"], errors="coerce").astype("Int64")
        return df
    @lru_cache(maxsize=1)
    def load_estoque_snapshot(self) -> pd.DataFrame:
        frames = [];
        for ano, fp in self._iter_year_files("estoque", "estoque.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names: mes, _ = _sheet_to_period(sheet); df = pd.read_excel(xls, sheet_name=sheet); df["Ano"] = ano; df["Mes"] = mes; df["Data_Validade"] = pd.to_datetime(df.get("Data_Validade"), errors="coerce"); df["Data_Snapshot"] = pd.to_datetime(_last_day(ano, mes)); frames.append(df)
        if not frames: return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True); df["ID_Produto"] = pd.to_numeric(df.get("ID_Produto"), errors="coerce").astype("Int64");
        for c in ["Quantidade_Estoque", "Preco_Custo", "Preco_Venda", "Nivel_Minimo_Estoque"]:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
        return df
    @lru_cache(maxsize=1)
    def load_publico_alvo(self) -> pd.DataFrame:
        frames = [];
        for ano, fp in self._iter_year_files("publico_alvo", "publico_alvo.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names: mes, _ = _sheet_to_period(sheet); df = pd.read_excel(xls, sheet_name=sheet); df["Ano"] = ano; df["Mes"] = mes; frames.append(df)
        if not frames: return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True);
        if "ID_Cliente" in df.columns: df["ID_Cliente"] = pd.to_numeric(df["ID_Cliente"], errors="coerce").astype("Int64")
        if "Idade" in df.columns: df["Idade"] = pd.to_numeric(df["Idade"], errors="coerce")
        return df
# ==============================================================================
# --- FIM DO CÓDIGO MOVIDO ---
# ==============================================================================

# --- CONFIGURAÇÃO ---
DB_PATH = project_root / 'data' / 'amazon_fruit.db'
DB_PATH.parent.mkdir(exist_ok=True)

TABLE_MAP = {
    'Estoque': 'estoque_historico', 'Financas': 'lancamentos_financeiros',
    'Fornecedores': 'fornecedores', 'Publico_Alvo': 'clientes',
    'Recursos_Humanos': 'funcionarios'
}

def migrate():
    print("Iniciando a migração de dados de Excel para SQLite...")
    conn = sqlite3.connect(DB_PATH)
    print(f"Banco de dados conectado em: {DB_PATH}")
    
    # Usa a classe DataRepository que agora está DENTRO deste arquivo
    repo = DataRepository()

    print("Carregando dados dos arquivos Excel (já corrigidos)...")
    datasets = {
        "Fornecedores": repo.load_fornecedores(), "Recursos_Humanos": repo.load_rh(),
        "Financas": repo.load_financas(), "Estoque": repo.load_estoque_snapshot(),
        "Publico_Alvo": repo.load_publico_alvo()
    }
    print("Dados carregados com sucesso.")

    for name, df in datasets.items():
        table_name = TABLE_MAP.get(name)
        if df.empty:
            print(f"-> Aviso: DataFrame '{name}' está vazio. Pulando a tabela '{table_name}'.")
            continue
        try:
            print(f"-> Escrevendo {len(df)} linhas na tabela '{table_name}'...")
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"   Tabela '{table_name}' criada com sucesso.")
        except Exception as e:
            print(f"   ERRO ao escrever na tabela '{table_name}': {e}")

    conn.close()
    print("\nMigração de dados para SQLite concluída com sucesso!")

if __name__ == '__main__':
    migrate()