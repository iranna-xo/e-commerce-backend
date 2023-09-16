from flask import Flask,request,make_response
import string
import random
import smtplib, ssl
import copy
app = Flask(__name__)

import random
import string


users = [

]


#generate a array with name product which has the following
#1. product id which is number 
#2. product description which tells about the product
#3. product amount which is number
#4. product imageUrl which is string


products = [
  {
    "productId": 1,
    "name": "Product 1",
    "description": "Product 1 description",
    "amount": 99,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 2,
    "name": "Product 2", 
    "description": "Product 2 description",
    "amount": 199,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 3,
    "name": "Product 3",
    "description": "Product 3 description",
    "amount": 299,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 4,
    "name": "Product 4",
    "description": "Product 4 description",
    "amount": 399,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 5,
    "name": "Product 5",
    "description": "Product 5 description",
    "amount": 499,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 6, 
    "name": "Product 6",
    "description": "Product 6 description",
    "amount": 599,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 7,
    "name": "Product 7",
    "description": "Product 7 description",
    "amount": 699,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 8,
    "name": "Product 8",
    "description": "Product 8 description",
    "amount": 799,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 9,
    "name": "Product 9",
    "description": "Product 9 description",
    "amount": 899,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  },
  {
    "productId": 10,
    "name": "Product 10",
    "description": "Product 10 description",
    "amount": 999,
    "imageUrl": "https://source.unsplash.com/random/200x200"
  }
]


def randomKeyGenerator():
  # generating random strings
  N = 7
  res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=N))
  return res
 

def randomOtp():
  min = 100000
  max = 999999;
  return random.randint(min,max)


def addUser(newUser):
  
  for user in users:
    if user['email'] == newUser['email']:
      return {"flag" : False}
  
  #generate a random key
  users.append({
    "name":newUser['name'],
    "email":newUser['email'],
    "password":newUser['password'],
    "sessionKey": randomKeyGenerator(),
  })
  objUser = copy.deepcopy(users[len(users) - 1])
  #remove password from the user
  del objUser['password']
  print(objUser)
  return {"flag": True, "user":objUser}

def validateUser(checkUser):
  for user in users:
    if checkUser['email'] == user['email'] and checkUser['password'] == user['password']:
      user['sessionKey'] = ""
      sendOtp(user)
      objUser = copy.deepcopy(user)
      del objUser['password']
      print(user)
      return {"flag":True,"user":objUser}
  return {"flag":False}

def sendOtp(user):
  user['otp'] = 000000
  #this function needs to be implemented



def validateOtp(checkUser):
  for user in users:
    if user['email'] == checkUser['email']:
      print(user)
      if user['otp'] == int(checkUser['otp']):
        user['sessionKey']=randomKeyGenerator()
        return user['sessionKey']
    else:
      return -1



    

@app.route('/sign-up', methods=['POST'])
def signUp():
  json = request.json
  user = addUser(json)
  response =''
  if user['flag']:
    #make copy of user['user'] and remove the password

    response = make_response(user['user'],201)
    # return {'status':'sucsess','body':{'user':user['user']}}
  else:
    response = make_response({"errorMessage":'Email already exists'},409
    )
    # return {'status':'failed','errorMessage':"Email already exists" , "status_code":404}
  return response

@app.route('/login',methods=['POST'])
def login():
  req = request.json
  flag = validateUser(req)
  if(flag['flag']):
    return make_response(flag['user'],200)
  else:
    return make_response({"errorMessage":'Invalid Credentials'},401)
  

@app.route('/verify-otp',methods=['POST'])
def verifyOtp():
  req = request.json
  print(req)
  sessionKey =  validateOtp(req)
  if sessionKey != -1:
    return make_response({"sessionKey":sessionKey},200)
  else:
    return make_response({"errorMessage":'Otp is invalid'},401)
  
@app.route('/products',methods=['GET'])
def getProducts():
  return make_response(products,200)


def validateChangePass(changePassUser):
  for user in users:
    if changePassUser['email'] == user['email']:
      if changePassUser['oldPassword'] == user['password']:
        user['password'] = changePassUser['newPassword']
        return True
      else:
        return False


@app.route('/change-password',methods=['POST'])
def changePassword():
  req= request.json
  print(req)
  flag = validateChangePass(req)
  if flag:
    return make_response({"status":"success"},200)
  else:
    return make_response({"errorMessage":"Invalid old password"},401)


if __name__=='__main__':
  app.run(debug=True)