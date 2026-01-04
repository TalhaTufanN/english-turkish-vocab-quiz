import random
# Şıklar oluştur (doğru cevap + 3 yanlış seçenek)
def generate_choices(correct_word, all_words):
    choices = [correct_word]
    wrong_choices = random.sample([w for w in all_words if w != correct_word], 3)
    choices.extend(wrong_choices)
    random.shuffle(choices)
    return choices

