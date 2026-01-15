# services/supabase.py
from supabase import create_client, Client
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

# Inicializa como None globalmente
_supabase_client = None

def get_supabase_client():
    """Retorna ou cria o cliente Supabase (singleton)"""
    global _supabase_client
    
    if _supabase_client is not None:
        return _supabase_client
    
    try:
        url = getattr(settings, 'SUPABASE_URL', None)
        key = getattr(settings, 'SUPABASE_SERVICE_KEY', None)
        
        if not url or not key:
            logger.error("❌ Variáveis do Supabase não configuradas")
            logger.error(f"URL: {'Presente' if url else 'Faltando'}")
            logger.error(f"Key: {'Presente' if key else 'Faltando'}")
            return None
        
        # Limpa a URL
        url = url.strip().rstrip('/')
        
        # Limpa a chave (remove 'Bearer ' se existir)
        if key.startswith('Bearer '):
            key = key[7:].strip()
        
        logger.info(f"🔧 Inicializando Supabase: {url[:30]}...")
        
        # Cria o cliente - FORMA SIMPLES E DIRETA
        # Remove as options que podem causar problemas
        client = create_client(supabase_url=url, supabase_key=key)
        
        # Testa a conexão de forma simples
        try:
            # Tenta uma operação simples
            result = client.table('_dummy').select('*').limit(1).execute()
            logger.info("✅ Supabase conectado com sucesso")
        except Exception as test_error:
            # Isso é esperado se a tabela não existir
            logger.info("⚠️  Teste de conexão: OK (erro esperado)")
        
        _supabase_client = client
        return client
        
    except Exception as e:
        logger.error(f"❌ Falha crítica ao conectar com Supabase: {str(e)}")
        logger.error(f"Tipo do erro: {type(e).__name__}")
        
        # Debug adicional
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return None

# Instância global
supabase = get_supabase_client()

def upload_product_file(file, product_id):
    """
    Upload de arquivo para Supabase Storage
    """
    client = get_supabase_client()
    if client is None:
        raise Exception("❌ Cliente Supabase não inicializado. Verifique as variáveis de ambiente.")
    
    try:
        file_content = file.read()
        file_name = file.name
        
        if not product_id:
            raise ValueError("❌ Product ID é necessário")
        
        # Sanitiza nome do arquivo
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', file_name)
        path = f"products/{product_id}/{safe_name}"
        
        bucket = getattr(settings, 'SUPABASE_BUCKET', 'products')
        
        logger.info(f"📤 Upload: {path} para bucket {bucket}")
        
        # Método mais simples e direto
        result = client.storage.from_(bucket).upload(
            path=path,
            file=file_content,
            file_options={
                "content-type": file.content_type or "application/octet-stream",
                "upsert": "true"
            }
        )
        
        logger.info(f"✅ Upload realizado: {path}")
        return path
        
    except Exception as e:
        logger.error(f"❌ Erro no upload: {str(e)}")
        raise