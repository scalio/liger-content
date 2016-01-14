#!/usr/bin/env python

import sys
import os
import yaml
import json

# TODO mkdir the dirs you need as they wont exist on clean checkout

def parse_file(original_json_file_path, translated_strings_file_path, out_file_path):
    in_stream = open(original_json_file_path, 'r')
    doc = json.load(in_stream)

    strings_stream = open(translated_strings_file_path, 'r')
    strings = json.load(strings_stream)


    for k,v in strings.iteritems():
        splits = k.split('::')
        path_id = splits[0]

        # get the doc level properites (of course this will badly break if the doc has array or dict props and is hence more than 2 deep
        if len(splits) == 2:
            key_id = splits[1]
            doc[key_id] = v # in this case its a doc level prop, not a path_id
            continue

        # check we are in teh right file by checking the pathid
        if not doc['id'] == path_id:
            print "!! key in translation file '%s' doesn't match this path's id: '%s'" % (splits[0], doc['id'])
            exit(-1)

        card_id = splits[1]
        prop_key = splits[2]


        for card in doc['cards']:
            if card['id'] == card_id:
                if len(splits) == 3:
                    key_splits = prop_key.split('[')
                    if len(key_splits) == 1:
                        key = key_splits[0]
                        # of form  "event_discussion_audio_question1::evaluation_card_0::text"
                        print "at %s, replacing '%s' with '%s'" % (k, card[key], v)
                        card[key] = v
                    elif len(key_splits) == 2:
                        # of form "event_discussion_audio_question1::clip_card_5::goals[0]"
                        key = key_splits[0]
                        array_index = int(key_splits[1].split(']')[0]) # FIXME skip this step by initially splitting on [ | ] in a regex
                        print "at %s, replacing '%s' with '%s'" % (k, card[key][array_index], v)
                        card[key][array_index] = v
                        # index into an array (or dict?)
                elif len(splits) == 4:
                    key_splits = prop_key.split('[')
                    if len(key_splits) == 1:
                        key = key_splits[0]
                        # of form  "event_discussion_audio_question1::evaluation_card_0::text"
                        print "at %s, replacing '%s' with '%s'" % (k, card[key], v)
                        card[key] = v
                    elif len(key_splits) == 2:
                        # of form "default_library::tip_collection::tips[0]::text"
                        key = key_splits[0]
                        array_index = int(key_splits[1].split(']')[0]) # FIXME skip this step by initially splitting on [ | ] in a regex
                        real_prop_key = splits[3]
                        print u"at {0}, replacing '{1}' with '{2}'".format(k, card[key][array_index][real_prop_key], v)
                        card[key][array_index][real_prop_key] = v
                        # index into an array (or dict?)
                else:
                    print "\n\n\ncard\n%s\n\n\n" % card
                    print "!! deeper nesting we need to handle in %s:\n\n\ncard\n%s\n\n\n" % (original_json_file_path, card)
                    exit(-1)
                    pass # TODO there are some deeper nestings we need to watch out for
                break

    json_string = json.dumps(doc, indent=4)
    out_file = open(out_file_path, 'w')
    out_file.write(json_string)
    out_file.close()


def gen_translations(json_dir, translations_dir):
    for translated_strings_file_name in os.listdir(translations_dir):
        file_name, file_extension = os.path.splitext(translated_strings_file_name)
        print "translations_dir: " + translations_dir
        print "translated_strings_file_name: " + translated_strings_file_name + " file_name: " + file_name
        (json_file_name, lang) = file_name.split('-')
        translated_json_file_name = "%s-%s.json" % (json_file_name, lang)
        out_file_path = "%s/%s" % (json_dir, translated_json_file_name)
        original_json_file_path = "%s/%s.json" % (json_dir, json_file_name)
        translated_strings_file_path = "%s/%s" % (translations_dir, translated_strings_file_name)

        print "inserting localized strings into %s" % out_file_path

        # strings_file_name = "%s/%s.json" % (translations_dir, file_name)
        parse_file(original_json_file_path, translated_strings_file_path, out_file_path)

"""
print "generating content for lessons"
parent_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/lessons/"
for f in os.listdir(parent_dir):
    json_dir = os.getcwd() + "/assets/org.storymaker.app/lessons/%s" % f
    translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/lessons/%s" % f
    gen_translations(json_dir, translations_dir)
#"""
    
"""
print "generating content for beta pack"
parent_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/beta/"
for f in os.listdir(parent_dir):
    json_dir = os.getcwd() + "/assets/org.storymaker.app/beta/%s" % f
    translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/beta/%s" % f
    gen_translations(json_dir, translations_dir)
#"""
    
"""
print "generating content for mobile_photo_basics pack"
parent_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/mobile_photo_101/"
for f in os.listdir(parent_dir):
    json_dir = os.getcwd() + "/assets/org.storymaker.app/mobile_photo_101/%s" % f
    translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/mobile_photo_101/%s" % f
    gen_translations(json_dir, translations_dir)
#"""

"""
# FIXME make sure there's no translations present or we are going to double translate them, maybe go into a loop
json_dir = os.getcwd() + "/assets/org.storymaker.app/default"
translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/default"
gen_translations(json_dir, translations_dir)

json_dir = os.getcwd() + "/assets/org.storymaker.app/learning_guide/learning_guide_1"
translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/learning_guide/learning_guide_1"
gen_translations(json_dir, translations_dir)

json_dir = os.getcwd() + "/assets/org.storymaker.app/learning_guide/learning_guide_2"
translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/learning_guide/learning_guide_2"
gen_translations(json_dir, translations_dir)

json_dir = os.getcwd() + "/assets/org.storymaker.app/learning_guide/learning_guide_3"
translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/learning_guide/learning_guide_3"
gen_translations(json_dir, translations_dir)
#"""

"""
print "generating content for lessons"
parent_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/lessons/"
for f in os.listdir(parent_dir):
    json_dir = os.getcwd() + "/assets/org.storymaker.app/lessons/%s" % f
    translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/lessons/%s" % f
    gen_translations(json_dir, translations_dir)
#"""

"""
print "generating content for journalism_part_1"
parent_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/journalism_part_1/"
for f in os.listdir(parent_dir):
    json_dir = os.getcwd() + "/assets/org.storymaker.app/journalism_part_1/%s" % f
    translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/journalism_part_1/%s" % f
    gen_translations(json_dir, translations_dir)
#"""

def generate_translated_assets(name):
    print "generating content for {0} pack".format(name)
    parent_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/{0}/".format(name)
    for f in os.listdir(parent_dir):
        json_dir = os.getcwd() + "/assets/org.storymaker.app/{0}/{1}".format(name, f)
        translations_dir = os.getcwd() + "/intermediates/translated_strings/org.storymaker.app/{0}/{1}".format(name, f)
        gen_translations(json_dir, translations_dir)

generate_translated_assets("mobile_photo_basics")
