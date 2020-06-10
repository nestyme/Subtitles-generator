# russian lang heuristics for google api.
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def reformat_rus(text):
    words = text.split(' ')
    result = ''

    for word in words:
        try:
            if 'Name' in morph.parse(word.replace('.',''))[1][1]:
                text = text.replace(f'. {word}', f' {word}')
        except:
            pass

    text = text.replace(' и.', ' и')
    text = text.replace('. Это ', ' - это ')
    text = text.replace(' это ', ', это ')
    text = text.replace(' как ', ', как ')
    text = text.replace(' где ', ', где ')
    text = text.replace(' который ', ', который ')
    text = text.replace(' которая ', ', которая ')
    text = text.replace(' которые ', ', которые ')
    text = text.replace(' таким образом ', ', таким образом, ')
    text = text.replace(' откуда ', ', откуда ')
    text = text.replace(' что ', ', что ')
    text = text.replace(' если ', ', если ')
    text = text.replace(',,', ',')
    text = text.replace(' -первых', '-первых,')
    text = text.replace(' -вторых', '-вторых,')
    text = text.replace(' но ', ', но ')
    text = text.replace(' а ', ', а ')
    text = text.replace(' да ', ', да ')
    return text

# detect_dot_before_name('Здравствуйте. Меня зовут. Александр и это короткая лекция и. Тема сегодняшней лекции. Это счастье. '
# 'Недавно мой знакомый спросил как быть счастливым и что нужно для этого делать')