#!/usr/bin/env python

import Image
from glob import glob

import json
import oauth2 as oauth
import os
import urllib

import pystache

# grab json set of profile data fron linkedin API
def get_lnkdn_json():

    # load api creds from json
    api_auth_conf = open('api-creds.json')
    api_auth_data = json.load(api_auth_conf)
    api_auth_conf.close()

    consumer_key = api_auth_data['consumer_key']
    consumer_secret = api_auth_data['consumer_secret']
    user_token = api_auth_data['user_token']
    user_secret = api_auth_data['user_secret']

    # authenticate to oauth
    consumer = oauth.Consumer(consumer_key, consumer_secret)
 
    access_token = oauth.Token(key=user_token, secret=user_secret)
 
    # instantiate oauth client object
    client = oauth.Client(consumer, access_token)

    # get a json set of all connections
    resp,content = client.request("http://api.linkedin.com/v1/people/~:(first-name,last-name,headline,summary,picture-url,positions,formatted-phonetic-name,email-address,phone-numbers,main-address,current-status,specialties,honors,interests,associations,languages,)?format=json")
    content = content.replace('\\\\', '{\\\\textbackslash}')
    content = content.replace('\\n', '\\\\\\\\')
    profile_txt_json = json.loads(content)

    profile_data = {'profile' : profile_txt_json}

    # print out all connections work histories from public profile
    for connection in profile_txt_json['positions']['values']:
        try: 
            connid = connection['company']['id']
            url = "http://api.linkedin.com/v1/companies/%s:(id,name,ticker,description,square-logo-url,logo-url)?format=json" % connid
            resp,content = client.request(url)
            company_json = json.loads(content)
            profile_data[connid] = company_json 
        except:
            print "no company id found!"

    # get json of url to profile picture ( original size )
    resp,content = client.request("http://api.linkedin.com/v1/people/~/picture-urls::(original)?format=json")
    profile_img_json = json.loads(content)
    # join json sets
    profile_data['photo'] = profile_img_json
    profile_json = json.dumps(profile_data, sort_keys=True, indent=4)
 
    #print profile_json
    # return full profile json set
    return profile_data

def render_lnkdn(profile):

    # instantiate pystache renderer
    renderer = pystache.Renderer()

    # apply profile json set to resume template.
    resume = renderer.render_path('header.mustache', profile)
    resume += renderer.render_path('objective.mustache', profile)
 
    resume += renderer.render_path('experience.mustache', profile)
    for connection in profile['profile']['positions']['values']:
        connid = connection['company']['id']
        resume += renderer.render_path('position.mustache', connection)

    resume += renderer.render_path('honorsawards.mustache', profile)
    resume += renderer.render_path('footer.mustache', profile)

    return resume

profile = get_lnkdn_json()
photourl = profile['photo']['values'][0]
headshot = open('headshot.jpg','wb')
headshot.write(urllib.urlopen(photourl).read())
headshot.close()
u = 'headshot.jpg'
out = u.replace('jpg','png')
img=Image.open(u)
img.save(out)
resume = render_lnkdn(profile)

print resume
