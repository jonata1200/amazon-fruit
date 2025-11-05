# modules/ui/qt_utils.py

from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt6.QtWidgets import QTableView, QHeaderView
import pandas as pd

def df_to_model(df: pd.DataFrame) -> QStandardItemModel:
    model = QStandardItemModel()
    if df is None or df.empty:
        return model
    model.setColumnCount(len(df.columns))
    model.setHorizontalHeaderLabels([str(c) for c in df.columns])
    for _, row in df.iterrows():
        items = [QStandardItem("" if pd.isna(v) else str(v)) for v in row.values]
        model.appendRow(items)
    return model

def set_table_from_df(table: QTableView, df: pd.DataFrame):
    model = df_to_model(df)
    
    header = table.horizontalHeader()
    # MODO CORRIGIDO: Distribui o espaço entre todas as colunas
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    table.setModel(model)
    table.setAlternatingRowColors(True)
    # A linha 'setStretchLastSection' foi removida

def set_table_with_conditional_formatting(table: QTableView, df: pd.DataFrame):
    model = df_to_model(df)
    
    if df is None or df.empty or model.rowCount() == 0:
        table.setModel(model)
        return

    for i, row_data in df.iterrows():
        try:
            qtd_str = str(row_data.get('Quantidade em Estoque', '0')).replace('R$', '').replace('.', '').replace(',', '.').strip()
            min_str = str(row_data.get('Nível Mínimo de Estoque', '0')).replace('R$', '').replace('.', '').replace(',', '.').strip()
            qtd = float(qtd_str)
            minimo = float(min_str)
            
            color = None
            if qtd <= minimo:
                color = QColor("#C21807")
            elif qtd <= minimo * 1.2:
                color = QColor("#FFBF00")

            if color:
                for j in range(model.columnCount()):
                    model.item(i, j).setBackground(color)
        except (ValueError, TypeError, AttributeError):
            continue

    table.setModel(model)
    header = table.horizontalHeader()
    # MODO CORRIGIDO: Distribui o espaço entre todas as colunas
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.setAlternatingRowColors(True)
    # A linha 'setStretchLastSection' foi removida