import os
import shutil
import subprocess

# Definindo os diretórios
system_dir = 'C:/Sistema_Recibos'
update_dir = 'C:/Gerador-de-Recibo'
backup_dir = 'C:/GDR_Backup'
dist_dir = os.path.join(update_dir, 'dist')
dist_subdir = os.path.join(dist_dir, 'Sistema_Recibo')
dest_dir = system_dir

#Limpando a pasta de atualização, ja que o sistema ja foi recompilado e enviado para a pasta do sistema.
def limpar_pasta_update():
    for file in os.listdir(update_dir):
        if os.path.isfile(os.path.join(update_dir, file)):
            if not file.endswith('.py') and not file.endswith('.txt'):
                os.remove(os.path.join(update_dir, file))
                print(f"Arquivo '{file}' excluído com sucesso.")
    
    for dir in os.listdir(update_dir):
        if os.path.isdir(os.path.join(update_dir, dir)):
            if dir in ['dist', 'build']:
                shutil.rmtree(os.path.join(update_dir, dir))
                print(f"Pasta '{dir}' excluída com sucesso.")

# Definindo as extensões de banco de dados
db_extensions = ['.db', '.sqlite', '.mdb']

# Função para ignorar a pasta .git
def ignore_git(dir, files):
    return [f for f in files if os.path.join(dir, f) != '.git']

# Atualizando o arquivo requeriments.txt
requeriments_file = os.path.join(update_dir, 'requeriments.txt')
with open(requeriments_file, 'w') as f:
    subprocess.check_call(['pip', 'freeze'], stdout=f)
print("Arquivo requeriments.txt atualizado com sucesso.")

# Excluindo os arquivos de banco de dados da pasta de update
for file in os.listdir(update_dir):
    if os.path.isfile(os.path.join(update_dir, file)):
        for extension in db_extensions:
            if file.endswith(extension):
                os.remove(os.path.join(update_dir, file))
                print(f"Arquivo de banco de dados '{file}' excluído com sucesso.")

# Criando um backup do sistema
backup_system_dir = os.path.join(backup_dir, 'Gerador_de_Recibo')
if os.path.exists(backup_system_dir):
    try:
        shutil.rmtree(backup_system_dir)
    except PermissionError:
        print("Erro ao excluir pasta de backup. Ignorando...")

if not os.path.exists(system_dir):
    os.makedirs(system_dir)
    
shutil.copytree(system_dir, backup_system_dir, dirs_exist_ok=True, ignore=ignore_git)
print("Backup do sistema feito com sucesso.")

# Recompile o executável
os.chdir(update_dir)
capabilities_json_path = r'C:\Users\joaom\AppData\Local\Programs\Python\Python313\Lib\site-packages\escpos\capabilities.json'
subprocess.check_call(['pyinstaller', '--noconsole', '--name=Sistema_Recibo', '--add-data=' + capabilities_json_path + ';escpos', 'script.py'])
print("Executável recompilado com sucesso.")

# Copie o executável para o diretório do sistema
if os.path.exists(os.path.join(system_dir, file)):
    # Substituir o executável
    shutil.copy2(os.path.join(dist_dir, file), system_dir)

else:
    print("Arquivo Sistema_Recibo.exe não encontrado.")
    # Copiar a pasta criada dentro da pasta dist
    shutil.copytree(dist_subdir, dest_dir, dirs_exist_ok=True)

limpar_pasta_update()
print("Atualização concluída com sucesso.")