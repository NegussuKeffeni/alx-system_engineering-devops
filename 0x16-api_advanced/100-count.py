#!/usr/bin/python3
""" recursive function that queries the Reddit API"""
import requests
import sys
import json
after = None
count_dic = []


def count_words(subreddit, word_list,hot_list=[],after=None):
    """parses the title of all hot articles, and prints a sorted count of given
    keywords (case-insensitive, delimited by spaces) """
    
    headers = {'User-Agent': 'xica369'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    parameters = {'after': after}
    response = requests.get(url, headers=headers, allow_redirects=False,
                            params=parameters)
    if response.status_code != 200:
        return None
    data = json.loads(response.text).get('data').get('children')
    after = json.loads(response.text).get('data').get('after')
    if data is None:
        if len(hot_list) == 0:
            print("")
            return
        word_count = {}
        word_list = list(set([word.lower() for word in word_list]))
        for word in word_list:
            word_count[word] = 0
        for word in word_list:
            for title in hot_list:
                for t in title.split():
                    if word == t.lower():
                        word_count[word] = word_count[word] + 1
        sort_word_count = sorted(word_count.items(), key=lambda x: x[1],
                                 reverse=True)
        for i in sort_word_count:
            if i[1] > 0:
                print("{}: {}".format(i[0], i[1]))
    else:
        for item in data:
            hot_list.append(item.get('data').get('title'))
    if after is None:
        if len(hot_list) == 0:
            print("")
            return
        word_count = {}
        word_list = list(set([word.lower() for word in word_list]))
        for word in word_list:
            word_count[word] = 0
        for word in word_list:
            for title in hot_list:
                for t in title.split():
                    if word.lower() == t.lower():
                        word_count[word] = word_count[word] + 1
        sort_word_count = sorted(word_count.items(), key=lambda x: x[1],
                                 reverse=True)
        for i in sort_word_count:
            if i[1] > 0:
                print("{}: {}".format(i[0], i[1]))
    else:
        return count_words(subreddit, word_list, hot_list, after)
