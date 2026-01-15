# services/storage.py
import uuid
from django.conf import settings
from .supabase import supabase

def upload_product_zip(file_obj, product_id):
    """
    Envia ZIP para o Supabase Storage
    Retorna o path salvo
    """
    try:
        # Garante que temos um ID válido
        if not product_id:
            raise ValueError("Product ID é necessário")
        
        # Gera nome único
        safe_filename = file_obj.name.replace(' ', '_')
        filename = f"{product_id}/{uuid.uuid4()}_{safe_filename}"
        
        # Lê o conteúdo do arquivo
        file_content = file_obj.read()
        
        if len(file_content) == 0:
            raise ValueError("Arquivo vazio")
        
        # Faz upload usando o método correto
        result = supabase.storage \
            .from_(settings.SUPABASE_BUCKET) \
            .upload(
                path=filename,
                file=file_content,
                file_options={
                    "content-type": "application/zip",
                    "upsert": "true"  # Use string em vez de bool
                }
            )
        
        print(f"✅ Upload realizado: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        raise