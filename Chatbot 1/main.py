#imports
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import  LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle



stemmer=LancasterStemmer()


# use json to loop through intents.json file

with open("intents.json") as file:
    data=json.load(file)
print(data['intents'])

try:
    with open("data.pickle",'rb') as f:
        words,labels,training,output=pickle.load(f)

except:

    words=[]
    labels=[]
    docs_x=[]
    docs_y=[]

    for intent in data['intents']:
        for pattern in intent['patterns']:
            # tokenize= get all the words in a pattern

            wrds=nltk.word_tokenize(pattern)
            #put all the tokenized words in the words list

            words.extend(wrds)

            #add pattern of words to docs

            docs_x.append(wrds)
            docs_y.append(intent['tag'])

            if intent['tag'] not in labels:
                labels.append(intent['tag'])

 #stem all the words in the words list and remove all the dupliacte elements


            words= [stemmer.stem(w.lower()) for w in words if w not in "?"]

            words=sorted(list(set(words)))

            #sort your labels

            labels=sorted(labels)
             # create a bag of words-one hot encoded

    training=[]
    output=[]

    out_empty=[0 for _ in  range(len(labels))]

    for x,doc in enumerate(docs_x):
        bag=[]

        wrds=[stemmer.stem(w.lower()) for w in doc] 

        for w in words:
            if w in wrds:
                bag.append(1) # this word exists

            else:
                bag.append(0)  #  this word does not exist

        output_row=out_empty[:]

        output_row[labels.index(docs_y[x])]=1  

        training.append(bag)
        output.append(output_row)

    training=np.array(training)
    output=np.array(output)


    with open("data.pickle",'wb') as f:
        pickle.dump((words,labels,training,output),f)

tf.compat.v1.reset_default_graph()
net=tflearn.input_data(shape=[None,len(training[0])])
net=tflearn.fully_connected(net, 8)   #add the fully connected layer to the neural network and add 8 neurons to the hidden layer
net=tflearn.fully_connected(net, 8)
net=tflearn.fully_connected(net, len(output[0]), activation="softmax")
net=tflearn.regression(net)

model=tflearn.DNN(net)


try:
    model.load("model.tflearn")

except:


    #n_epoch= no of epochs= how many times the model will see the data
    model.fit(training,output,n_epoch=2000,batch_size=8,show_metric=True)

    model.save("model.tflearn")

def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]
    s_words=nltk.word_tokenize(s)


    s_words=[stemmer.stem(word.lower()) for word in s_words]


    for se in s_words:
        for i,w in enumerate(words):
            if w == se:   #if the current word we r looking at is equal to the word in the sentence
                bag[i]=1  #the word exists

    return np.array(bag)

def chat():
    print("Start talking with the bot(type quit to stop)")

    while True:
        inp=input("You:")   #u type to the bot

        if inp.lower() == 'quit':
            break


        results= model.predict([bag_of_words(inp,words)])
        results_index=np.argmax(results)
        tag=labels[results_index]
        

        for tg in data['intents']:
            if tg['tag']==tag:
                responses=tg['responses']

        print(random.choice(responses))
       

chat()       








