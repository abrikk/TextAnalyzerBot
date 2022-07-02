import json

from cld3 import get_frequent_languages
from aiogram import Dispatcher
from aiogram.types import Message

from string import punctuation
from collections import Counter


async def analyze_text(message: Message):
    text = str(Text(message.text))

    await message.reply(text)


def register_analyze_text(dp: Dispatcher):
    dp.register_message_handler(analyze_text, state="*")


class Text:
    def __init__(self, text: str):
        self._text: str = text

    def only_letters(self) -> str:
        testee_text = self._text
        for char in punctuation:
            testee_text = testee_text.replace(char, "")
        return testee_text

    def count_words(self) -> int:
        return len(self.only_letters().split())

    def count_symbols(self) -> int:
        return len(self._text)

    def count_punctuations(self) -> int:
        return self.count_symbols() - len(self.only_letters())

    def frequent_words(self, n: int or None = None) -> list:
        counted_words = Counter(self.only_letters().split()).most_common(n)
        return [(word, quantity) for word, quantity in counted_words if quantity >= 3]

    def number_of_languages(self):
        return len(self.detect_languages())

    def detect_languages(self):
        return get_frequent_languages(self._text, num_langs=10)

    def get_languages(self) -> str:
        with open("languages.json") as file:
            lang_codes = json.load(file)["main"]["en"]["localeDisplayNames"]["languages"]

        text = []

        for lang in self.detect_languages():
            lang_code = lang.language
            probability = f"{int(lang.probability * 100)}%"
            lang_name = lang_codes[lang_code]

            text.append(f"{lang_name} ({probability})")

        return ", ".join(text)

    def palindroms(self) -> str:
        stack: set[str] = set()
        for word in self.only_letters().split():
            if word == word[::-1] and len(word) >= 3:
                stack.add(word)
        return ", ".join(stack)

    def __str__(self):
        if self.count_words() < 3:
            return "The text is too short to analyze! There should be at least 3 words."
        else:
            language = "language" if self.number_of_languages() == 1 else "languages"
            text = [
                f"Number of characters: <code>{str(self.count_symbols())}</code>",
                f"Number of words: <code>{str(self.count_words())}</code>",
                f"Number of punctuations: <code>{str(self.count_punctuations())}</code>"
            ]

            if self.frequent_words(3):
                word = "word" if len(self.frequent_words(3)) == 1 else "words"
                frequent_words = ", ".join([f"<code>{word} - {quantity}</code>" for word, quantity in self.frequent_words(3)])
                text.append(f"The most {len(self.frequent_words(3))} frequent {word}: {frequent_words}")

            if self.palindroms():
                text.append(f"Palindroms: {self.palindroms()}")

            text.append(f"Detected {language}: {self.get_languages()}")

            return "\n".join(text)
