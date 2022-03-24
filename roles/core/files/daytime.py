#!/usr/bin/env python3

import sys
import re
import time

wait_reply = True
run_test = False
daytime_dir = 'extras'
language = ''


def get_language():
    agi_vars = {}
    while True:
        line = input().strip()
        if not line:
            break
        mo = re.match('^agi_([^:]+): (.*)$', line)
        if mo:
            name = mo.group(1).strip()
            value = mo.group(2).strip()
            agi_vars[name] = value
    return agi_vars.get('language', 'en')


def choose_num_word(num, word1, word234, wordx):
    num = int(num)
    if num == 1:
        return word1
    if num >= 5 or num <= 0:
        return wordx
    return word234


def choose_num_digit(num, gender):
    num = int(num)
    if language != 'ru':
        gender = ''
    if gender != 'f':
        gender = ''
    if num != 1 and num != 2:
        gender = ''
    return str(num) + gender


def saynum1000(words, num, gender, skip01, word1, word234, wordx):
    num = int(num) % 1000
    if num >= 100:
        if language == 'ru':
            words.append(choose_num_digit(num - num % 100, ''))
        else:
            words.append(choose_num_digit(int(num / 100), ''))
            words.append('hundred')
        num %= 100
        if num == 0:
            num = -1
    if num >= 20:
        words.append(choose_num_digit(num - num % 10, gender))
        num %= 10
        if num == 0:
            num = -1
    if num >= 0 and (not skip01 or num >= 2):
        words.append(choose_num_digit(num, gender))
    if wordx:
        words.append(choose_num_word(num, word1, word234, wordx))


def saynum(num, gender, word1, word234, wordx):
    num = int(num)
    words = []
    if num < 0:
        words.append('minus')
        num = -num
    num %= 1000000000
    if num >= 1000000:
        if language == 'ru':
            saynum1000(words, num / 1000000, '', True,
                       'million', 'million-a', 'millions')
        else:
            saynum1000(words, num / 1000000, '', True,
                       'million', 'million', 'million')
        num %= 1000000
        if num == 0:
            num = -1
    if num >= 1000:
        if language == 'ru':
            saynum1000(words, num / 1000, 'f', True,
                       'thousand', 'thousands-i', 'thousands')
        else:
            saynum1000(words, num / 1000, 'f', True,
                       'thousand', 'thousand', 'thousand')
        num %= 1000
        if num == 0:
            num = -1
    saynum1000(words, num, gender, 0, word1, word234, wordx)
    return '&'.join(w for w in words)


def say_time():
    tm = time.localtime()
    words = []
    if language == 'ru':
        words.append(saynum(tm.tm_hour, 'm',
                            'hour', 'hours-a', 'hours'))
    else:
        words.append(saynum(tm.tm_hour, '',
                            'hours', 'hours', 'hours'))
    if tm.tm_min:
        if language == 'ru':
            words.append(saynum(tm.tm_min, 'f',
                                'minute', 'minutes-i', 'minutes'))
        else:
            words.append(saynum(tm.tm_min, '',
                                'minute', 'minutes', 'minutes'))
    return words


def test_words():
    words = []
    for x in range(0, 25):
        if language == 'ru':
            words.append(saynum(x, 'm', 'hour', 'hours-a', 'hours'))
        else:
            words.append(saynum(x, '', 'hours', 'hours', 'hours'))
    for x in range(0, 60):
        if language == 'ru':
            words.append(saynum(x, 'f', 'minute', 'minutes-i', 'minutes'))
        else:
            words.append(saynum(x, '', 'minute', 'minutes', 'minutes'))
    return words


def play(words):
    if type(words) is not str:
        words = '&'.join(words)
    words = re.split('&', words)
    for word in words:
        print('STREAM FILE {}/{} ""'.format(daytime_dir, word.strip()))
        if wait_reply:
            input()


if __name__ == '__main__':
    try:
        language = get_language()
        play(test_words() if run_test else say_time())
    except Exception as ex:
        if run_test:
            print('Exception: %s' % ex, file=sys.stderr)  # NOQA
    sys.exit(0)
