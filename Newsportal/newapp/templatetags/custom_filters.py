from django import template
import re

register = template.Library()

BAD_WORDS = ['редиска', 'чорный', 'lorem'] # Lorem часто используется, по этому для примера добавил его

@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor применяется только к строкам.")
    
    for word in BAD_WORDS:
        # Создаем регулярное выражение для поиска слова с учетом регистра
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        # Заменяем слово на его цензурированную версию
        value = pattern.sub(word[0] + '*' * (len(word) - 1), value)
    
    return value