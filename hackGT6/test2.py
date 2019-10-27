from firebase import firebase
import json
firebase = firebase.FirebaseApplication('https://xuzheyuan1014.firebaseio.com/', None)
data = 'temp1.jpg'
result = firebase.get('/xuzheyuan1014/processed_images', '')
print(result)
