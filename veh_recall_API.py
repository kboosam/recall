# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 14:26:55 2018

@author: kboosam
"""
# data preprocessing example
# Importing libraries

'''
@@ API TO CAPTURE THE RECALL DETAILS OF A VEHICLE BASED ON THE YEAR, MAKE AND MODEL

'''
# Importing libraries

import pandas as pd
from flask import Flask, jsonify, request
import logging
from flask_cors import CORS
import numpy as np
from raven.contrib.flask import Sentry ## Sentry logging 
import requests

# function to build the response from this API with ChatFuel widgets

def build_resp(recallAPI_resp):
    
    try:
        recalls = recallAPI_resp["Results"]  ## Get all results ##
              
        if recallAPI_resp["Count"] > 0:
            # post a simple text about the number of recalls identified - UNUSED BELOW
            #resp_txt = resp_txt + "{ \"text\": \"We found total "+ str(recallAPI_resp["Count"]) + " recalls for your vehicle. Please contact your deals or service agent for more details.\"},"
            
            
            # initialize gallrey list and dictionary for each gallery item.
            gallery_roll = []
            gallery = dict.fromkeys(['title','image_url', 'suntitle','buttons'])
            for recall in recalls:
                 
                 gallery = {
                                "title" : recall['Component'], 
                                "image_url": "",
                                "subtitle": recall['Conequence'],
                                "buttons":[
                                            {
                                                "type":"web_url",
                                                "url" : "https://www.nhtsa.gov/vehicle/"+ recall['ModelYear'] + "/"+ recall['Make'] + "/"+ recall['Model'] , 
                                                "title":"View Recalls"                                    
                                            }
                                        ]
                            }
                    
                 gallery_roll.append(gallery)
            # build the Full response dictionary        
            resp_dict = {
                        "messages": [
                                      { "text": "We found total " + str(recallAPI_resp["Count"]) + " recalls for your vehicle. Please contact your dealer or service agent for more details." 
                                       },
                                      { "attachment" : {
                                              
                                              "type": "template",
                                              "payload": {
                                                      "template_type":"list",
                                                      "top_element_style": "compact",
                                                      "elements": gallery_roll
                                                      
                                                      }
                                              }
                                     }
                                    ]
                        }

                
        else:
             #resp_txt = resp_txt + "{ \"text\": \"There are no recalls reported for your vehicle at this point.Please contact your dealer or service agent for any further questions.\"} ] }"
            resp_dict = {
                        "messages": [
                                      { "text": "Happy to inform you that, there are no active recalls reported for your vehicle at this time."
                                       
                                       },
                                       { 
                                       "text": "However recommend to check with your dealer or service agent regularly." 
                                       }
                                      
                                    ]
                        }

    except Exception as e:
        print(e)
        sentry.captureMessage(message=e, level=logging.FATAL)
        resp_dict = {
                 "messages": [
                   {"text": "An error occured while fetching the recall details for your vehicle - 102."},
                  ]
                }
        
    return resp_dict;

##### END OF FUNCTION - build_resp
###################################################################

app = Flask(__name__)
#set sentry for logging the messages
sentry = Sentry(app, dsn='https://e8ddaf32cc924aa295b846f4947a9332:5e52d48fe13a4d2c82babe6833c5f871@sentry.io/273115')
CORS(app) ## cross origin resource whitelisting..


@app.route('/predict/recall_api', methods=['POST','GET'])
def get_recalls():
    
    """API Call
    Pandas dataframe (sent as a payload) from API Call
    """
    print("\n\n\n Started processing the request..\n\n\n")
   
        #req_json = str(request.get_json())
        #req = pd.read_json("test_json.txt", typ='series')
##################

#   REQUEST STRCUTRE
#
#{   'VehVin': <>,
#    'vehyear':<>,
#    'vehmake':<>,
#    'vehmodel':<>
#  }

#################       
    try: 
        req = request.json
        print("####This is the request:", req, '\n\n')
        
        sentry.captureMessage(message='Started processing request- {}'.format(req['VehVin']), level=logging.INFO)
        
    except Exception as e:
        print(e)
        sentry.captureMessage(message=e, level=logging.FATAL)
        
    if any(req.values()): #any values in the request?  
        recall_req = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/' + req['vehyear'] +'/'+ req['vehmake'] +'/' + req['vehmodel'] +'?format=json'
        
    else:
        sentry.captureMessage(message='Empty Request!!!', level=logging.CRITICAL)
        resp = {
                 "messages": [
                   {"text": "An error occured while fetching the recall details for your vehicle - 102."},
                  ]
                }
    
    ### call the recall API from NHTSA
    
    try:
        recall_resp = requests.get(recall_req)
        
        print(recall_resp)
        # call the function to build the response text
        resp = build_resp(recall_resp.json())
        sentry.captureMessage(message='completed processing the recall request - VIN: {}'.format(req['VehVin']), level=logging.INFO)
    
    except Exception as e:
        
        
        print(e)
        sentry.captureMessage(message=e, level=logging.FATAL) #printing all exceptions to the log
        resp = {
                 "messages": [
                   {"text": "An error occured while fetching the recall details for your vehicle - 103."},
                  ]
                }
    
    
    return jsonify(resp)


if __name__ == '__main__':
   ## DISABLE CERITIFACATE VERIFICATION FOR SSL.. some issue in Capgemini network..
   '''
   try:
        _create_unverified_https_context = ssl._create_unverified_context
   except AttributeError:
         # Legacy Python that doesn't verify HTTPS certificates by default
        pass
   else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
   '''    
   sentry.captureMessage('Started runnning API for Recalls !!')
   app.run(debug=True,port=5100) #turnoff debug for production deployment

