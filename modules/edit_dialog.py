# modules/edit_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDialogButtonBox, QSpinBox, QDoubleSpinBox, QDateEdit)
from PyQt6.QtCore import QDate

class ProductDialog(QDialog):
    """
    Uma janela de diálogo para adicionar ou editar um produto.
    """
    def __init__(self, product_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar/Editar Produto")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Criar os campos do formulário
        self.id_produto = QLineEdit()
        self.nome_produto = QLineEdit()
        self.categoria = QLineEdit()
        self.id_fornecedor = QLineEdit()
        self.quantidade_estoque = QSpinBox()
        self.quantidade_estoque.setRange(0, 9999)
        self.preco_custo = QDoubleSpinBox()
        self.preco_custo.setRange(0, 9999.99)
        self.preco_venda = QDoubleSpinBox()
        self.preco_venda.setRange(0, 9999.99)
        self.data_validade = QDateEdit()
        self.data_validade.setCalendarPopup(True)
        self.data_validade.setDate(QDate.currentDate())
        self.nivel_minimo = QSpinBox()
        self.nivel_minimo.setRange(0, 9999)
        
        # Adicionar campos ao layout do formulário
        form_layout.addRow("ID Produto:", self.id_produto)
        form_layout.addRow("Nome:", self.nome_produto)
        form_layout.addRow("Categoria:", self.categoria)
        form_layout.addRow("ID Fornecedor:", self.id_fornecedor)
        form_layout.addRow("Quantidade:", self.quantidade_estoque)
        form_layout.addRow("Preço de Custo:", self.preco_custo)
        form_layout.addRow("Preço de Venda:", self.preco_venda)
        form_layout.addRow("Data de Validade:", self.data_validade)
        form_layout.addRow("Nível Mínimo:", self.nivel_minimo)
        
        layout.addLayout(form_layout)

        # Botões OK e Cancelar
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        # Se for para editar, preencher os campos com os dados existentes
        if product_data:
            self.id_produto.setText(str(product_data.get('ID_Produto', '')))
            self.id_produto.setReadOnly(True) # O ID não pode ser editado
            self.nome_produto.setText(str(product_data.get('Nome_Produto', '')))
            self.categoria.setText(str(product_data.get('Categoria', '')))
            self.id_fornecedor.setText(str(product_data.get('ID_Fornecedor', '')))
            self.quantidade_estoque.setValue(int(product_data.get('Quantidade_Estoque', 0)))
            self.preco_custo.setValue(float(product_data.get('Preco_Custo', 0.0)))
            self.preco_venda.setValue(float(product_data.get('Preco_Venda', 0.0)))
            self.data_validade.setDate(QDate.fromString(str(product_data.get('Data_Validade', '')).split(' ')[0], 'yyyy-MM-dd'))
            self.nivel_minimo.setValue(int(product_data.get('Nivel_Minimo_Estoque', 0)))

    def get_data(self):
        """Retorna os dados inseridos no formulário como um dicionário."""
        return {
            'ID_Produto': self.id_produto.text(),
            'Nome_Produto': self.nome_produto.text(),
            'Categoria': self.categoria.text(),
            'ID_Fornecedor': self.id_fornecedor.text(),
            'Quantidade_Estoque': self.quantidade_estoque.value(),
            'Preco_Custo': self.preco_custo.value(),
            'Preco_Venda': self.preco_venda.value(),
            'Data_Validade': self.data_validade.date().toString('yyyy-MM-dd'),
            'Nivel_Minimo_Estoque': self.nivel_minimo.value(),
        }