#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Matt Joyce's Resume
'''

__author__ = 'Matt Joyce'
__email__ = 'matt@surly.bike'
__copyright__ = 'Copyright 2012, Matt Joyce'


import argparse
import json
import pystache
import sys


def load_json(json_file):
    ''' load specified json file into dictionary '''
    with open('file.json') as data_file:
        data = json.load(data_file)
    return data


def render_latex(profile):
    ''' render a LaTeX format from JSON values '''
    # instantiate pystache renderer
    renderer = pystache.Renderer()

    # apply profile json set to resume template.
    resume = renderer.render_path('header.mustache', profile)
    resume += renderer.render_path('objective.mustache', profile)
    resume += renderer.render_path('experience.mustache', profile)
    for connection in profile['profile']['positions']['values']:
        resume += renderer.render_path('position.mustache', connection)
    resume += renderer.render_path('honorsawards.mustache', profile)
    resume += renderer.render_path('footer.mustache', profile)
    return resume


def main():
    ''' main program loop '''
    # CLI flag parsing
    parser = argparse.ArgumentParser(description='metronome bot')
    # specify config file
    parser.add_argument(
        '-r', '--resume', nargs='?',
        help='specify path to config file',
        default='resume.json'
    )
    # specify output file
    parser.add_argument(
        '-o', '--output', nargs='?',
        help='specify output filename',
        default='resume.tex'
    )
    # parse
    try:
        args = parser.parse_args()
    except Exception as err:
        print('failed to parse arguments: %s' % (err))
        sys.exit(1)
    # generate json blob from file
    profile = load_json(args.resume)
    # generate resume LaTeX from json blob
    resume = render_latex(profile)
    print resume


if __name__ == "__main__":
    main()
