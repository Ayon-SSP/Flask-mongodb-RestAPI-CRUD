from flask import Flask, jsonify, request, redirect, url_for
from flask_pymongo import PyMongo

app =  Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users-db'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def retrieveAll():
    holder = []
    currentCollection = mongo.db.users
    for user in currentCollection.find():
        holder.append({'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']})
        # holder.append({'1':'1'})
        # print(user)
    return jsonify(holder)


@app.route('/<id>', methods=['GET'])
def retrieveFromId(id):
    currentCollection = mongo.db.users
    data = currentCollection.find_one({"id": id})
    if data:
        return jsonify({'id': data['id'], 'name': data['name'], 'email': data['email'], 'password': data['password']})
    else:
        return jsonify({'message': 'User not found'})


@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.users
    id = request.json['id']
    name = request.json['name']
    mail = request.json['email']
    password = request.json['password']

    if request.method == 'POST':
        currentCollection.insert_one({'id': id, 'name': name, 'email': mail, 'password': password})
        return jsonify({'message': 'User created successfully', 'id': id, 'name': name, 'email': mail, 'password': password})
    else:
        return jsonify({'message': 'Error'})


@app.route('/deleteData/<id>', methods = ['DELETE'])
def deleteData(id):
    currentCollection = mongo.db.users
    currentCollection.delete_one({'id' : id})
    # return jsonify({'message': 'User deleted successfully', 'id' : id})
    return redirect(url_for('retrieveAll'))


@app.route('/update/<id>', methods = ['PUT'])
def updateData(id):
    currentCollection = mongo.db.users
    if request.json['id']:
        updatedId = request.json['id']
        currentCollection.update_one({'id': id}, {"$set": {'id': updatedId}})
    if request.json['name']:
        updatedName = request.json['name']
        currentCollection.update_one({'id': id}, {"$set": {'name': updatedName}})
    if request.json['email']:
        updatedEmail = request.json['email']
        currentCollection.update_one({'id': id}, {"$set": {'email': updatedEmail}})
    if request.json['password']:
        updatedPassword = request.json['password']
        updatedPasswordCheck = request.json['passwordCheck']
        if updatedPassword == updatedPasswordCheck:
            currentCollection.update_one({'id': id}, {"$set": {'password': updatedPassword}})
        else:
            return jsonify({'message': 'Passwords do not match'})
    return redirect(url_for('retrieveAll'))



if __name__ == '__main__':
    app.run(debug=True)