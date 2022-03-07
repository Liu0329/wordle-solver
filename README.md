[Wordle](https://www.nytimes.com/games/wordle/index.html) is a popular online word guessing game. To win, you should guess the word in six tries.
Each guess must be a valid five-letter word.
After each guess, the color of the tiles will change to show how close your guess was to the word.
green means the letter is in the word and in the correct spot.
yellow means the letter is in the but in the wrong spot.
grey means the letter is not in the word in any spot.

![企业微信截图_164665837678](https://user-images.githubusercontent.com/8122099/157040041-e3ddafb1-d57d-4fab-bcad-345e750c8e37.png)

# wordle-solver
This powerful worlde-solver is written in python, run on terminal. Inspired by [3Blue1Brown's work](https://www.youtube.com/watch?v=v68zYyaEmEA), I use maxmum entropy to generate the next guess. It can help you win with least attempts statistically. And, assuming all target words share the same chance, I do not use word frequency to reweight them. In 2315/2315 words mode, the winning rate is 100%.

You can
### 1. play: with 3|4|5|6|7|8 (or more) letters of wordle
`python play.py` 

![企业微信截图_16466563081949](https://user-images.githubusercontent.com/8122099/157035008-85902e50-6b44-41bc-94ba-9f1c9742861c.png)

### 2. solve: as a good helper to solve online wordle of any version
`python solve.py`

![企业微信截图_16466564497878](https://user-images.githubusercontent.com/8122099/157035352-0add46ad-6588-4925-8909-5a5dd159dcc4.png)

### 3. experiment: get overall performance with all words in the word list
`python experiment.py`
|letter |target words| legal words| win | lose | winning rate(<=6) | avg attempts |min/max attempts |
|  ----  | ----  |----  | ----  | ----  |----  | ----  | ----  |
| 4  | 3076 | 3076 | 3051 | 25 | 99.19% | 4.40 |1/7|
| 5  | 2315 | 2315 | 2315 | 0  | 100.0% | 3.57 |1/6|
| **5**  | **2315** | **12972** | 2315 | 1  | 99.96% | 4.04 |2/7|
| 5  | 12972| 12972| 12936 | 36  | 99.72% |4.15 |1/7|
| 6  | 7634 | 7634 | 7634 | 0  | 100.0% | 3.40 |1/6|
| 7  | 8981 | 8981 | 8981 | 0  | 100.0% | 3.10 |1/5|

After removing rare words, current online wordle uses 2315 words for the targets, but 12972 words as legal try, as the 3rd line. The only word it fails is **jolly**. The reason is that there are so many *olly: polly, holly, golly, wolly, folly, jolly, lolly, molly ... 

Interestingly, the shorter the words, the harder it grows for the computer. Because there are more similar words, for instance: five, bide, tide, aide, kite, wine, wide, pide...

### online versions:

official 5-letter: https://www.nytimes.com/games/wordle/index.html

4|5|6|7-letter: https://www.thewordfinder.com/6-letter-wordle/

Try solve them using wordle-solver, feel the accuracy.
