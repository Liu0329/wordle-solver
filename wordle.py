import random
import math
import functools
from collections import defaultdict
import itertools
from multiprocessing import Pool, cpu_count
from colorama import Fore
import pdb

# words_3 = [w for w in words if len(w) == 3]  # 939
# words_4 = [w for w in words if len(w) == 4]  # 3082
# words_5 = [w for w in words if len(w) == 5]  # 5196
# words_6 = [w for w in words if len(w) == 6]  # 7696
# words_7 = [w for w in words if len(w) == 7]  # 9146
# words_8 = [w for w in words if len(w) == 8]  # 9896
# print(len(words_3), len(words_4), len(words_5), len(words_6), len(words_7), len(words_8))

# https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
# deprecated
letter_freq = {
    'e': 56,
    'a': 43,
    'r': 38,
    'i': 38,
    'o': 36,
    't': 35,
    'n': 33,
    's': 29,
    'l': 27,
    'c': 23,
    'u': 18,
    'd': 17,
    'p': 16,
    'm': 15,
    'h': 15,
    'g': 12,
    'b': 10,
    'f': 9,
    'y': 9,
    'w': 6,
    'k': 5,
    'v': 5,
    'x': 1,
    'z': 1,
    'j': 1,
    'q': 1
}
assert len(letter_freq) == 26


def compare(w1, w2):
    if len(set(w1)) != len(set(w2)):
        return len(set(w2)) - len(set(w1))
    else:
        f1 = sum([letter_freq[c] for c in w1])
        f2 = sum([letter_freq[c] for c in w2])
        return f2 - f1


