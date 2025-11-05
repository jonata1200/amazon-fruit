# utils/data_handler.py

from __future__ import annotations
import re
from pathlib import Path
from functools import lru_cache
import pandas as pd
from calendar import monthrange

# Nenhuma mudança na seção inicial
BASE_DIR = Path(__file__).resolve().parents[2] / "data"
MESES = {"Jan":1,"Fev":2,"Mar":3,"Abr":4,"Mai":5,"Jun":6,"Jul":7,"Ago":8,"Set":9,"Out":10,"Nov":11,"Dez":12}
SHEET_RGX = re.compile(r"^(\d{2})-([A-Za-z]{3})$")

def _sheet_to_period(sheet_name: str) -> tuple[int, int]:
    m = SHEET_RGX.match(str(sheet_name).strip())
    if not m:
        raise ValueError(f"Aba fora do padrão 'MM-Mmm': {sheet_name}")
    mm, mmm = int(m.group(1)), m.group(2).title()
    mes = MESES.get(mmm, mm)
    return mes, mes

def _last_day(ano: int, mes: int) -> str:
    return f"{ano:04d}-{mes:02d}-{monthrange(ano, mes)[1]:02d}"


# ================================================================
# NENHUMA MUDANÇA NECESSÁRIA NA CLASSE DataRepository
# Sua lógica de leitura de arquivos já é ótima.
# ================================================================
class DataRepository:
    def __init__(self, base_dir: Path | str | None = None):
        p = Path(base_dir) if base_dir is not None else BASE_DIR
        if p.suffix.lower() == ".db" or p.is_file():
            p = p.parent
        rh_rel = Path("recursos_humanos") / "recursos_humanos.xlsx"
        if not (p / rh_rel).exists():
            default_base = BASE_DIR
            if (default_base / rh_rel).exists():
                p = default_base
        self.base_dir: Path = p

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
        path = self.base_dir / "fornecedores" / "fornecedores.xlsx"
        df = pd.read_excel(path, sheet_name=0, engine="openpyxl")
        df["ID_Fornecedor"] = pd.to_numeric(df["ID_Fornecedor"], errors="coerce").astype("Int64")
        df["Avaliacao"] = pd.to_numeric(df["Avaliacao"], errors="coerce")
        return df

    @lru_cache(maxsize=1)
    def load_rh(self) -> pd.DataFrame:
        path = self.base_dir / "recursos_humanos" / "recursos_humanos.xlsx"
        df = pd.read_excel(path, sheet_name=0, engine="openpyxl")
        df["ID_Funcionario"] = pd.to_numeric(df["ID_Funcionario"], errors="coerce").astype("Int64")
        df["Data_Contratacao"] = pd.to_datetime(df["Data_Contratacao"], errors="coerce")
        df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce")
        return df

    @lru_cache(maxsize=1)
    def load_financas(self) -> pd.DataFrame:
        frames = []
        for ano, fp in self._iter_year_files("financas", "financas.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names:
                mes, _ = _sheet_to_period(sheet)
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Data"] = pd.to_datetime(df.get("Data"), errors="coerce")
                df["Ano"] = ano; df["Mes"] = mes
                frames.append(df)
        if not frames: return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
        df["ID_Lancamento"] = pd.to_numeric(df.get("ID_Lancamento"), errors="coerce").astype("Int64")
        df["Valor"] = pd.to_numeric(df.get("Valor"), errors="coerce")
        return df

    @lru_cache(maxsize=1)
    def load_estoque_snapshot(self) -> pd.DataFrame:
        frames = []
        for ano, fp in self._iter_year_files("estoque", "estoque.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names:
                mes, _ = _sheet_to_period(sheet)
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Ano"] = ano; df["Mes"] = mes
                df["Data_Validade"] = pd.to_datetime(df.get("Data_Validade"), errors="coerce")
                df["Data_Snapshot"] = pd.to_datetime(_last_day(ano, mes))
                frames.append(df)
        if not frames: return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
        df["ID_Produto"] = pd.to_numeric(df.get("ID_Produto"), errors="coerce").astype("Int64")
        for c in ["Quantidade_Estoque", "Preco_Custo", "Preco_Venda", "Nivel_Minimo_Estoque"]:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
        return df

    @lru_cache(maxsize=1)
    def load_publico_alvo(self) -> pd.DataFrame:
        frames = []
        for ano, fp in self._iter_year_files("publico_alvo", "publico_alvo.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names:
                mes, _ = _sheet_to_period(sheet)
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Ano"] = ano; df["Mes"] = mes
                frames.append(df)
        if not frames: return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
        if "ID_Cliente" in df.columns: df["ID_Cliente"] = pd.to_numeric(df["ID_Cliente"], errors="coerce").astype("Int64")
        if "Idade" in df.columns: df["Idade"] = pd.to_numeric(df["Idade"], errors="coerce")
        return df

# ================================================================
# TODAS AS MUDANÇAS ESTÃO CONCENTRADAS AQUI, NA CLASSE DataHandler
# ================================================================
__all__ = ["DataRepository", "DataHandler"]

class DataHandler:
    """Fachada que gerencia o acesso aos dados e aplica filtros globais, como o de período."""
    def __init__(self, base_dir: Path | str | None = None):
        self._repo = DataRepository(base_dir)
        # (1) Atributos para armazenar o período selecionado pelo usuário.
        self.start_date: pd.Timestamp | None = None
        self.end_date: pd.Timestamp | None = None

    # (2) Novo método para ser chamado pela UI quando o período mudar.
    def set_period(self, start_iso: str, end_iso: str):
        """Define o período de filtro e limpa o cache dos dados temporais."""
        self.start_date = pd.to_datetime(start_iso, errors='coerce')
        self.end_date = pd.to_datetime(end_iso, errors='coerce')
        
        # ESSENCIAL: Limpa o cache para que os dados sejam recarregados e filtrados.
        self._repo.load_financas.cache_clear()
        self._repo.load_estoque_snapshot.cache_clear()
        # self._repo.load_publico_alvo.cache_clear() # Não precisa, pois não tem filtro de data

    # (3) Novo método para o gerador de relatórios saber o período atual.
    def get_period(self) -> tuple[str, str] | None:
        """Retorna o período atual formatado para exibição."""
        if self.start_date and self.end_date:
            return self.start_date.strftime('%d/%m/%Y'), self.end_date.strftime('%d/%m/%Y')
        return None

    # (4) Método principal modificado para APLICAR o filtro.
    def load_table(self, name: str) -> pd.DataFrame:
        """
        Carrega uma tabela de dados. Se um período estiver definido,
        aplica o filtro para tabelas que contenham uma coluna de data.
        """
        key = str(name).strip().lower()
        df = pd.DataFrame()

        # Carrega o DataFrame COMPLETO a partir do repositório
        if key in ("financas", "financeiro", "finance"):
            df = self._repo.load_financas()
            # Aplica o filtro se o período estiver definido e a coluna 'Data' existir
            if not df.empty and 'Data' in df.columns and self.start_date and self.end_date:
                df = df[df['Data'].between(self.start_date, self.end_date)]

        elif key in ("estoque", "inventory"):
            df = self._repo.load_estoque_snapshot()
            # Aplica o filtro na coluna de 'Data_Snapshot'
            if not df.empty and 'Data_Snapshot' in df.columns and self.start_date and self.end_date:
                df = df[df['Data_Snapshot'].between(self.start_date, self.end_date)]

        # Dados sem linha do tempo são carregados normalmente, sem filtro.
        elif key in ("publico_alvo", "publico", "public"):
            df = self._repo.load_publico_alvo()
        elif key in ("recursos_humanos", "rh", "recursos-humanos"):
            df = self._repo.load_rh()
        elif key in ("fornecedores", "supplier", "suppliers"):
            df = self._repo.load_fornecedores()
        else:
            raise ValueError(f"Tabela desconhecida: {name}")
            
        return df

    def healthcheck(self):
        return self._repo.healthcheck()