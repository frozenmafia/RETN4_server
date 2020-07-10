from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
import uuid
from otp import OTP_MANAGER
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adata.sqlite3'

CORS(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer,unique=False,nullable=False)
    country_code = db.Column(db.Integer,unique=False,nullable=False)
    password = db.Column(db.String(120),unique=False,nullable=True)


    def __repr__(self):
        return '<User %r>' % self.username

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.Integer,unique=False,nullable=False)
    country_code = db.Column(db.Integer,unique=False,nullable=False)

    def __repr__(self):
        return '<OTP>'


@app.route('/generate-otp/',methods=['POST'])
def generate_OTP():
    
    phone_text = convert_bytes_to_string(request.data)
    phone_text = phone_text.replace("\"","")
    print(phone_text)
    phone_json = convert_phone_string_to_phone_json(phone_text)
    # print(phone_json)

    country_code = phone_json['country_code']
    phone_number = phone_json['phone_number']
    if existence_of_user(country_code,phone_number):
        return jsonify({
            'country_code':country_code,
            'phone_number':phone_number,
            'verified':None,
            'user_existence':True
            })


    otp_generated= OTP_MANAGER().get_otp()
    print("=======>>>>>",otp_generated)
    otp_info = OTP(otp=otp_generated,phone=phone_json['phone_number'],country_code = phone_json['country_code'])
    db.session.add(otp_info)
    db.session.commit()
    print('otp----------------added',convert_bytes_to_string(request.data))
    return jsonify({
            'country_code':country_code,
            'phone_number':phone_number,
            'verified':None,
            'user_existence':False
            })

@app.route('/verify-otp/',methods=['POST'])
def verify_OTP():
    otp_info_bytes = request.data
    otp_info_json = convert_bytes_to_json(otp_info_bytes)
    phone_json = convert_phone_string_to_phone_json(otp_info_json['phone'])
    
    verified = verify_otp(otp_info_json['otp'],phone_json['country_code'],phone_json['phone_number'],otp_info_json['password'])
    return jsonify(verified)
    return jsonify("lol")

@app.route('/register-user/',methods=['POST'])
def register_user():
    user_info = convert_bytes_to_json(request.data)


@app.route('/login/',methods=['POST'])
def login_user():
    print(request.data)
    login_info = convert_bytes_to_json(request.data)
    phone_json = phone_json = convert_phone_string_to_phone_json(login_info['phone'])
    if existence_of_user(phone_number=phone_json['phone_number'],country_code=phone_json['country_code']):
        login_object = User.query.filter_by(country_code=phone_json['country_code'],phone=phone_json['phone_number'],password=login_info['password']).first()
        if login_object == None:
            return jsonify({
                "logined":False,
                "user_registered":True
            })
        else:
            return jsonify({
                "logined":True,
                "user_registered":True
            })
    else:
        return jsonify({
                "logined":None,
                "user_registered":False
        })


    print(phone_json,login_info)
    return jsonify({"lol":"shivank"})


def convert_bytes_to_json(byte_data):
    return json.loads(byte_data.decode('utf-8'))

def convert_bytes_to_string(byte_data):
    return byte_data.decode('utf-8')

def get_unique_id():
    return str(uuid.uuid4())

def convert_phone_string_to_phone_json(phone_text):
    x = phone_text.split(None,1)
    print(x)
    print(x[0])
    print(x[1])
    return {
        'country_code':int(x[0]),
        'phone_number':int(x[1].replace(" ",""))
    }

def verify_otp(otp,country_code,phone_number,password):
        otp_object = OTP.query.filter_by(otp=otp,country_code=country_code,phone=phone_number).first()
        print(otp_object)
        if otp_object == None:
            print('otp_incorrect')
            return {
                'country_code':country_code,
                'phone_number':phone_number,
                'verified':False,
                'user_existence':False
            }
        else:
            print(otp_object.phone)
            print('correct')
            user_info = User(phone = phone_number,country_code=country_code,password=password)
            db.session.add(user_info)
            db.session.commit()
            
            return {
                'country_code':otp_object.country_code,
                'phone_number':otp_object.phone,
                'verified':True,
                'user_existence':False
            }

        # otp_generated = otp_object.otp
        # otp_entered_by_user = otp_info['otp']



        # if otp_generated == otp_entered_by_user:
        #     db.session.delete(otp)
        #     db.session.commit()
        #     return {
        #         "otp":"expired",
        #         "count":None,
        #         "verified":True
        #     }
        # else:
            
        #     otp.count = otp.count+1
        #     db.session.commit()
        #     if otp.count>3:
        #         db.session.delete(otp)
        #         db.session.commit()
        #         return {
        #             "otp":"expired",
        #             "count":None,
        #             "verified":False
        #         }
        #     return {
        #         "otp":"not expired",
        #         "count":otp.count,
        #         "verified":False
        #     }

def existence_of_user(country_code,phone_number):

    otp_object = User.query.filter_by(country_code=country_code,phone=phone_number).first()
    if otp_object == None:
        return False
            
    else:
        return True
    
        

    
if __name__=="__main__":
    db.create_all()
    app.run(host='0.0.0.0',debug=True)
