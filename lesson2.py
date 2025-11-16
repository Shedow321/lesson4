from gtts import gTTS
from pygame import *
import os
import time
import random

def text_to_speech(phrase: str, lang: str = "uk") -> str:
    """
    Озвучує текст і зберігає його у mp3 файл, потім програє.
    """
    filename = f"voice_{random.randint(1000, 9999)}.mp3"
    tts = gTTS(phrase, lang=lang)
    tts.save(filename)

    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.5)

    mixer.music.unload()
    mixer.quit()
    return filename


def delete_file(filename: str) -> bool:
    """
    Видаляє тимчасовий mp3 файл.
    """
    try:
        os.remove(filename)
        return True
    except Exception as e:
        print(f"Помилка при видаленні файлу: {e}")
        return False


while True:
    print("\nВибери мову:")
    print("1 - українська")
    print("2 - англійська")
    print("3 - іспанська")
    print("0 - вихід")

    choice = input("Твій вибір: ").strip()

    if choice == "0":
        print("Вихід з програми...")
        break

    if choice == "1":
        lang = "uk"
    elif choice == "2":
        lang = "en"
    elif choice == "3":
        lang = "es"
    else:
        print("Невірний вибір. Спробуй ще раз.")
        continue

    phrase = input("Введи фразу для озвучки: ").strip()

    if not phrase:
        print("Фраза не може бути порожньою.")
        continue

    file = text_to_speech(phrase, lang)
    success = delete_file(file)
    print(f"Файл видалено: {success}")
