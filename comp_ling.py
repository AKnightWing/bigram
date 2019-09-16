#GITHUB LINK:
#https://github.com/AKnightWing/bigram

#PREREQUISITES
#A function to print a 2D Matrix in a proper, neat way. It takes a 2D List as input and prints it
import os
def print2dlist(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    
#A function that Calculates count of "first second" pair of words in corpus
def bigram_count(corpus,first,second):
    return(corpus.count(" "+first+" "+second+" "))

#A function that Calculates MLE conditional probability of first given second; i.e P(first|second)
def prob_mle(corpus,first,second):
        bigram_count=corpus.count(" "+first+" "+second+" ")
        unigram_count=corpus.count(" "+first+" ")
        return(round(bigram_count/unigram_count,4))
            
#A function that Calculates Laplace probability of first given second; i.e P(first|second)
def prob_laplace(corpus,first,second,vocab_length):
        adjusted_bigram_count=corpus.count(" "+first+" "+second+" ")+1
        adjusted_unigram_count=corpus.count(" "+first+" ")+vocab_length
        return(round(adjusted_bigram_count/adjusted_unigram_count,4))

#A function to calculate the product of all elements in a list
def  product_list(mylist):
    prod=1
    for elem in mylist:
        prod=prod*elem
    return(prod)

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"mothergoosecorpus.txt")

file=open(dir_path,"r")        #Open file
raw_corpus=file.read()      #Store file as a raw string
corpus=raw_corpus.replace('\n',' ')     #Replace all \n characters with spaces; useful for probability calculation
vocab_dict={}       #Dictionary that holds the vocabulary
split_corpus=raw_corpus.split()     #Store individual words of the corpus as a list


#Part 1
print("-----------START OF PART 1------------")
for one_word in split_corpus:       #Loop to add words to the vocabulary dictionary
    vocab_dict.setdefault(one_word,0)
    vocab_dict[one_word]=vocab_dict[one_word] + 1
del vocab_dict['<s>']       #Delete <s> from vocabulary, as mentioned in class

print("The Vocabulary is as follows:")
for key in vocab_dict.keys():
    print(key)
vocab_length=len(vocab_dict.keys())     #Calculate vocabulary length for future calculations
print("-----------END OF PART 1--------------")


#Part 2
print("-----------START OF PART 2------------")
prob_dict={}        #Dictionary that holds the probability of each unigram
for key in vocab_dict.keys():
    prob_dict[key]=vocab_dict[key]/sum(vocab_dict.values())

all_probabilities=sorted(prob_dict.items(), key=lambda x: x[1],reverse=True)        #This is a list of tuples containing word_name,probability

for tup in all_probabilities[0:2]:      #Loop to print all unigrams having the highest probability
    print("The word '{}' has probability = {}".format(tup[0],tup[1]))

print("-----------END OF PART 2--------------")


#Part 3
print("-----------START OF PART 3------------")
firstrow=[' ']      #The first row in the 2D list will be the vocabulary
for key in vocab_dict.keys():
    firstrow.append(key)

starting_matrix=[]      #A n*n 2D list which stores only the skeleton of the matrix
for i in range(vocab_length+1):
    if i==0:
        starting_matrix.append(firstrow)
    else:
        row=[]
        for j in range(vocab_length+1):
            if j==0:
                row.append(firstrow[i])
            else:
                row.append(0)
        starting_matrix.append(row)
        
count_matrix=[]         #A n*n 2D list which stores the bigram counts
for i in range(vocab_length+1):
    if i==0:
        count_matrix.append(firstrow)
    else:
        row=[]
        for j in range(vocab_length+1):
            if j==0:
                row.append(firstrow[i])
            else:
                row.append(bigram_count(corpus,starting_matrix[i][0],starting_matrix[0][j]))
        count_matrix.append(row)
        
prob_mle_matrix=[]         #A n*n 2D list which stores the MLE probability
for i in range(vocab_length+1):
    if i==0:
        prob_mle_matrix.append(firstrow)
    else:
        row=[]
        for j in range(vocab_length+1):
            if j==0:
                row.append(firstrow[i])
            else:
                row.append(prob_mle(corpus,starting_matrix[i][0],starting_matrix[0][j]))
        prob_mle_matrix.append(row)
        
print("The Matrix of MLE Probabilities is as follows:")
print2dlist(prob_mle_matrix)
print("-----------END OF PART 3--------------")



#Part 4
print("-----------START OF PART 4------------")
max_val=0
max_bigram_list=[]         #A list which stores the bigrams having max frequency
for i in range(len(count_matrix)):
    for j in range(len(count_matrix)):
        if type(count_matrix[i][j])==int:
            if count_matrix[i][j]==max_val:
                max_bigram_list.append(starting_matrix[i][0]+" "+starting_matrix[0][j])
            if count_matrix[i][j]>max_val:
                max_bigram_list=[]
                max_bigram_list.append(starting_matrix[i][0]+" "+starting_matrix[0][j])
                max_val=count_matrix[i][j]
                
