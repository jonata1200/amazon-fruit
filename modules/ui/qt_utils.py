# modules/ui/qt_utils.py
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTableView, QHeaderView
import pandas as pd

def df_to_model(df: pd.DataFrame) -> QStandardItemModel:
    model = QStandardItemModel()
    if df is None or df.empty:
        return model
    model.setColumnCount(len(df.columns))
    model.setHorizontalHeaderLabels([str(c) for c in df.columns])
    for _, row in df.iterrows():
        items = [QStandardItem("" if v is None else str(v)) for v in row.values]
        model.appendRow(items)
    return model

def set_table_from_df(table: QTableView, df: pd.DataFrame):
    model = df_to_model(df)
    
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    table.setModel(model)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setStretchLastSection(False)