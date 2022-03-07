import random
from colorama import Fore
from wordle import Wordle

if __name__ == '__main__':
    wordle = Wordle()
    attempt = 1
    guesses = wordle.words[:5]
    while True:
        if len(wordle.words) > 2:
            print(Fore.RED + f'probe words with maximum entropy: {guesses[:5]}')
        hints = wordle.words[:50]
        n = min(len(hints), 10)
        print(Fore.GREEN + f'hints: {random.sample(hints, n)}')
        guess = input(Fore.WHITE + 'your guess: ')
        feedback = input('your feedback: (o is green, x is grey, - is yellow) \n')
        if set(feedback) == {'o'}:
            break
        wordle.words = wordle.recommend_guess(guess, feedback)
        # print(wordle.words)
        if len(wordle.words) > 2:
            guesses = wordle.find_maximum_entropy_words_mp()
