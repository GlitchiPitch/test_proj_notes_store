import requests

def check_text(text: str) -> str:
    url: str = f"https://speller.yandex.net/services/spellservice.json/checkText?text={text}"
    answer = requests.get(url).json()

    for checked_word in answer:
        text = text.replace(checked_word['word'], checked_word['s'][0])

    return text
