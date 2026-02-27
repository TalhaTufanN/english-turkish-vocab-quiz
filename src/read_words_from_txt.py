import re

# İngilizce kelimeleri TXT dosyasından oku ve boş satırlarını temizle
# Kelime türü kısaltmalarını (adj., v., n., adv. vb.) temizle
def read_words_from_txt(file_path):
    # Yaygın kelime türü kısaltmaları (birden fazla virgülle ayrılmışları da yakalar, örn: "v., n.")
    word_type_pattern = r'\s+(?:(?:adj|adv|n|v|prep|conj|pron|interj|art|num|aux|det|int|modal|part|phr|phr\.v|phrasal)\.?\s*,?\s*)+$'
    
    with open(file_path, "r", encoding="utf-8") as file:
        words = []
        for line in file:
            line = line.strip()
            if line:
                # Kelime türü kısaltmalarını tamamen kaldır
                cleaned_word = re.sub(word_type_pattern, '', line, flags=re.IGNORECASE)
                words.append(cleaned_word.strip())
                    
    return words
