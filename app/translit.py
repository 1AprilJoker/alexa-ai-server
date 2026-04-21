import re

RU_MAP = {
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"yo",
    "ж":"zh","з":"z","и":"i","й":"y","к":"k","л":"l","м":"m",
    "н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u",
    "ф":"f","х":"h","ц":"ts","ч":"ch","ш":"sh","щ":"shch",
    "ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya"
}


def to_phonetic(text: str):

    text = text.lower()

    # заменяем знаки препинания на паузы SSML
    text = re.sub(r"[–—-]", " <break time='300ms'/> ", text)
    text = re.sub(r"[.]", " <break time='500ms'/> ", text)
    text = re.sub(r"[,]", " <break time='200ms'/> ", text)

    result = []
    i = 0

    while i < len(text):

        # пропускаем SSML теги как есть
        if text[i] == "<":
            tag_end = text.find(">", i)
            result.append(text[i:tag_end+1])
            i = tag_end + 1
            continue

        char = text[i]
        result.append(RU_MAP.get(char, char))
        i += 1

    return "".join(result)
