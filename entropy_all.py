from collections import defaultdict
import itertools
from multiprocessing import Pool, cpu_count
from wordle import Wordle


def compute_entropy(guess, wordle):
    marks = defaultdict(int)
    for target in wordle.all_words:  # iter through whole list
        _, mark, _, _, _ = wordle.get_guess_result(target, guess)
        marks[''.join(mark)] += 1
    entropy = wordle.compute_entropy(marks)
    dict_en = {guess: entropy}
    return dict_en


if __name__ == '__main__':
    wordle = Wordle()
    # dict_en = {}
    # for guess in wordle.all_words[:100]:  # iter through whole list
    #     marks = defaultdict(int)
    #     for target in wordle.all_words[:100]:  # iter through whole list
    #         _, mark, _, _, _ = wordle.get_guess_result(target, guess)
    #         marks[''.join(mark)] += 1
    #     entropy = wordle.compute_entropy(marks)
    #     dict_en[guess] = entropy

    with Pool(cpu_count()) as pool:
        dict_en = pool.starmap(compute_entropy, [(guess, wordle) for guess in wordle.all_words])
    dict_en = dict(itertools.chain(*map(dict.items, dict_en)))

    with open('5letter_2315_entropy.txt', 'w') as f:
        for k in sorted(dict_en, key=dict_en.get, reverse=True):
            s = k + ' ' + str(round(dict_en[k], 3)) + '\n'
            f.write(s)
