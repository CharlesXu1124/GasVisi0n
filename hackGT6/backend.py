from google.cloud import vision
import cv2
import json
import spacy
import warnings
import string
from PIL import Image, ImageDraw
import urllib.request
import re
import io
from difflib import SequenceMatcher
import cv2
import random
from firebase import firebase

# set up firebase
firebase = firebase.FirebaseApplication('https://xuzheyuan1014.firebaseio.com/', None)


warnings.filterwarnings('ignore')


dictionary = ["regular", "plus", "supreme", "premium", "silver", "ultimate", "reg", "spec", "sup", "super", "special", "diesel", "V-Power", "unleaded", "unlead"]
dictionary = [d.title() for d in dictionary]


def char_match(s1, s2):
    ok = False
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            if ok:
                return False
            else:
                ok = True

    return ok

def compute_correlation(text, label_list):
    while text and text[-1] in string.punctuation:
        text = text[0:-1]
    for t in dictionary:
        '''
        words = text + " " + t
        tokens = nlp(words)
        # print(tokens)
        token1, token2 = tokens[0], tokens[1]
        similarity = token1.similarity(token2)
        # print(token1, token2, similarity)
        
        seqMatch = SequenceMatcher(None, t, text)
        match = seqMatch.find_longest_match(0, len(t), 0, len(text))
        t_set = set(t)
        text_set = set(text)
        intersect = t_set.difference(text_set)
        print("t: ", t, " text: ", text, " diff: ", char_match(t, text))
        #(len(intersect)<= 1 and match.size >= len(text) - 3)
        '''
        text = text.lower().title()
        if char_match(t, text) or text == t:
            label_list.append(t)
            return True
    # a similar word hasn't been found
    return False

def check_is_float(text):
    
    try:
        float(text)
        return True
    except ValueError:
        return False


# load the english word correlation file (medium)
#nlp = spacy.load('en_core_web_md') 

# image_uri = 'https://www.watchfiresigns.com/assets/uploads/remote/https_www.watchfiresigns.com/assets/uploads/images/Shop_N_Save_Market_Atlantic_Sign_Media_W_8mm_108x324_Price_Watcher_12inch_Red_Red_Green_Mooresville_NC_145658_145689_35x93_v2_1200x900.jpg'

# with urllib.request.urlopen(image_uri) as url:
#    with open('temp.jpg', 'wb') as f:
#        f.write(url.read())

def optimize_image(iteration):
    img = cv2.imread('temp.jpg', cv2.IMREAD_UNCHANGED)
    
    # scale_percent = random.uniform(30, 95) # percent of original size
    scale_percent = 85
    # print('scaling : ', scale_percent)
    

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite(f'temp_{iteration}.jpg', resized)


def main(iteration):
    label_list = []
    price_list = []

    optimize_image(iteration)

    img = Image.open(f'temp_{iteration}.jpg')

    with io.open(f'temp_{iteration}.jpg', 'rb') as image_file:
            content = image_file.read()

    image = vision.types.Image(content=content)


    draw = ImageDraw.Draw(img)

    client = vision.ImageAnnotatorClient()
    # image = vision.types.Image()
    # image.source.image_uri = image_uri


    response = client.text_detection(image=image)
    flag = 0
    #print(response.text_annotations)


    for text in response.text_annotations:
        # preprocessing text to extract prices
        word = text.description
        f = re.findall(r"[2-5]\.?[0-9]?[0-9]", word)
        # print(f)
        if f and not price_list:
            price_list = f
        elif f:
            vects = text.bounding_poly.vertices
            draw.rectangle([(vects[0].x, vects[0].y), vects[2].x, vects[2].y], width = 2, outline='red', fill=None)
            
        
        # compute the correlation between each word inside each word group
        if compute_correlation(word, label_list) and word.isnumeric() == False:
            
            # vertices = [(v.x, v.y) for v in text.bounding_poly.vertices]
            vects = text.bounding_poly.vertices
            draw.rectangle([(vects[0].x, vects[0].y), vects[2].x, vects[2].y], width = 2, outline='green', fill=None)
            # print(vertices)
            
            draw.polygon(text.bounding_poly.vertices, None, 'red')
            
            
            # print(f'"{text.description}"')
            # print(f'bounds: {",".join(vertices)}')
    print(label_list, price_list)
    img.show()
    return (label_list, price_list)
    

#img.show()
main(1)


