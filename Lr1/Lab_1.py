import re
import statistics

def File_Conversion():
    text_file = open('file.txt', 'r')
    text_file = text_file.read().lower().replace('!','.').replace('?','.').replace(',','').replace('-','').replace('mr.','mister')
    return text_file

def Words_Counter():
    text_file = File_Conversion()
    pattern = re.findall(r'\b[a-z]{2,15}\b', text_file)
    dictionary = {}
    for word in sorted(pattern, key=len):
        count = dictionary.get(word, 0)  # 0 - default value
        dictionary[word] = count + 1
    for words in dictionary.keys():
        print(words, "-", dictionary[words])

def Averange_Number_Of_Words():
    text_file = File_Conversion()
    l = text_file.split(' ')
    c = text_file.count('.')
    print("\nAverange number of words: ", round(len(l)/c))

def Median_Count_Words():
    text_file = File_Conversion()
    print("Median count of words: ", (statistics.median([len(sentence.split()) for sentence in text_file.split(".")])))

def Search_Top(n,k):
    text_file = File_Conversion()
    text_file = re.findall(r'\b[a-z]{2,15}\b', text_file)
    words_dict = {}
    ngram_dict = {}
    print("n=", n, "k=", k)
    for word in text_file:
        count = words_dict.get(word, 0)  # 0 - default value
        words_dict[word] = count + 1
    for word in words_dict.keys():
        if len(word) >= n:
            tmp_word = word
            n_count = 0
            n_ends = n
            for i in range(len(word) - n_ends + 1):
                ngram = tmp_word[n_count:n_ends]
                if ngram in ngram_dict.keys():  # if ngram already exist in ngram_dict
                    ngram_dict[ngram] += words_dict[word]
                else:
                    ngram_dict[ngram] = words_dict[word]
                n_count += 1
                n_ends += 1

    ngram_dict = {k: ngram_dict[k] for k in sorted(ngram_dict,key=ngram_dict.get, reverse=True)}
    tmp_k = 0
    print("\nTop", k, "n-gram")
    for words in ngram_dict:
        if tmp_k < k:
            print( words, "-", ngram_dict[words])
            tmp_k += 1

def Main():
    text_file = open('file.txt', 'r')
    print(text_file.read())
    Words_Counter()
    Averange_Number_Of_Words()
    Median_Count_Words()
    check = input("N = 4 and K = 10? (y/n): ")
    if check == 'y':
        n = 4
        k = 10
        Search_Top(n, k)
    else:
        n = int(input("Write n: "))
        k = int(input("Write k: "))
        Search_Top(n, k)

if __name__ == "__main__":
    Main()