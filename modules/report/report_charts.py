# modules/report/report_charts.py

import io
import matplotlib.pyplot as plt
from reportlab.platypus import Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

# Importa TODAS as funções de criação de gráficos do nosso módulo centralizado
from ..dashboards.chart_generator import (
    create_general_evolution_chart,
    create_finance_evolution_chart, create_top_expenses_chart, create_top_revenues_chart,
    create_top_selling_chart, create_least_selling_chart, create_stock_rupture_chart,
    create_public_location_chart, create_public_gender_chart, create_public_channel_chart,
    create_supplier_ranking_chart, create_supplier_geo_chart, create_supplier_heatmap,
    create_hr_headcount_chart, create_hr_cost_chart, create_hr_role_chart, create_hr_hiring_chart
)

# --- FUNÇÕES AUXILIARES (sem alterações) ---
def _save_plot_to_story(story, fig, max_w=6.2, max_h=3.2):
    """Salva uma figura Matplotlib na story do relatório e a fecha para liberar memória."""
    if fig is None: return
    buf = io.BytesIO()
    fig.savefig(buf, format='PNG', dpi=150, bbox_inches='tight')
    plt.close(fig) # Essencial para liberar memória
    
    buf.seek(0)
    reader = ImageReader(buf)
    iw, ih = reader.getSize()
    aspect = ih / float(iw)
    
    width = min(iw, max_w * inch)
    height = min(ih, max_h * inch)
    
    if (width / inch * aspect) > max_h:
        height = max_h * inch
        width = height / aspect
    else:
        width = width
        height = width * aspect

    story.append(Image(buf, width=width, height=height))
    story.append(Spacer(1, 12))

# --- REESCRITA COMPLETA DAS FUNÇÕES DE SEÇÃO ---

def add_finance_charts(story, df_fin):
    """Adiciona os gráficos de finanças ao relatório."""
    fig1 = create_finance_evolution_chart(df_fin)
    _save_plot_to_story(story, fig1)
    
    fig2 = create_top_expenses_chart(df_fin)
    _save_plot_to_story(story, fig2, max_w=5.5)

def add_inventory_charts(story, df_fin, df_est):
    """Adiciona os gráficos de estoque ao relatório."""
    fig1 = create_top_selling_chart(df_fin, df_est)
    _save_plot_to_story(story, fig1)
    
    fig2 = create_stock_rupture_chart(df_est)
    _save_plot_to_story(story, fig2)

def add_public_charts(story, df_pub):
    """Adiciona os gráficos de público-alvo ao relatório."""
    fig1 = create_public_gender_chart(df_pub)
    _save_plot_to_story(story, fig1, max_w=4.0)
    
    fig2 = create_public_location_chart(df_pub)
    _save_plot_to_story(story, fig2)

def add_suppliers_charts(story, df_sup):
    """Adiciona os gráficos de fornecedores ao relatório."""
    fig1 = create_supplier_ranking_chart(df_sup)
    _save_plot_to_story(story, fig1, max_h=4.0) # Permite mais altura
    
    fig2 = create_supplier_geo_chart(df_sup)
    _save_plot_to_story(story, fig2)

def add_hr_charts(story, df_hr):
    """Adiciona os gráficos de RH ao relatório."""
    fig1 = create_hr_headcount_chart(df_hr)
    _save_plot_to_story(story, fig1)
    
    fig2 = create_hr_cost_chart(df_hr)
    _save_plot_to_story(story, fig2)