# utils/data_handler.py
from __future__ import annotations
import re
from pathlib import Path
from functools import lru_cache
import pandas as pd
from calendar import monthrange

# Raiz padrão para ./data (projeto/ data)
BASE_DIR = Path(__file__).resolve().parents[2] / "data"

MESES = {"Jan":1,"Fev":2,"Mar":3,"Abr":4,"Mai":5,"Jun":6,"Jul":7,"Ago":8,"Set":9,"Out":10,"Nov":11,"Dez":12}
SHEET_RGX = re.compile(r"^(\d{2})-([A-Za-z]{3})$")  # ex.: 01-Jan, 12-Dez


def _sheet_to_period(sheet_name: str) -> tuple[int, int]:
    m = SHEET_RGX.match(str(sheet_name).strip())
    if not m:
        raise ValueError(f"Aba fora do padrão 'MM-Mmm': {sheet_name}")
    mm, mmm = int(m.group(1)), m.group(2).title()
    mes = MESES.get(mmm, mm)
    return mes, mes


def _last_day(ano: int, mes: int) -> str:
    return f"{ano:04d}-{mes:02d}-{monthrange(ano, mes)[1]:02d}"


class DataRepository:
    def __init__(self, base_dir: Path | str | None = None):
        p = Path(base_dir) if base_dir is not None else BASE_DIR
        # se passar um arquivo (ex.: amazon_fruit.db), usa a pasta dele
        if p.suffix.lower() == ".db" or p.is_file():
            p = p.parent
        # fallback: se não existir 'recursos_humanos/recursos_humanos.xlsx' nessa base,
        # tenta a pasta padrão <raiz>/data
        rh_rel = Path("recursos_humanos") / "recursos_humanos.xlsx"
        if not (p / rh_rel).exists():
            default_base = BASE_DIR  # <raiz>/data
            if (default_base / rh_rel).exists():
                p = default_base
        self.base_dir: Path = p

    # ---- utils dependentes de self.base_dir ----
    def _iter_year_files(self, subdir: str, filename: str):
        """Gera caminhos <base_dir>/<subdir>/<ano>/<filename> existentes."""
        raiz = self.base_dir / subdir
        if not raiz.exists():
            return
        for ano_dir in sorted(raiz.iterdir()):
            if not ano_dir.is_dir():
                continue
            fp = ano_dir / filename
            if fp.exists():
                try:
                    ano_int = int(ano_dir.name)
                except ValueError:
                    continue
                yield ano_int, fp

    # ---------- FOTO (1 aba, estado atual) ----------
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

    # ---------- FILME (12 abas por ano) ----------
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
        return df

    @lru_cache(maxsize=1)
    def load_estoque_snapshot(self) -> pd.DataFrame:
        """Concatena todos os meses como snapshots; adiciona Data_Snapshot = último dia do mês da aba."""
        frames = []
        for ano, fp in self._iter_year_files("estoque", "estoque.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names:
                mes, _ = _sheet_to_period(sheet)
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Ano"] = ano
                df["Mes"] = mes
                df["Data_Validade"] = pd.to_datetime(df.get("Data_Validade"), errors="coerce")
                df["Data_Snapshot"] = pd.to_datetime(_last_day(ano, mes))
                frames.append(df)
        if not frames:
            return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
        df["ID_Produto"] = pd.to_numeric(df.get("ID_Produto"), errors="coerce").astype("Int64")
        for c in ["Quantidade_Estoque", "Preco_Custo", "Preco_Venda", "Nivel_Minimo_Estoque"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        return df

    @lru_cache(maxsize=1)
    def load_publico_alvo(self) -> pd.DataFrame:
        """Une as abas mensais por ano; mantém Ano/Mes para filtros."""
        frames = []
        for ano, fp in self._iter_year_files("publico_alvo", "publico_alvo.xlsx"):
            xls = pd.ExcelFile(fp, engine="openpyxl")
            for sheet in xls.sheet_names:
                mes, _ = _sheet_to_period(sheet)
                df = pd.read_excel(xls, sheet_name=sheet)
                df["Ano"] = ano
                df["Mes"] = mes
                frames.append(df)
        if not frames:
            return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
        if "ID_Cliente" in df.columns:
            df["ID_Cliente"] = pd.to_numeric(df["ID_Cliente"], errors="coerce").astype("Int64")
        if "Idade" in df.columns:
            df["Idade"] = pd.to_numeric(df["Idade"], errors="coerce")
        return df

    # ---------- Helpers ----------
    def healthcheck(self) -> dict:
        return {
            "fornecedores": len(self.load_fornecedores()),
            "rh": len(self.load_rh()),
            "financas": len(self.load_financas()),
            "estoque_snapshot": len(self.load_estoque_snapshot()),
            "publico_alvo": len(self.load_publico_alvo()),
        }


# --- Compat: fachada DataHandler para código legado -------------------------
__all__ = ["DataRepository", "DataHandler"]

class DataHandler:
    """Fachada compatível com o código antigo."""
    def __init__(self, base_dir: Path | str | None = None):
        self._repo = DataRepository(base_dir)

    def load_table(self, name: str):
        key = str(name).strip().lower()
        if key in ("financas", "financeiro", "finance"):     return self._repo.load_financas()
        if key in ("estoque", "inventory"):                   return self._repo.load_estoque_snapshot()
        if key in ("publico_alvo", "publico", "public"):      return self._repo.load_publico_alvo()
        if key in ("recursos_humanos", "rh", "recursos-humanos"): return self._repo.load_rh()
        if key in ("fornecedores", "supplier", "suppliers"):  return self._repo.load_fornecedores()
        raise ValueError(f"Tabela desconhecida: {name}")

    def healthcheck(self):
        return self._repo.healthcheck()