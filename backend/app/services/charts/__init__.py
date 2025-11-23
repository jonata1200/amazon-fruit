# backend/app/services/charts/__init__.py
"""
Módulo de geração de gráficos Plotly para os dashboards.
Organizado em submódulos por categoria de dashboard.
"""

# Gráficos do Dashboard Geral
from .general_charts import create_general_evolution_chart_data

# Gráficos do Dashboard de Finanças
from .finance_charts import (
    create_finance_evolution_chart_data,
    create_top_expenses_chart_data,
    create_top_revenues_chart_data
)

# Gráficos do Dashboard de Estoque
from .inventory_charts import (
    create_top_selling_chart_data,
    create_least_selling_chart_data,
    create_stock_rupture_chart_data
)

# Gráficos do Dashboard de Fornecedores
from .suppliers_charts import (
    create_supplier_ranking_chart_data,
    create_supplier_geo_chart_data
)

# Gráficos do Dashboard de Público-Alvo
from .public_charts import (
    create_public_location_chart_data,
    create_public_gender_chart_data,
    create_public_channel_chart_data
)

# Gráficos do Dashboard de Recursos Humanos
from .hr_charts import (
    create_hr_headcount_chart_data,
    create_hr_cost_chart_data,
    create_hr_role_chart_data,
    create_hr_hiring_chart_data
)

# Exportar todas as funções para compatibilidade com imports antigos
__all__ = [
    # Geral
    'create_general_evolution_chart_data',
    # Finanças
    'create_finance_evolution_chart_data',
    'create_top_expenses_chart_data',
    'create_top_revenues_chart_data',
    # Estoque
    'create_top_selling_chart_data',
    'create_least_selling_chart_data',
    'create_stock_rupture_chart_data',
    # Fornecedores
    'create_supplier_ranking_chart_data',
    'create_supplier_geo_chart_data',
    # Público-Alvo
    'create_public_location_chart_data',
    'create_public_gender_chart_data',
    'create_public_channel_chart_data',
    # RH
    'create_hr_headcount_chart_data',
    'create_hr_cost_chart_data',
    'create_hr_role_chart_data',
    'create_hr_hiring_chart_data',
]

