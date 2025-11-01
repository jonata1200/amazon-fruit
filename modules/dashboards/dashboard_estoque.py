# modules/dashboards/dashboard_estoque.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from ..edit_dialog import ProductDialog

import pandas as pd
from modules.ui.qt_utils import set_table_from_df

# --- 1. CLASSE INTELIGENTE PARA ORDENAÇÃO ---
class CustomTableWidgetItem(QTableWidgetItem):
    """
    Subclasse de QTableWidgetItem que permite a ordenação correta de números.
    """
    def __lt__(self, other):
        # Tenta comparar os itens como se fossem números (float)
        try:
            return float(self.text()) < float(other.text())
        except (ValueError, TypeError):
            # Se a conversão para float falhar, compara como texto
            return super().__lt__(other)

class DashboardEstoque(QWidget):
    def __init__(self, data_handler, theme_name='dark'):
        super().__init__()
        self.data_handler = data_handler
        self.theme_name = theme_name
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_content_widget = None
        self.build_ui()

    def build_ui(self):
        if self.central_content_widget:
            self.central_content_widget.deleteLater()
        self.central_content_widget = QWidget()
        content_layout = QVBoxLayout(self.central_content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        self.df_estoque = self.data_handler.get_dataframe('Estoque')
        title_label = QLabel("Dashboard de Estoque")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: '#FF8C00';")
        content_layout.addWidget(title_label)
        kpi_layout = QHBoxLayout()
        
        total_produtos = len(self.df_estoque)
        valor_total_custo = (self.df_estoque['Preco_Custo'] * self.df_estoque['Quantidade_Estoque']).sum()
        itens_estoque_baixo = (self.df_estoque[self.df_estoque['Quantidade_Estoque'] <= self.df_estoque['Nivel_Minimo_Estoque']]).shape[0]
        kpi_layout.addWidget(self._create_kpi_box("Produtos Únicos", f"{total_produtos}"))
        kpi_layout.addWidget(self._create_kpi_box("Valor do Estoque (Custo)", f"R$ {valor_total_custo:,.2f}"))
        kpi_layout.addWidget(self._create_kpi_box("Itens com Estoque Baixo", f"{itens_estoque_baixo}"))
        content_layout.addLayout(kpi_layout)
        action_buttons_layout = QHBoxLayout()

        add_button = QPushButton("➕ Adicionar Produto")
        add_button.setObjectName("ActionButton")
        add_button.clicked.connect(self.add_product)
        edit_button = QPushButton("✏️ Editar Produto")
        edit_button.setObjectName("ActionButton")
        edit_button.clicked.connect(self.edit_product)
        delete_button = QPushButton("🗑️ Excluir Produto")
        delete_button.setObjectName("ActionButton")
        delete_button.clicked.connect(self.delete_product)

        action_buttons_layout.addWidget(add_button)
        action_buttons_layout.addWidget(edit_button)
        action_buttons_layout.addWidget(delete_button)
        action_buttons_layout.addStretch()
        content_layout.addLayout(action_buttons_layout)
        bottom_layout = QHBoxLayout()
        table_section_layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar produto...")
        self.search_bar.textChanged.connect(self.filter_table)
        table_section_layout.addWidget(self.search_bar)
        self.stock_table = self._create_stock_table()
        table_section_layout.addWidget(self.stock_table)
        bottom_layout.addLayout(table_section_layout)

        charts_layout = QVBoxLayout()
        charts_layout.addWidget(self._create_low_stock_chart())
        charts_layout.addWidget(self._create_category_pie_chart())
        bottom_layout.addLayout(charts_layout)
        content_layout.addLayout(bottom_layout)
        self.main_layout.addWidget(self.central_content_widget)

    def _create_stock_table(self):
        table = QTableWidget()
        # --- 2. HABILITAR A ORDENAÇÃO ---
        table.setSortingEnabled(True)

        table.setColumnCount(len(self.df_estoque.columns))
        table.setRowCount(len(self.df_estoque))
        table.setHorizontalHeaderLabels(self.df_estoque.columns)
        for i, row in self.df_estoque.iterrows():
            for j, value in enumerate(row):
                # --- 3. USAR A NOVA CLASSE INTELIGENTE ---
                item = CustomTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def update_theme(self, new_theme_name):
        self.theme_name = new_theme_name
        self.build_ui()

    def add_product(self):
        """Abre o diálogo para adicionar um novo produto, com validação de dados."""
        dialog = ProductDialog()
        if dialog.exec():
            new_data = dialog.get_data()

            # --- LÓGICA DE VALIDAÇÃO ---
            # 1. Validação de campos obrigatórios
            if not new_data['ID_Produto'] or not new_data['Nome_Produto']:
                QMessageBox.warning(self, "Entrada Inválida", "ID do Produto e Nome são campos obrigatórios.")
                return

            # 2. Validação de ID duplicado
            if self.data_handler.record_exists('Estoque', 'ID_Produto', new_data['ID_Produto']):
                QMessageBox.warning(self, "Entrada Inválida", f"O ID de produto '{new_data['ID_Produto']}' já existe. Por favor, use um ID único.")
                return

            # 3. Validação de Preço de Venda vs. Custo
            if new_data['Preco_Venda'] < new_data['Preco_Custo']:
                QMessageBox.warning(self, "Entrada Inválida", "O preço de venda não pode ser menor que o preço de custo.")
                return
            
            # Se todas as validações passarem, adiciona o registro
            if self.data_handler.add_record('Estoque', new_data):
                QMessageBox.information(self, "Sucesso", "Produto adicionado com sucesso!")
                self.build_ui()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível adicionar o produto ao banco de dados.")

    def edit_product(self):
        """Abre o diálogo para editar o produto selecionado, com validação de dados."""
        selected_row_index = self.stock_table.currentRow()
        if selected_row_index < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para editar.")
            return
            
        product_id = self.stock_table.item(selected_row_index, 0).text()
        product_data = self.df_estoque.iloc[selected_row_index].to_dict()
        
        dialog = ProductDialog(product_data=product_data)
        if dialog.exec():
            updated_data = dialog.get_data()
            
            # --- LÓGICA DE VALIDAÇÃO ---
            # 1. Validação de Preço de Venda vs. Custo
            if updated_data['Preco_Venda'] < updated_data['Preco_Custo']:
                QMessageBox.warning(self, "Entrada Inválida", "O preço de venda não pode ser menor que o preço de custo.")
                return
            
            del updated_data['ID_Produto'] # O ID não é editável, então removemos para a query UPDATE
            
            # Se a validação passar, atualiza o registro
            if self.data_handler.update_record('Estoque', updated_data, 'ID_Produto', product_id):
                QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso!")
                self.build_ui()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível atualizar o produto no banco de dados.")

    # --- NOVO MÉTODO PARA EXCLUSÃO ---
    def delete_product(self):
        """Exclui o produto selecionado na tabela após confirmação."""
        selected_row_index = self.stock_table.currentRow()
        if selected_row_index < 0:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um produto na tabela para excluir.")
            return

        # Obter o ID e o Nome do produto para a mensagem de confirmação
        product_id = self.stock_table.item(selected_row_index, 0).text()
        product_name = self.stock_table.item(selected_row_index, 1).text()

        # Caixa de diálogo de confirmação
        reply = QMessageBox.question(
            self,
            'Confirmar Exclusão',
            f"Você tem certeza que deseja excluir o produto:\n\n{product_name} (ID: {product_id})?\n\nEsta ação não pode ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.data_handler.delete_record('Estoque', 'ID_Produto', product_id):
                QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso!")
                self.build_ui() # Atualiza a interface
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível excluir o produto do banco de dados.")


    def filter_table(self):
        search_text = self.search_bar.text().lower()
        for row_num in range(self.stock_table.rowCount()):
            row_text = ''.join([self.stock_table.item(row_num, c).text().lower() for c in range(self.stock_table.columnCount())])
            self.stock_table.setRowHidden(row_num, search_text not in row_text)

    def _create_kpi_box(self, title, value, value_color=None):
        kpi_frame = QFrame()
        kpi_frame.setObjectName("KPIFrame")
        layout = QVBoxLayout(kpi_frame)
        title_label = QLabel(title)
        title_label.setObjectName("KPITitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label = QLabel(value)
        value_label.setObjectName("KPIValueLabel")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if value_color:
            value_label.setStyleSheet(f"color: {value_color};")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return kpi_frame

    def _create_stock_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.df_estoque.columns))
        table.setRowCount(len(self.df_estoque))
        table.setHorizontalHeaderLabels(self.df_estoque.columns)
        for i, row in self.df_estoque.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def _create_low_stock_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        low_stock_df = self.df_estoque[self.df_estoque['Quantidade_Estoque'] <= self.df_estoque['Nivel_Minimo_Estoque']].copy().sort_values('Quantidade_Estoque', ascending=True).head(5)
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.barh(low_stock_df['Nome_Produto'], low_stock_df['Quantidade_Estoque'], color='#FF8C00')
        ax.set_title('Top 5 Produtos com Estoque Baixo', color=text_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(bg_color)
        fig.tight_layout()
        return FigureCanvas(fig)

    def _create_category_pie_chart(self):
        text_color = 'white' if self.theme_name == 'dark' else 'black'
        bg_color = '#2E2E2E' if self.theme_name == 'dark' else '#F0F0F0'
        category_counts = self.df_estoque['Categoria'].value_counts()
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.pie(
            category_counts,
            labels=category_counts.index,
            autopct='%1.1f%%',
            textprops={'color': text_color}
        )
        ax.set_title('Distribuição por Categoria', color=text_color)
        fig.tight_layout()
        return FigureCanvas(fig)

    # dentro da sua classe DashboardEstoque:
    def _reload_data(self):
        self.df_estoque = self.data_handler.load_table("Estoque")

    def _rebuild_kpis(self):
        df = self.df_estoque
        total = df['ID_Produto'].nunique() if 'ID_Produto' in df else len(df)
        valor = 0.0
        if {'Quantidade_Estoque','Preco_Custo'}.issubset(df.columns):
            q = pd.to_numeric(df['Quantidade_Estoque'], errors='coerce').fillna(0)
            c = pd.to_numeric(df['Preco_Custo'], errors='coerce').fillna(0.0)
            valor = float((q*c).sum())
        baixo = 0
        if {'Quantidade_Estoque','Nivel_Minimo_Estoque'}.issubset(df.columns):
            baixo = int((pd.to_numeric(df['Quantidade_Estoque'], errors='coerce') <=
                        pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce')).sum())

        # supondo que você tenha labels: self.kpi_produtos, self.kpi_valor, self.kpi_baixo
        self.kpi_produtos.setText(str(total))
        self.kpi_valor.setText(f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.kpi_baixo.setText(str(baixo))

    def _rebuild_tables(self):
        # supondo que table é self.table_estoque (QTableView)
        set_table_from_df(self.table_estoque, self.df_estoque)

    def _rebuild_charts(self):
        # 1) pizza por categoria -> self.canvas_categoria (FigureCanvas)
        if hasattr(self, "canvas_categoria"):
            self.layout_categoria.removeWidget(self.canvas_categoria)
            self.canvas_categoria.setParent(None)
        fig1 = Figure(figsize=(5, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        if not self.df_estoque.empty and 'Categoria' in self.df_estoque:
            s = self.df_estoque['Categoria'].astype(str).value_counts()
            if not s.empty:
                ax1.pie(s.values, labels=s.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Distribuição por Categoria")
        self.canvas_categoria = FigureCanvas(fig1)
        self.layout_categoria.addWidget(self.canvas_categoria)

        # 2) barra horizontal itens abaixo do mínimo -> self.canvas_baixo
        if hasattr(self, "canvas_baixo"):
            self.layout_baixo.removeWidget(self.canvas_baixo)
            self.canvas_baixo.setParent(None)
        fig2 = Figure(figsize=(5.6, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        req = {'Nome_Produto','Quantidade_Estoque','Nivel_Minimo_Estoque'}
        if req.issubset(self.df_estoque.columns):
            df = self.df_estoque.copy()
            df['gap'] = pd.to_numeric(df['Nivel_Minimo_Estoque'], errors='coerce') - \
                        pd.to_numeric(df['Quantidade_Estoque'], errors='coerce')
            low = df[df['gap'] > 0].sort_values('gap', ascending=False).head(10)
            if not low.empty:
                ax2.barh(low['Nome_Produto'].astype(str), low['gap'])
                ax2.invert_yaxis()
        ax2.set_title("Itens com Estoque Baixo (gap)")
        self.canvas_baixo = FigureCanvas(fig2)
        self.layout_baixo.addWidget(self.canvas_baixo)

    def refresh(self):
        self._reload_data()
        self._rebuild_kpis()
        self._rebuild_tables()
        self._rebuild_charts()