class Wordle:
    def __init__(self):
        print(Fore.WHITE + 'Welcome to the game of wordle with 3|4|5|6|7|8 letters.')
        print('Print the number of letters you want to play: (default 5)')
        length = int(input() or '5')
        self.mode = 'other'
        if length == 5:
            # self.all_words = [line.strip() for line in open('orig_wordle_list.txt')]
            print('Choose 0:easy (2315 common words as targets also for use) \n'
                  '       1:standard (2315 targets, 10k+ words to use, same as online wordle) \n'
                  '       2:hard (every guess has to obey the showed colors, same as online wordle hard mode) \n'
                  '       3:rare (the target is from 10k+ words)\n'
                  '       (default easy)' or '0')
            mode = int(input() or '0')
            if mode == 0:
                self.mode = 'easy'
                self.target_words = [line.strip().split()[0] for line in open('5letter_2315_entropy.txt')]
                self.all_words = [line.strip().split()[0] for line in open('5letter_2315_entropy.txt')]
            elif mode == 1:
                self.mode = 'standard'
                self.target_words = [line.strip().split()[0] for line in open('5letter_2315_entropy.txt')]
                self.all_words = [line.strip().split()[0] for line in open('5letter_entropy.txt')]
            elif mode == 2:
                self.mode = 'hard'
                self.target_words = [line.strip().split()[0] for line in open('5letter_2315_entropy.txt')]
                self.all_words = [line.strip().split()[0] for line in open('5letter_entropy.txt')]
            else:
                self.mode = 'rare'
                self.target_words = [line.strip().split()[0] for line in open('5letter_entropy.txt')]
                self.all_words = [line.strip().split()[0] for line in open('5letter_entropy.txt')]
        else:
            self.all_words = [line.strip().split()[0] for line in open(f'{length}letter_entropy.txt')]
            self.target_words = self.all_words.copy()

        self.words = self.target_words.copy()

    def get_guess_result(self, target, guess):
        mark = ['x'] * len(target)
        condition = [0] * len(target)
        have, not_have = set(), set()
        # first remove all-correct letters
        for i, (a, b) in enumerate(zip(target, guess)):
            if a == b:
                mark[i] = 'o'
                have.add(a)
    
        new_t, new_g = '', ''
        for i, c in enumerate(mark):
            if c != 'o':
                new_t += target[i]
                new_g += guess[i]
    
        cnt = {}
        for a in new_t:
            if a in cnt:
                cnt[a] += 1
            else:
                cnt[a] = 1

        for i, a in enumerate(guess):
            if mark[i] == 'o':  # all-correct
                condition[i] = a
                continue
            if a in new_t:  # should have but position wrong
                have.add(a)
                condition[i] = '~' + a
                if cnt[a] > 0:
                    mark[i] = '-'
                    cnt[a] -= 1
            else:
                mark[i] = 'x'
                condition[i] = '~' + a
                if a not in have:
                    not_have.add(a)

        win = set(mark) == {'o'}
        return condition, mark, have, not_have, win

    def print_colors(self, guesses, marks):
        for guess, mark in zip(guesses, marks):
            for a, m in zip(guess, mark):
                if m == 'o':
                    print(Fore.GREEN + a, end='')
                elif m == 'x':
                    print(Fore.WHITE + a, end='')
                elif m == '-':
                    print(Fore.YELLOW + a, end='')
            print(Fore.WHITE)

    def recommend_guess(self, guess, feedback):
        """
        feedback:
        e.g. xx--o means grey, grey, yellow, yellow, green
        """
        condition = [0] * len(guess)
        have, not_have = set(), set()
        for i, mark in enumerate(feedback):
            if mark == 'o':
                condition[i] = guess[i]
                have.add(guess[i])

        for i, mark in enumerate(feedback):
            if mark == 'x' and guess[i] not in have:
                not_have.add(guess[i])
            elif mark == '-':
                condition[i] = '~' + guess[i]
                have.add(guess[i])

        cands = self.filter_words(condition, have, not_have)
        return cands  # or random sample

    def word_has_letter(self, word, letters):
        """
        the word must have all these letters        
        """
        for a in letters:
            if a not in word:
                return False
        return True
    
    def word_has_no_letter(self, word, letters):
        """
        the word has none of these letters
        """
        for a in letters:
            if a in word:
                return False
        return True

    def compute_entropy(self, counts):
        """
        counts: e.g. {'p1': 5, 'p2': 2, ...}
        """
        s = sum(counts.values())
        probs = {k: p / s for k, p in counts.items()}
        bits = [-p * math.log(p, 2) for p in probs.values()]
        return sum(bits)

    def find_maximum_entropy_word(self):
        M = 0
        for guess in self.all_words:  # iter through whole list
            marks = defaultdict(int)
            for target in self.words:  # iter through candidates
                _, mark, _, _, _ = self.get_guess_result(target, guess)
                marks[''.join(mark)] += 1
            entropy = self.compute_entropy(marks)
            if entropy > M:
                M = entropy
                best = guess
        return best

    def compute_entropy_a_guess(self, guess):
        counts = defaultdict(int)
        for target in self.words:  # iter through legal list
            _, mark, _, _, _ = self.get_guess_result(target, guess)
            counts[''.join(mark)] += 1
        entropy = self.compute_entropy(counts)
        dict_en = {guess: entropy}
        return dict_en

    def compare(self, w1, w2):
        if w1[1] == w2[1]:
            if w1[0] in self.target_words:
                return -1
            elif w2[0] in self.target_words:
                return 1
            else:
                return 0
        else:
            return w2[1] - w1[1]

    def find_maximum_entropy_words_mp(self):
        with Pool(cpu_count()) as pool:
            if self.mode == 'hard':
                dict_en = pool.starmap(self.compute_entropy_a_guess, [(guess,) for guess in self.words])
            else:
                dict_en = pool.starmap(self.compute_entropy_a_guess, [(guess, ) for guess in self.all_words])
        dict_en = dict(itertools.chain(*map(dict.items, dict_en)))  # gather results
        large_en = sorted(dict_en, key=dict_en.get, reverse=True)
        # large_en = sorted(list(dict_en.items()), key=functools.cmp_to_key(self.compare))
        return large_en

    def filter_words(self, condition, have, not_have):
        """
        condition:
            e.g. ['a', 0, '~ab']
            'a': the position is surely 'a'
            0: the position can be anyone
            '~ab': the position is surely not 'a' or 'b'
        have:
            e.g. 'abc' means the word should have these letters at some position
        not_have:
            e.g. 'abc' means the word must not have these letters at any position
        """
        candidates = []
        for word in self.words:
            valid = True
            for i, cond in enumerate(condition):  # for each letter/condition
                if cond == 0:
                    pass
                elif len(cond) == 1 and word[i] != cond:
                    valid = False
                    break
                elif word[i] in cond[1:]:
                    valid = False
                    break
    
            if valid and self.word_has_letter(word, have) and self.word_has_no_letter(word, not_have):
                candidates.append(word)

        return candidates
