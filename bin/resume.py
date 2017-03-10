#!/usr/bin/env python
# this is bogusnow -*- coding: utf-8 -*-
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
    with open(json_file) as data_file:
        data = json.load(data_file)
    return data


def render_latex(profile, template_path):
    ''' render a LaTeX format from JSON values '''
    # instantiate pystache renderer
    renderer = pystache.Renderer()

    # apply profile json set to resume template.
    resume = renderer.render_path(template_path + 'header.mustache', profile)
    resume += renderer.render_path(template_path + 'objective.mustache', profile)
    resume += renderer.render_path(template_path + 'experience.mustache', profile)
    for role in profile['Experience']:
        resume += renderer.render_path(template_path + 'position.mustache', role)
    resume += renderer.render_path(template_path + 'projects.mustache', profile)
    for project in profile['Projects']:
        resume += renderer.render_path(template_path + 'project.mustache', project)
    resume += renderer.render_path(template_path + 'honorsawards.mustache', profile)
    for honor in profile['Honors & Awards']:
        resume += renderer.render_path(template_path + 'honor.mustache', honor)
    resume += renderer.render_path(template_path + 'footer.mustache', profile)
    return resume


def write_to_file(filename, filedata):
    with open(filename, "w") as text_file:
        text_file.write(filedata.encode('utf-8'))
    return 0


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
    # specify template path
    parser.add_argument(
        '-t', '--template', nargs='?',
        help='specify template path',
        default='../templates/'
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
    resume = render_latex(profile, args.template)
    write_to_file(args.output, resume)


if __name__ == "__main__":
    main()
