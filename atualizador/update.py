import requests
import json
import subprocess

def verificar_atualizacao():
    try:
        with open("pdv/versao_local.txt", "r") as f:
            versao_atual = f.read().strip()
    except FileNotFoundError:
        versao_atual = "0.0.0"

    url_servidor = "https://github.com/LuanAllves/Gerador-de-Recibo/blob/main/atualizador/version.json"

    try:
        resposta = requests.get(url_servidor)
        resposta.raise_for_status()
        dados_versao = resposta.json()
        versao_nova = dados_versao["versao"]

        if versao_nova > versao_atual:
            print("Atualização disponível!")
            link_download = dados_versao["link_download"]
            arquivo_instalador = "atualizacao.exe"  # Ou outro formato
            baixar_arquivo(link_download, arquivo_instalador)
            instalar_atualizacao(arquivo_instalador)
            atualizar_versao_local(versao_nova)
        else:
            print("Sistema atualizado.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao verificar atualização: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao processar dados da versão: {e}")

def baixar_arquivo(url, arquivo):
    resposta = requests.get(url, stream=True)
    resposta.raise_for_status()
    with open(arquivo, "wb") as f:
        for chunk in resposta.iter_content(chunk_size=8192):
            f.write(chunk)

def instalar_atualizacao(arquivo):
    subprocess.run([arquivo])

def atualizar_versao_local(versao):
    with open("pdv/versao_local.txt", "w") as f:
        f.write(versao)

if __name__ == "__main__":
    verificar_atualizacao()