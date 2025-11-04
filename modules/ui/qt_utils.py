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
        items = [QStandardItem("" if v is None else str(v)) for v in row.values]
        model.appendRow(items)
    return model

def set_table_from_df(table: QTableView, df: pd.DataFrame):
    model = df_to_model(df)
    
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    table.setModel(model)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setStretchLastSection(True)

def set_table_with_conditional_formatting(table: QTableView, df: pd.DataFrame):
    model = df_to_model(df) # Reutiliza a função que já existe para criar o modelo
    
    # Se o DataFrame ou o modelo estiverem vazios, não faz nada
    if df is None or df.empty or model.rowCount() == 0:
        table.setModel(model)
        return

    # Itera sobre as linhas do DataFrame para decidir a cor
    for i, row_data in df.iterrows():
        try:
            # Pega os valores das colunas corretas para a lógica de cores
            # Usamos .get() para não dar erro se a coluna não existir
            qtd_str = str(row_data.get('Quantidade em Estoque', '0')).replace('R$', '').replace('.', '').replace(',', '.').strip()
            min_str = str(row_data.get('Nível Mínimo de Estoque', '0')).replace('R$', '').replace('.', '').replace(',', '.').strip()

            qtd = float(qtd_str)
            minimo = float(min_str)
            
            color = None
            if qtd <= minimo:
                color = QColor("#C21807") # Vermelho para alerta
            elif qtd <= minimo * 1.2: # Amarelo para atenção (até 20% acima do mínimo)
                color = QColor("#FFBF00")

            # Se uma cor foi definida, aplica a todos os itens daquela linha
            if color:
                for j in range(model.columnCount()):
                    model.item(i, j).setBackground(color)
        except (ValueError, TypeError, AttributeError):
            # Se houver qualquer erro na conversão dos números, apenas ignora a formatação daquela linha
            continue

    table.setModel(model)
    header = table.horizontalHeader()
    # Ajusta o tamanho das colunas ao conteúdo
    header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    table.setAlternatingRowColors(True)