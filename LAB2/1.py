from firebase import firebase
import json as simplejson
firebase = firebase.FirebaseApplication('https://czqa1-de9c1.firebaseio.com',None)
result  = firebase.get('',None)
print result
 
name = {'Edison':888}
#data = simplejson.dumps(name)
  
post = firebase.post('/users',name)
   
print post
