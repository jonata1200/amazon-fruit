#!/usr/bin/env python3
"""
Script auxiliar para aplicar validações em endpoints que ainda não têm.
Este script identifica endpoints que precisam de validação.
"""

import re
from pathlib import Path

def find_endpoints_needing_validation():
    """Encontra endpoints que recebem start_date/end_date mas não têm validação"""
    
    routes_dir = Path("backend/app/api/routes")
    endpoints_needing_validation = []
    
    for route_file in routes_dir.glob("*.py"):
        if route_file.name == "__init__.py":
            continue
            
        content = route_file.read_text(encoding="utf-8")
        
        # Procurar por funções async que recebem start_date e end_date
        pattern = r'async def (\w+)\([^)]*start_date[^)]*end_date[^)]*\):'
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in matches:
            func_name = match.group(1)
            func_start = match.start()
            
            # Verificar se já tem validate_date_range após a definição da função
            func_end = content.find(":", func_start)
            next_lines = content[func_end:func_end+200]
            
            if "validate_date_range" not in next_lines:
                endpoints_needing_validation.append({
                    "file": route_file.name,
                    "function": func_name
                })
    
    return endpoints_needing_validation

if __name__ == "__main__":
    endpoints = find_endpoints_needing_validation()
    
    if endpoints:
        print("⚠️  Endpoints que ainda precisam de validação:")
        for ep in endpoints:
            print(f"  - {ep['file']}::{ep['function']}")
    else:
        print("✅ Todos os endpoints têm validação!")

