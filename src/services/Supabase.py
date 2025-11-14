from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

supabase : Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

default_pic : str = 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg'

def get_img_url(path : str):
    return default_pic if path is None else supabase.storage.from_('images').create_signed_url(path, 3600).get('signedURL')