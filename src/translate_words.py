import deepl
import time
import os
try:
    from dotenv import load_dotenv
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(env_path)
except ImportError:
    pass 

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
if not DEEPL_API_KEY:
    raise ValueError("DEEPL_API_KEY environment variable is not set. Please set it in your environment or create a .env file in the root directory with DEEPL_API_KEY=your_key")
translator = deepl.Translator(DEEPL_API_KEY)

# Kelimeleri Türkçeye çevir
def translate_words(words):
    translations = {}
    total_words = len(words)
    
    for idx, word in enumerate(words, 1):
        max_retries = 5
        retry_delay = 2  # İlk retry'da 2 saniye bekle
        
        for attempt in range(max_retries):
            try:
                # İstekler arasında bekleme (rate limiting için)
                if idx > 1:  # İlk kelimeden sonra bekle
                    time.sleep(0.5)  # Her istek arasında 0.5 saniye bekle
                
                translated = translator.translate_text(word, target_lang="TR").text
                translations[word] = translated
                
                # İlerleme göster
                if idx % 10 == 0 or idx == total_words:
                    print(f"  {idx}/{total_words} kelime çevrildi...")
                
                break  # Başarılı oldu, döngüden çık
                
            except deepl.exceptions.TooManyRequestsException:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"  Çok fazla istek! {wait_time} saniye bekleniyor... (Deneme {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"  HATA: '{word}' kelimesi çevrilemedi (çok fazla deneme sonrası)")
                    translations[word] = f"[Çevrilemedi: {word}]"
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"  Hata oluştu: {e}. {wait_time} saniye bekleniyor... (Deneme {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"  HATA: '{word}' kelimesi çevrilemedi: {e}")
                    translations[word] = f"[Çevrilemedi: {word}]"
    
    return translations

