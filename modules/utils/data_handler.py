# modules/utils/data_handler.py

from __future__ import annotations
import re
from pathlib import Path
from functools import lru_cache
import pandas as pd
from calendar import monthrange

# O início do arquivo e a classe DataRepository permanecem os mesmos
BASE_DIR = Path(__file__).resolve().parents[2] / "data"
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
    # ... (toda a classe DataRepository permanece inalterada) ...
    def __init__(self, base_dir: Path | str | None = None):
        p = Path(base_dir) if base_dir is not None else BASE_DIR;
        if p.suffix.lower() == ".db" or p.is_file(): p = p.parent
        rh_rel = Path("recursos_humanos") / "recursos_humanos.xlsx"
        if not (p / rh_rel).exists():
            default_base = BASE_DIR
            if (default_base / rh_rel).exists(): p = default_base
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
        path = self.base_dir / "fornecedores" / "fornecedores.xlsx"; df = pd.read_excel(path, sheet_name=0, engine="openpyxl"); df["ID_Fornecedor"] = pd.to_numeric(df["ID_Fornecedor"], errors="coerce").astype("Int64"); df["Avaliacao"] = pd.to_numeric(df["Avaliacao"], errors="coerce"); return df
    @lru_cache(maxsize=1)
    def load_rh(self) -> pd.DataFrame:
        path = self.base_dir / "recursos_humanos" / "recursos_humanos.xlsx"; df = pd.read_excel(path, sheet_name=0, engine="openpyxl"); df["ID_Funcionario"] = pd.to_numeric(df["ID_Funcionario"], errors="coerce").astype("Int64"); df["Data_Contratacao"] = pd.to_datetime(df["Data_Contratacao"], errors="coerce"); df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce"); return df
    @lru_cache(maxsize=1)
    def load_financas(self) -> pd.DataFrame:
        """Concatena todos os anos/abas e retorna uma tabela única de lançamentos."""
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
        if not frames:
            return pd.DataFrame()
        
        df = pd.concat(frames, ignore_index=True)
        df["ID_Lancamento"] = pd.to_numeric(df.get("ID_Lancamento"), errors="coerce").astype("Int64")
        df["Valor"] = pd.to_numeric(df.get("Valor"), errors="coerce")
        
        # --- CORREÇÃO ADICIONADA AQUI ---
        # Garante que a coluna ID_Produto, se existir, seja do mesmo tipo que na tabela de estoque.
        if "ID_Produto" in df.columns:
            df["ID_Produto"] = pd.to_numeric(df["ID_Produto"], errors="coerce").astype("Int64")
            
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

__all__ = ["DataRepository", "DataHandler"]

class DataHandler:
    def __init__(self, base_dir: Path | str | None = None):
        self._repo = DataRepository(base_dir)
        self.start_date: pd.Timestamp | None = None
        self.end_date: pd.Timestamp | None = None

    def set_period(self, start_iso: str, end_iso: str):
        self.start_date = pd.to_datetime(start_iso, errors='coerce')
        self.end_date = pd.to_datetime(end_iso, errors='coerce')
        self._repo.load_financas.cache_clear()
        self._repo.load_estoque_snapshot.cache_clear()
        self._repo.load_publico_alvo.cache_clear()
        self._repo.load_rh.cache_clear()

    def get_period(self) -> tuple[str, str] | None:
        if self.start_date and self.end_date:
            return self.start_date.strftime('%d/%m/%Y'), self.end_date.strftime('%d/%m/%Y')
        return None

    def load_table(self, name: str) -> pd.DataFrame:
        df = self._load_table_by_name(name)
        if df.empty: return df
        
        date_col_map = {
            "financas": "Data",
            "estoque": "Data_Snapshot",
            "recursos_humanos": "Data_Contratacao"
        }
        date_col = date_col_map.get(name.lower())
        
        if date_col and date_col in df.columns and self.start_date and self.end_date:
            return df[df[date_col].between(self.start_date, self.end_date)]
            
        return df

    def load_comparative_data(self, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        # --- CORREÇÃO APLICADA AQUI ---
        # A chamada agora é para 'self._load_table_by_name', sem o '_repo'.
        df_full = self._load_table_by_name(name)
        
        if df_full.empty:
            return pd.DataFrame(), pd.DataFrame()

        date_col_map = {
            "financas": "Data", "estoque": "Data_Snapshot",
            "recursos_humanos": "Data_Contratacao"
        }
        date_col = date_col_map.get(name.lower())

        if not date_col or date_col not in df_full.columns:
            return df_full, pd.DataFrame()

        df_current = pd.DataFrame()
        df_previous = pd.DataFrame()

        if self.start_date and self.end_date:
            df_current = df_full[df_full[date_col].between(self.start_date, self.end_date)]
            period_duration = self.end_date - self.start_date
            prev_end_date = self.start_date - pd.Timedelta(days=1)
            prev_start_date = prev_end_date - period_duration
            df_previous = df_full[df_full[date_col].between(prev_start_date, prev_end_date)]
        else:
            df_current = df_full

        return df_current, df_previous

    def load_full_unfiltered_table(self, name: str) -> pd.DataFrame:
        """
        Carrega uma tabela completa diretamente do repositório, ignorando qualquer filtro de data.
        Essencial para obter listas completas de entidades como 'produtos'.
        """
        # Chama diretamente a função de carregamento do repositório, que tem cache e não aplica filtros.
        return self._load_table_by_name(name)

    def _load_table_by_name(self, name: str) -> pd.DataFrame:
        key = str(name).strip().lower()
        if key == "financas": return self._repo.load_financas()
        if key == "estoque": return self._repo.load_estoque_snapshot()
        if key == "publico_alvo": return self._repo.load_publico_alvo()
        if key == "recursos_humanos": return self._repo.load_rh()
        if key == "fornecedores": return self._repo.load_fornecedores()
        return pd.DataFrame()