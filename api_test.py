from googletrans import Translator

translator = Translator()
result = translator.translate('안녕하세')

print(result.src)
print(result.dest)
print(result.origin)
print(result.text)
print(result.pronunciation)
