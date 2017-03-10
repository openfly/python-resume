#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Matt Joyce's Resume
'''

__author__ = 'Matt Joyce'
__email__ = 'matt@surly.bike'
__copyright__ = 'Copyright 2012, Matt Joyce'


import json
import pystache

def load_json(json_file):
    ''' load specified json file into dictionary '''
    

def render_latex(profile):
    ''' render a LaTeX format from JSON values '''
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


resume = render_latex(profile)

print resume
