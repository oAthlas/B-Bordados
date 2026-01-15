# services/storage.py
import uuid
from django.conf import settings
from .supabase import supabase  # Importa a instância configurada

def upload_product_zip(file_obj, product_id):
    """
    Envia ZIP para o Supabase Storage
    Retorna o path salvo
    """
    try:
        filename = f"{product_id}/{uuid.uuid4()}_{file_obj.name}"
        
        # Lê o conteúdo do arquivo
        file_content = file_obj.read()
        
        # Verifica se o arquivo não está vazio
        if len(file_content) == 0:
            raise ValueError("Arquivo vazio")
        
        supabase.storage \
            .from_(settings.SUPABASE_BUCKET) \
            .upload(
                path=filename,
                file=file_content,
                file_options={
                    "content-type": "application/zip",
                    "upsert": True,
                }
            )
        
        return filename
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")
        raise