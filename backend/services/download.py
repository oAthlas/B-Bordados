# services/download.py
from django.conf import settings
from .supabase import supabase

def get_signed_url(file_path, expires=3600):
    """
    Link temporário (1h por padrão)
    """
    if supabase is None:
        raise Exception("Supabase não configurado. Verifique conexão.")
    
    try:
        # Remove espaços do caminho se houver
        file_path = str(file_path).strip()
        
        res = supabase.storage \
            .from_(settings.SUPABASE_BUCKET) \
            .create_signed_url(file_path, expires)
        
        # Diferentes versões da biblioteca retornam formatos diferentes
        if hasattr(res, 'signed_url'):
            return res.signed_url
        elif isinstance(res, dict):
            return res.get('signedURL') or res.get('signedUrl')
        else:
            return str(res)
            
    except Exception as e:
        print(f"❌ Erro ao criar URL assinada: {e}")
        print(f"Caminho: {file_path}")
        print(f"Bucket: {settings.SUPABASE_BUCKET}")
        raise