# services/supabase.py
from supabase import create_client, Client
from django.conf import settings
import socket

def create_supabase_client():
    """Cria e retorna cliente Supabase com tratamento de erros"""
    try:
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_SERVICE_KEY
        
        if not url or not key:
            raise ValueError("URL ou Service Key do Supabase não configurados")
        
        # Remove trailing slash se existir
        url = url.rstrip('/')
        
        # Testa conexão de rede
        if url.startswith('https://'):
            hostname = url.replace('https://', '').split('/')[0]
            # Testa DNS
            socket.gethostbyname(hostname)
        
        # Cria cliente
        client: Client = create_client(url, key)
        
        # Testa conexão simples
        client.auth.get_session()
        
        print(f"✅ Supabase conectado: {url}")
        return client
        
    except socket.gaierror as e:
        print(f"❌ Erro DNS - Não conseguiu resolver {url}: {e}")
        print("Verifique: 1. Conexão com internet 2. URL correta 3. DNS funcionando")
        return None
    except Exception as e:
        print(f"❌ Erro ao conectar com Supabase: {e}")
        return None

# Cria o cliente global
supabase = create_supabase_client()

def upload_product_file(file, product_id):
    """
    file = UploadedFile do Django
    """
    if supabase is None:
        raise Exception("Cliente Supabase não inicializado. Verifique conexão.")
    
    try:
        file_content = file.read()
        file_name = file.name
        
        # Sanitiza nome do arquivo
        safe_name = file_name.replace(' ', '_').replace('/', '_')
        path = f"products/{product_id}/{safe_name}"
        
        # Faz upload
        result = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            path,
            file_content,
            {
                "content-type": file.content_type or "application/octet-stream",
                "upsert": True
            }
        )
        
        print(f"✅ Upload realizado: {path}")
        return path
        
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        raise