import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

from datetime import datetime
import random
import string
import sys

cred = credentials.Certificate("./serviceAccountKey.json")  # Private credentials of database.
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tfg-smartgaraje.firebaseio.com/',
    'storageBucket': 'tfg-smartgaraje.appspot.com'
})
db = firestore.client()
bucket = storage.bucket()

def randomString(stringLength=19):
    letters = string.ascii_lowercase
    return 'A' + ''.join(random.choice(letters) for i in range(stringLength))

def getMembersOfOrganization(db, orgID):
    membersIDs = []
    membersDocs = db.collection('organizations').document(orgID).collection('members')
    for member in membersDocs.stream():
        membersIDs.append(member.id)
    return membersIDs

def plateOwner(db, plate):
    ownerDoc = db.collection('vehicules').document(plate)
    return ownerDoc.get().to_dict().get('uid')

def addingVehiculeToTimeLine(db, bucket, orgId, img_path):
    public_url = uploadImage(bucket, orgId, img_path)
    db.collection('organizations').document(orgID).collection('timeLine').document(str(randomID)).set({
        'date': datetime.now(),
        'plateURL': public_url,
        'status': 'Enter'
    })

def uploadImage(bucket, orgId, img_path):
    path_on_cloud = 'organizations/' + orgID + '/' + str(randomID) + '.png'
    blob = bucket.blob(path_on_cloud)
    blob.upload_from_filename(img_path)
    blob.make_public()
    return blob.public_url

if __name__ == "__main__":
    randomID = randomString()
    orgID = sys.argv[1]
    plate = sys.argv[2]
    imagePathToUpload = sys.argv[3]
    members = getMembersOfOrganization(db, orgID)
    ownerID = plateOwner(db, plate)
    try:
        members.index(ownerID)
        print('Opening garaje door.')
        addingVehiculeToTimeLine(db, bucket, orgID, imagePathToUpload)
    except:
        print('This license plate doesn\'t belong to this garage.')
