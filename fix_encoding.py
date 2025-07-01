# -*- coding: utf-8 -*-
import os
import codecs

def fix_file_encoding(file_path):
    """Corrige encoding de um arquivo para UTF-8"""
    try:
        # Tentar ler com diferentes encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        
        for encoding in encodings:
            try:
                with codecs.open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"✅ Arquivo {file_path} lido com encoding {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"❌ Não foi possível ler {file_path}")
            return False
        
        # Adicionar BOM UTF-8 se não existir
        if not content.startswith('# -*- coding: utf-8 -*-'):
            content = '# -*- coding: utf-8 -*-\n' + content
        
        # Salvar como UTF-8
        with codecs.open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Arquivo {file_path} convertido para UTF-8")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def fix_project_encoding():
    """Corrige encoding de todos os arquivos Python do projeto"""
    python_files = []
    
    # Encontrar todos os arquivos .py
    for root, dirs, files in os.walk('.'):
        # Pular diretórios desnecessários
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'env']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"🔍 Encontrados {len(python_files)} arquivos Python")
    
    success_count = 0
    for file_path in python_files:
        if fix_file_encoding(file_path):
            success_count += 1
    
    print(f"\n✅ {success_count}/{len(python_files)} arquivos corrigidos com sucesso!")

if __name__ == "__main__":
    fix_project_encoding()
