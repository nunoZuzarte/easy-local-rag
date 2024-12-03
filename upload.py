import os
import PyPDF2
import re
import json
import argparse

def process_file(file_path):
    # Lógica para processar diferentes tipos de arquivo
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.pdf':
            with open(file_path, 'rb') as input_file:
                pdf_reader = PyPDF2.PdfReader(input_file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() + " "
        
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as input_file:
                text = input_file.read()
        
        elif file_extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as input_file:
                data = json.load(input_file)
                text = json.dumps(data, ensure_ascii=False)
        
        else:
            print(f"Tipo de arquivo não suportado: {file_extension}")
            return

        # Normalizar e dividir texto em chunks
        text = re.sub(r'\s+', ' ', text).strip()
        sentences = re.split(r'(?<=[.!?]) +', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 < 1000:
                current_chunk += (sentence + " ").strip()
            else:
                chunks.append(current_chunk)
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk)

        # Adicionar chunks ao vault.txt
        with open("vault.txt", "a", encoding="utf-8") as vault_file:
            for chunk in chunks:
                vault_file.write(chunk.strip() + "\n")
        
        print(f"Conteúdo de {file_path} adicionado ao vault.txt")

    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Upload files to vault")
    parser.add_argument('files', nargs='+', help='Arquivos para upload (PDF, TXT, JSON)')
    
    args = parser.parse_args()
    
    for file_path in args.files:
        process_file(file_path)

if __name__ == "__main__":
    main()