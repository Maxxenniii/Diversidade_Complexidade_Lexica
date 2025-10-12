import os
import re
import json

def diversidade_lexica(texto):
    palavras = re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', texto.lower())
    if not palavras:
        return 0
    return len(set(palavras)) / len(palavras)

def buscar_pasta(pasta):
    resultados = {}
    total_palavras = 0
    set_unicas_geral = set()

    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".json"):
            caminho = os.path.join(pasta, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as arqui:
                    dados = json.load(arqui)
                
                if "redacao" in dados and isinstance(dados["redacao"], dict):
                    texto = " ".join(dados["redacao"].values())
                else:
                    texto = ""
                    print(f"Aviso: Campo 'redacao' não encontrado ou inválido em {arquivo}")
                    continue
                
                diversidade = diversidade_lexica(texto)
                resultados[arquivo] = diversidade

          
                palavras = re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', texto.lower())
                total_palavras += len(palavras)
                set_unicas_geral.update(palavras)
                        
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")
                continue

    diversidade_geral = len(set_unicas_geral) / total_palavras if total_palavras > 0 else 0
    
    print(f"\n=== ESTATÍSTICAS GERAIS ===")
    print(f"Total de arquivos processados: {len(resultados)}")
    print(f"Total de palavras no dataset (com 3+ letras): {total_palavras}")
    print(f"Palavras únicas no dataset (com 3+ letras): {len(set_unicas_geral)}")
    print(f"Diversidade léxica geral: {diversidade_geral:.3f}")
    
    return resultados, diversidade_geral

def main():
    pasta = "C:/Users/Maxine/Downloads/IC/ChatgptTurbo"
    
    resultados, diversidade_geral = buscar_pasta(pasta)

    resultados_dir = "C:/Users/Maxine/Downloads/IC/Resultados"
    os.makedirs(resultados_dir, exist_ok=True)

    resultados_separados = os.path.join(resultados_dir, "Resultados_Separados.txt")
    resultado_dataSet = os.path.join(resultados_dir, "Resultado_dataSet.txt")

    with open(resultados_separados, "w", encoding="utf-8") as arqui:
        for nome, valor in resultados.items():
            arqui.write(f"{nome}: {valor:.3f} e com isso {valor*100:.1f}\n")

    with open(resultado_dataSet, "w", encoding="utf-8") as arqui:
        arqui.write(f"Diversidade léxica geral do dataset: {diversidade_geral:.3f}, com isso {diversidade_geral*100:.1f}%")

if __name__ == "__main__":
    main()