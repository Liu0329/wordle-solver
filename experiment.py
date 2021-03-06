import random
from tqdm import tqdm
from wordle import Wordle

if __name__ == '__main__':
    total_attempts, m, M, num_win, num_lose = 0, 100, 0, 0, 0
    wordle = Wordle()
    for target in tqdm(wordle.target_words):
        attempt = 1
        wordle.words = wordle.target_words.copy()
        print(f'Target: {target}')
        while True:
            # print(f'Target: {target}')
            if attempt == 1:
                guess = wordle.all_words[0]
            elif len(wordle.words) <= 2:
                guess = wordle.words[0]
            else:
                guess = wordle.find_maximum_entropy_words_mp()[0]

            # print(f'Guess {attempt}: {guess}')

            condition, mark, have, not_have, win = wordle.get_guess_result(target, guess)
            if win:
                total_attempts += attempt
                M = max(attempt, M)
                m = min(attempt, m)
                if attempt > 6:
                    num_lose += 1
                else:
                    num_win += 1
                print(f'WIN after {attempt} attempts!!!')
                break
    
            # print(condition, mark, have, not_have)
            wordle.words = wordle.filter_words(condition, have, not_have)
            # print(wordle.words)
            attempt += 1
    
    print(f'average attempts to win: {total_attempts / len(wordle.target_words)}')
    print(f'maximum attempts: {M}, minimum attempts: {m}')
    print(f'win: {num_win}, lose: {num_lose}, winning rate: {num_win / (num_win + num_lose)}')