print("The most frequent bigrams has/have frequency {} and is/are:".format(max_val))
print(str(max_bigram_list)[1:-1])
print("-----------END OF PART 4--------------")



#Part 5
print("-----------START OF PART 5------------")
prob_laplace_matrix=[]         #A n*n 2D list which stores the Laplacian probability
for i in range(vocab_length+1):
    if i==0:
        prob_laplace_matrix.append(firstrow)
    else:
        row=[]
        for j in range(vocab_length+1):
            if j==0:
                row.append(firstrow[i])
            else:
                row.append(prob_laplace(corpus,starting_matrix[i][0],starting_matrix[0][j],vocab_length))
        prob_laplace_matrix.append(row)
        
print("The Matrix of Laplace Probabilities is as follows:")
print2dlist(prob_laplace_matrix)
print("-----------END OF PART 5--------------")



#Part 6
print("-----------START OF PART 6------------")

zero_count_coordinates=[]       #A list which stores all indices of unseen bigrams
for i in range(vocab_length+1):
    for j in range(vocab_length+1):
        if type(count_matrix[i][j])==int:
            if count_matrix[i][j]==0:
                zero_count_coordinates.append((i,j))

unseen_bigram_dict={}       #A dictionary which stores all unseen bigrams
for i in range(vocab_length+1):
    for j in range(vocab_length+1):
        if(i,j) in zero_count_coordinates:
            unseen_bigram_dict.setdefault(count_matrix[i][0]+" "+count_matrix[0][j],0)
            unseen_bigram_dict[count_matrix[i][0]+" "+count_matrix[0][j]]=prob_laplace_matrix[i][j]
            
print("The probability of an unseen bigram is thus either of:")
print(set(unseen_bigram_dict.values()))
print("Type the word 'more' and press enter to look at all unseen bigrams and their probabilities")
print("If not, just press enter to continue to part 7")
temp=input()
#Print all unseen bigrams and their probabilities
if temp.lower()=="more":
    for key in unseen_bigram_dict.keys():
        print(str(key)+": "+str(unseen_bigram_dict[key]))
    
print("-----------END OF PART 6--------------")


#Part 7
print("-----------START OF PART 7------------")

count_of_counts_dict={}       #A dictionary which stores count of count values for all bigrams
for i in range(vocab_length+1):
    for j in range(vocab_length+1):
        if type(count_matrix[i][j])==int:
            count_of_counts_dict.setdefault(count_matrix[i][j],0)
            count_of_counts_dict[count_matrix[i][j]]=count_of_counts_dict[count_matrix[i][j]]+1

all_keys_list=list(count_of_counts_dict.keys())       #Convert it to a list for sorting
all_keys_list.sort()

count_of_counts_list=[["Count","No. of bigrams"]]
for key in all_keys_list:
    count_of_counts_list.append([key,count_of_counts_dict[key]])
print("The count of counts table is")
print2dlist(count_of_counts_list)
print("-----------END OF PART 7--------------")



#Part 8
print("-----------START OF PART 8------------")
print("The count of counts table needs to be smoothed, for preparation of the data for calculation of the Good-Turing probability. For the calculation of the probability of the ith (in ascending order of frequency) bigram, we have to divide it by the number of occurences of the (i-1)th bigram. If this frequency is zero, it'll give us a NaN error, and thus we smooth it out to avoid division by zero.")
print("-----------END OF PART 8--------------")

#Part 9
print("-----------START OF PART 9------------")
test_sentence="<s> peter piper picked a pickled peppers </s>"
#Split test sentences into a unigram list called set1 and shift it and call it set2
set1=test_sentence.split()
set2=set1[1:]
del(set1[0])
del(set2[0])
del(set1[-1])

sentence_bigrams=[]     #List to store all bigrams in given sentence, which is nothing but ith element of set1 and set2.
for i in range(len(set1)):
    sentence_bigrams.append(set1[i]+" "+set2[i])
    
mle_prob_sentence_bigrams=[]     #List to store MLE probabilities of pairwise brigrams in the given sentence
laplace_prob_sentence_bigrams=[]     #List to store Laplace probabilities of pairwise brigrams in the given sentence
for a_bigram in sentence_bigrams:
    first_word=a_bigram.split()[0]
    second_word=a_bigram.split()[1]
    mle_prob_sentence_bigrams.append(prob_mle(corpus,first_word,second_word))
    laplace_prob_sentence_bigrams.append(prob_laplace(corpus,first_word,second_word,vocab_length))

pmle=product_list(mle_prob_sentence_bigrams)       #Take a product of all the pairwise bigram MLE probabilities in the given sentence
plap=product_list(laplace_prob_sentence_bigrams)   #Take a product of all the pairwise bigram Laplace probabilities in the given sentence
print("The probability of the above test sentence is")

print("Using MLE:      {}".format(pmle))
print("Using Laplace:      {}".format(plap))
print("-----------END OF PART 9--------------")



