# open txt file
words = open('names.txt', 'r').read().splitlines() # readlines() returns a list of lines

# print the first 10 words
for word in words[:10]:
    print(word)

# Check the lenght of the list and print it
print('Length of the list: ', len(words))

# Check and print the shortest word
shortest = min(words, key=len)
print('Shortest word: ', shortest, len(shortest))

# Check and print the longest word
longest = max(words, key=len)
print('Longest word: ', longest, len(longest))


import torch
N = torch.zeros((27,27), dtype=torch.int32)

list_of_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.']
string_to_integer = {letter: i for i, letter in enumerate(list_of_letters)}
integer_to_string = {i: letter for i, letter in enumerate(list_of_letters)}

print(integer_to_string)

for w in words:
    # w = single name
    # add . to the end of the name
    w = '.' + w + '.'
    for i in range(len(w)-1):
        ch_1 = w[i]
        ch_2 = w[i+1]
        N[string_to_integer[ch_1], string_to_integer[ch_2]] += 1

# plot N as matrix
import matplotlib.pyplot as plt
plt.imshow(N)
plt.show()


# repeat until you get a .

import random
def generate_name():
    name = ''
    ch = integer_to_string[random.randint(0, 26)] # start with a random letter
    name += ch
    while ch != '.':
        # then sample the next letter from the distribution of the next letter
        ch = integer_to_string[torch.multinomial(N[string_to_integer[ch]].float(), 1).item()]
        name += ch
    return name

for i in range(10):
    print(generate_name())