# Atualização do requirements.txt

## ✅ Alterações Realizadas

### Dependências Adicionadas

As seguintes dependências foram **adicionadas** ao `requirements.txt`:

#### Framework Web
- ✅ `fastapi==0.104.1` - Framework web moderno para Python
- ✅ `uvicorn[standard]==0.24.0` - Servidor ASGI para FastAPI

#### Banco de Dados
- ✅ `sqlalchemy==2.0.23` - ORM para Python
- ✅ `aiosqlite==0.19.0` - Suporte assíncrono para SQLite

#### Gráficos Web
- ✅ `plotly==5.18.0` - Biblioteca de gráficos interativos para web
- ✅ `kaleido==0.2.1` - Exportação de gráficos Plotly

#### Testes
- ✅ `pytest==7.4.3` - Framework de testes
- ✅ `pytest-asyncio==0.21.1` - Suporte a testes assíncronos

### Dependências Mantidas

Todas as dependências existentes foram **mantidas** para garantir compatibilidade com a aplicação desktop:

- PyQt6 (interface desktop)
- Matplotlib e Seaborn (gráficos desktop)
- Pandas e NumPy (análise de dados)
- ReportLab (relatórios PDF)
- E todas as outras dependências existentes

## 📋 Estrutura do Arquivo

O arquivo foi organizado em seções para facilitar a leitura:

1. **Framework Web** - FastAPI e Uvicorn
2. **Banco de Dados** - SQLAlchemy e aiosqlite
3. **Análise de Dados** - Pandas e NumPy
4. **Gráficos** - Matplotlib, Seaborn (desktop) e Plotly (web)
5. **Interface Desktop** - PyQt6
6. **Relatórios** - ReportLab
7. **Manipulação de Arquivos** - OpenPyXL e Pillow
8. **Utilitários** - Várias bibliotecas de suporte
9. **Desenvolvimento** - Pytest e plugins

## 🚀 Próximos Passos

Agora você pode:

1. **Criar o ambiente virtual:**
   ```bash
   python -m venv .venv
   ```

2. **Ativar o ambiente virtual:**
   ```bash
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar todas as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar instalação:**
   ```bash
   pip list | Select-String -Pattern "fastapi|uvicorn"
   ```

## 📊 Resumo

- **Total de dependências:** ~30 pacotes
- **Novas dependências adicionadas:** 8 pacotes
- **Dependências mantidas:** Todas as existentes
- **Compatibilidade:** Mantida com aplicação desktop e web

## ⚠️ Nota Importante

Este `requirements.txt` agora suporta **ambos** os projetos:
- ✅ Aplicação Desktop (PyQt6) - continua funcionando
- ✅ Aplicação Web (FastAPI) - pronta para desenvolvimento

Se você quiser instalar apenas as dependências do backend web, use:
```bash
pip install -r backend/requirements.txt
```

Mas para ter tudo disponível, use o `requirements.txt` da raiz.

