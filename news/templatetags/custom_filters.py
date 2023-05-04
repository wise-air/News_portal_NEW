import string
from django import template


register = template.Library()


@register.filter()
def censor(text, cens):
    text_list = text.split()
    censored_text_list = []
    cens = ["мира", 'слабо', 'клим']

    for n in text_list:
        word = ''.join(_ for _ in n if _ not in string.punctuation)
        if word.lower() in cens:
            censored_word = word[0] + '***'
            censored_text_list.append(n.replace(word, censored_word))
        else:
            censored_text_list.append(n)

    return ' '.join(censored_text_list)




