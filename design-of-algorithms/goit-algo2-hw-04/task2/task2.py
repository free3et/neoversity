import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from trie import Trie

class LongestCommonWord(Trie):

    def find_longest_common_word(self, strings: list[str]) -> str:
        if not isinstance(strings, list) or not strings:
            raise TypeError(f"Невірні аргументи для find_longest_common_word: strings = {strings} має бути списком рядків")

        for str_word in strings:
            if not isinstance(str_word, str) or not str_word:
                raise TypeError(f"Невірні аргументи для find_longest_common_word: string = {str_word} має бути рядком")

        # Додаємо всі слова в Trie 
        for i, str_word in enumerate(strings): 
            self.put(str_word, i)

        # Пошук найдовшого спільного префікса
        current = self.root
        prefix = []
        while len(current.children) == 1 and current.value is None: # Поки гілка і вузол не кінець слова
            char = list(current.children.keys())[0] # Беремо перший символ
            current = current.children[char] # Переходимо до наступного вузла
            prefix.append(char)
        return "".join(prefix)

if __name__ == "__main__":
    # Тести
    trie = LongestCommonWord()
    strings = ["flower", "flow", "flight"]
    assert trie.find_longest_common_word(strings) == "fl"

    trie = LongestCommonWord()
    strings = ["interspecies", "interstellar", "interstate"]
    assert trie.find_longest_common_word(strings) == "inters"

    trie = LongestCommonWord()
    strings = ["dog", "racecar", "car"]
    assert trie.find_longest_common_word(strings) == ""
