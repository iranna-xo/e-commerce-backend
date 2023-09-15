from flask import Flask,request,make_response
import string
import random
import smtplib, ssl
import copy
app = Flask(__name__)


users = [

]

systemEmail= "irannacy22@gmail.com"
systemPassword = "forvdiuse"
port = 465



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

if __name__=='__main__':
  app.run(debug=True)