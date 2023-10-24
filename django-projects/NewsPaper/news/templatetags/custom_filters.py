from django import template

register = template.Library()

@register.filter(name='censor')

def censor(value, arg):
    bad_words = ['wddd', 'dfghjfgh', 'fghjk', 'tgm']
    for word in bad_words:
        value = value.replace(word, arg)
    return value
