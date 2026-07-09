# Arquivo: auditoria.py

def auditar_notas(lote, limite):
    print(f"\n--- INICIANDO AUDITORIA (Limite de aprovação: R$ {limite}) ---")
    
    for nota in lote:
        if nota["valor"] > limite:
            print(f"⚠️ {nota['item']} (R$ {nota['valor']}) -> Revisão Necessária")
            nota["status"] = "Em Revisão"
        else:
            print(f"✅ {nota['item']} (R$ {nota['valor']}) -> Faturado")
            nota["status"] = "Faturado"
            
    return lote