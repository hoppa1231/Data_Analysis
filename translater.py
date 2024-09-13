from googletrans import Translator

def translate_to_russian(text):
    try:
        translator = Translator()
        translated = translator.translate(text, dest='ru')
        return translated.text
    except:
        return 1
