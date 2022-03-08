import os
import platform
import random
from wordle import Wordle


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == '__main__':
    wordle = Wordle()
    while True:
        target = random.choice(wordle.target_words)
        attempt = 1
        guesses, marks, can_use, exclude = [], [], set('abcdefghijklmnopqrstuvwxyz'), set()
        while True:
            exclude_format = "\u0336" + "\u0336".join(sorted(exclude))
            guess = input(f'Input your guess: from {"".join(sorted(can_use))}, {exclude_format}\n')
            guesses.append(guess)
            if wordle.mode != 'hard' and guess not in wordle.all_words:
                print('word not in our word list')
                continue
            if wordle.mode == 'hard' and guess not in wordle.words:
                print('word has to obey the colors')
                continue
            condition, mark, have, not_have, win = wordle.get_guess_result(target, guess)
            if wordle.mode == 'hard':
                wordle.words = wordle.filter_words(condition, have, not_have)
            exclude.update(not_have)
            can_use = can_use - not_have
            marks.append(mark)

            clear_screen()

            wordle.print_colors(guesses, marks)
            if win:
                print(f'WIN after {attempt} attempts!!!')
            attempt += 1
