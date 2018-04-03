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
import logging, ssl
import numpy as np
from flask import Flask, jsonify, request



# function to build the response from this API with ChatFuel widgets

def build_resp(recallAPI_resp):
    
   
    recalls = recallAPI_resp["Results"]

    resp_txt = "{\"messages\": [" 
    
    resp_txt = resp_txt + "{ \"text\": We found total "+ len(recalls).toString() + " recalls for your vehicle. Please contact your deals or service agent for more details.}"
    
       
    for recall in recalls:
        gallery = gallery + "{ \"title\": \""+ recall['Component'] +"\","
        gallery = gallery + "\"image_url\": \"\","
        gallery = gallery + "\"subtitle\": \""+ recall['Conequence'] + "\","
        gallery = gallery + "\"buttons\": \"[ { \"type\": \"web_url\", \"url\": \"https://www.nhtsa.gov/vehicle/"+ recall['ModelYear'] + "/"+ recall['Make'] + "/"+ recall['Model'] +"\", \"title\": \"View Recalls\" } ]"
        gallery = gallery + "}"
    
    
    resp_txt = resp_txt + "{" +  "\"attachment\": {" + "\"type\": \"template\"," + "\"payload\": {" + "\"template_type\": \"list\"," + "\"top_element_style\": \"large\"," + "\"elements\": [" + gallery + " ] } } } ]}"
    
    return resp_txt

##### END OF FUNCTION - build_resp

req = { 'vehYear': '2012', 
        'vehMake': 'honda',
        'vehModel': 'civic'}

recall_req = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/' + req['vehYear'] +'/'+ req['vehMake'] +'/' + req['vehModel'] +'?format=json'
        
        ### call the recall API from NHTSA
   
import requests
       
recall_resp = requests.get(recall_req)
        
#resp = build_resp(recall_resp.json())
stat_code = 100
reason = 'Successful'


recallAPI_resp = recall_resp.json()

############ function call made inline###########
recalls = recallAPI_resp["Results"]


# initialize gallrey string and a string
gallery_roll = []
gallery = dict.fromkeys(['title','image_url', 'suntitle','buttons'])
i=0
for recall in recalls:
    '''    
    if i > 0 : gallery = gallery + ","  # add a comma between gallery items
    
    gallery = gallery + "\n{ \"title\": \""+ recall['Component'] +"\","
    gallery = gallery + "\"image_url\": \"\","
    gallery = gallery + "\"subtitle\": \""+ recall['Conequence'] + "\","
    gallery = gallery + "\"buttons\": [ { \"type\": \"web_url\", \"url\": \"https://www.nhtsa.gov/vehicle/"+ recall['ModelYear'] + "/"+ recall['Make'] + "/"+ recall['Model'] +"\", \"title\": \"View Recalls\" } ]"
    gallery = gallery + "}"
    i=1 # switch for adding the comma
    '''
    gallery = {
                "title" : recall['Component'], 
                "image_url": "",
                "subtitle": recall['Conequence'],
                "buttons":[
                            {
                                "type":"web_url",
                                "url" : "https://www.nhtsa.gov/vehicle/"+ recall['ModelYear'] + "/"+ recall['Make'] + "/"+ recall['Model'] +"\"", 
                                "title":"View Recalls"                                    
                            }
                        ]
            
            }
    
    gallery_roll.append(gallery)
    
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


   
resp_txt = resp_txt + "\n {" +  "\"attachment\": {" + "\"type\": \"template\"," + "\"payload\": {" + "\"template_type\": \"list\"," + "\"top_element_style\": \"compact\"," + "\"elements\": [" + gallery + " ] } } } ]}"

