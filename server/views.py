import logging
import config
import json

from bson import json_util, ObjectId
from flask import jsonify, Response, request, abort, make_response

from Offer import Offer

@config.g_app.route("/")
def index():
    return "Artspeaker job offer and portfolio services."


@config.g_app.route("/offer", methods=["POST"])
def createOffer():
    '''
    Create the offer
    '''

    offerId = str(ObjectId())
    userId = request.get_json().get("userId", None)

    if  offerId == None or userId == None:
        logging.error("The offer ID, the user ID or the project title is undefined")
        abort(make_response("The offer ID, the user ID is undefined", 500))

    offer = Offer(offerId, userId)

    # minimal requierements

    projectTitle = request.get_json().get("projectTitle", None)
    fieldActivity = request.get_json().get('fieldActivity', None)
    place = request.get_json().get('place', None)
    enterpriseLogo = request.get_json().get('entrepriseLogo', None)
    networking = request.get_json().get('networking', None)
    projectDate = request.get_json().get('projectDate', None)
    contact = request.get_json().get('contact', None)

    # Data

    if projectTitle is not None :
        offer.projectTitle = projectTitle
    if fieldActivity is not None :
        offer.fieldActivity = fieldActivity
    if place is not None :
        offer.place = place
    if enterpriseLogo is not None :
        offer.enterpriseLogo = enterpriseLogo
    if networking is not None :
        offer.networking = networking
    if projectDate is not None :
        offer.projectDate['begin'] = projectDate['begin']
        offer.projectDate['end'] = projectDate['end']
    if contact is not None :
        offer.contact['name'] = contact['name']
        offer.contact['phone'] = contact['phone']
        offer.contact['mail'] = contact['mail']

    config.offerTable.insert(offer.__dict__)
    requestResult = config.offerTable.find_one({"offerId": offerId})
    logging.error(requestResult)
    return mongodoc_jsonify(requestResult)



'''
    worktype = request.get_json().get('worktype', None)
    offerDate = request.get_json().get('offerDate', None)

    
    remuneration = request.get_json().get('remuneration', None)

    if remuneration is not None :
        offer.remuneration = remuneration
    if wantedProfiles is not None :
        offer.wantedProfiles = wantedProfiles
    if worktype is not None :
        offer.worktype = worktype
    if offerDate is not None :
        offer.offerDate['begin'] = offerDate['begin']
        offer.offerDate['end'] = offerDate['end']
'''

@config.g_app.route("/offer/<offerId>/step/<step>", methods=["POST"])
def offerStepTwo(offerId, step):
    logging.error("yay")
    offerTitle = request.get_json().get('offerTitle', None)
    offerDate = request.get_json().get('offerDate', None)
    wantedProfiles = request.get_json().get('wantedProfiles', None)
    text = request.get_json().get('text', None)
    tags = request.get_json().get('tags', None)

    config.offerTable.update_one(
        {"offerId": offerId},
        {"$set":{   "offerTitle":offerTitle,
                    "offerDate" : offerDate,
                    "wantedProfiles" : wantedProfiles,
                    "text": text, 
                    "tags":tags,
                    "offerDate['begin']" : offerDate['begin'],
                    "offerDate['end']" : offerDate['end'],
                    }}
    )

    updateResult = config.offerTable.find_one({"offerId": offerId})
    logging.error(updateResult)
    return mongodoc_jsonify(updateResult)

@config.g_app.route("/offer", methods=["GET"])
def getOffers():
    offers = config.offerTable.find()
    return mongodoc_jsonify({"offers":[ result for result in offers ]})

@config.g_app.route("/user/<userId>/offer", methods=["GET"])
def getOffersFromUser(userId):
    offers = config.offerTable.find({"userId": userId})
    return mongodoc_jsonify({"offers":[ result for result in offers ]})

@config.g_app.route("/offer/<offerId>", methods=["DELETE"])
def deleteOffers(offerId):
    deletedOffer = config.offerTable.remove({"offerId": offerId})
    return mongodoc_jsonify(deletedOffer)

@config.g_app.route("/offer/<offerId>", methods=["GET"])
def getOfferById(offerId):
    offer = config.offerTable.find_one({"offerId": offerId})
    return mongodoc_jsonify(offer)

def mongodoc_jsonify(*args, **kwargs):
    return Response(json.dumps(args[0], default=json_util.default), mimetype='application/json')

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.serverPort,debug=True)