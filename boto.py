"""
This is the template server side for ChatBot
"""
import bottle
import requests
requests.get('https://geek-jokes.sameerkumar.website/api')
from bottle import route, run, template, static_file, request
import json
from textblob import TextBlob
import sched, time
s = sched.scheduler(time.time, time.sleep)
import string
string.ascii_lowercase


train = [
     ('I love this sandwich.', 'pos'),
     ('this is an amazing place!', 'pos'),
     ('I feel very good about these beers.', 'pos'),
     ('this is my best work.', 'pos'),
     ("what an awesome view", 'pos'),
     ('I do not like this restaurant', 'neg'),
     ('I am tired of this stuff.', 'neg'),
     ("I can't deal with this", 'neg'),
     ('he is my sworn enemy!', 'neg'),
     ('my boss is horrible.', 'neg'),
     ("I feel sad today", ".neg")
]
from textblob.classifiers import NaiveBayesClassifier
cl = NaiveBayesClassifier(train)


bottle.TEMPLATE_PATH.insert(0, '')

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    swear_words = ["anal", "anus", "arse", 'ass', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'blow job', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt',
'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'f u c k', 'fudgepacker', 'fudge packer', 'flange',
'Goddamn', 'God damn', 'hell', 'homo', 'jerk', 'jizz', 'knobend', 'knob end', 'labia', 'lmao', 'lmfao', 'muff', 'nigger', 'nigga', 'omg', 'penis', 'piss', 'poop', 'prick', 'pube', 'pussy', 'queer',
'scrotum', 'sex', 'shit', 'sh1t', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank' 'whore' 'wtf']
    pet_words = ("dog", "cat", "hamster", "bunny", "bird", "lizard", "mouse", "pet", "leash")
    money_words = ("coin", "dollar", "money", "wallet", "bank", "shekel")
    question_words = ("can", "aliyah", "army")
    user_message = request.POST.get('msg')
    b = TextBlob(user_message)
    print(b.sentiment)
    boto_response =str(b)
    translated_response = language_check(boto_response)
    translated_response_array = translated_response.split(" ")
    translated_blob = TextBlob(translated_response)
    translated_blob_array = translated_blob.words
    random_joke = joke_generator()
    boto_response = "Oh jeez, I don't know how to answer that one. I'm ony a couple of days old."
    boto_animation = "confused"
    if "You" in translated_blob or "you" in translated_blob:
        if any((word in question_words for word in translated_blob_array)):
            print(translated_blob_array)
            for item in translated_response_array:
                print(item)
                if item in question_words:
                    responses = question_response(item)
                    boto_response = responses[0]
                    boto_animation = responses[1]
        else:
            boto_response = "No " + str(translated_blob)
            boto_animation = "heartbroke"
    elif "Jacob Collins" in b:
        input_index = user_message.index("Jacob Collins") + len("Jacob Collins")
        boto_response = user_message[:input_index] + " is a Billy Bollins"
        boto_animation = "giggling"
    elif "I am" in translated_response and translated_blob.polarity <= -.5:
        boto_response = "If you or a friend is considering taking their own life. Please call the Israel suicide hotline at 972-9-8891333"
        boto_animation = "afraid"
    elif "I am" in translated_response or "i am" in translated_response:
        name_index = translated_response_array.index("am") + 1
        boto_response = "Hello " + translated_response_array[name_index]
        boto_animation = "excited"
    elif "my name is" in translated_response or "My name is" in translated_response:
        name_index = translated_response_array.index("is") + 1
        boto_response = "Hello " + translated_response_array[name_index]
        boto_animation = "excited"
    for item in translated_response_array:
        print(item)
        if item in swear_words:
            boto_response = "Why don't we talk again when you have something nice to say"
            boto_animation = "no"
    if translated_blob.polarity <= -.5:
        boto_response = "I'm sorry to hear that:("
        boto_animation = "crying"
    elif translated_blob.polarity >= .5:
        boto_response = "That's great!"
        boto_animation = "excited"
    if "what" and "is" in translated_blob:
        word = translated_blob_array[-1]
        definition = word.definitions
        boto_response = "A " + word + " is " + str(definition[0])
        boto_animation = "dancing"
    elif "what" and "mean" in translated_blob:
        print(translated_blob[-1])
        word = translated_blob_array[-2]
        definition = word.definitions
        boto_response = word.capitalize() + " has a few meanings, for example: " + str(definition[0]) + "," + str(definition[1]) + ". I hope that helps!"
        boto_animation = "dancing"
    if "joke" in translated_blob:
        boto_response = str(random_joke)
        boto_animation = "laughing"
    if "love" in translated_blob and "you" in translated_blob:
        boto_response = "Awww, boto loves you too"
        boto_animation = "inlove"
    if any((word in pet_words for word in translated_blob_array)):
        boto_response = "Boto has a pet too, you know? His name is Robarks. He loves to be petted."
        boto_animation = "dog"
    if any((word in money_words for word in translated_blob_array)):
        boto_response = "Haha, you wanna talk about money? My robo-helmet is worth more than your house young-blood."
        boto_animation = "money"
    return json.dumps({"animation": boto_animation, "msg": boto_response})


def question_response(item):
    print (item)
    if item == "army":
        boto_response = "Of course. I was a fighter pilot for 15 years!"
        boto_animation = "takeoff"
    if item == "can":
        boto_response = "Yep, can do!"
        boto_animation = "ok"
    if item == "aliyah":
        boto_response = "Not yet. They told me they would schedule my interview soon!"
        boto_animation = "waiting"
    print(boto_response)
    print(boto_animation)
    return boto_response, boto_animation


def language_check(string):
    boto_response = string
    botText = TextBlob(boto_response)
    if botText.detect_language() != 'en':
        translated_response = botText.translate(to='en')
        boto_response = str(translated_response)
        return boto_response
    return boto_response


# def print_some_times():
#     print('running')
#     s.enter(5, 1, reminder, ())
#     s.run()
#
# @route("/chat", method='POST')
# def reminder():
#     print("go")
#     return json.dumps({"animation": "bored", "msg": "C'mon, I'm getting bored. Say something!"})

# print_some_times()


@route('https://geek-jokes.sameerkumar.website/api', method='GET')
def joke_generator():
    random_joke = requests.get('https://geek-jokes.sameerkumar.website/api')
    print(random_joke.text)
    return random_joke.text

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
