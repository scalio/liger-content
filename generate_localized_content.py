#!/usr/bin/env python

import sys
import os
import yaml
import json

languages = [
    #'ar',
    #'fa',
    #FIXME fill in the rest
    'de'
]

# TODO mkdir the dirs you need as they wont exist on clean checkout


def parse_file(original_json_file_path, translated_strings_file_name, out_file_path):
    in_stream = open(original_json_file_path, 'r')
    doc = json.load(in_stream)

    strings_stream = open(translated_strings_file_name, 'r')
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
                        print "at %s, replacing '%s' with '%s'" % (k, card[key][array_index][real_prop_key], v)
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


def gen_translations():
    for translated_strings_file_name in os.listdir(translations_dir):
        file_name, file_extension = os.path.splitext(translated_strings_file_name)
        (json_file_name, lang) = file_name.split('-')
        translated_json_file_name = "%s-%s.json" % (json_file_name, lang)
        out_file_path = "%s/%s" % (json_dir, translated_json_file_name)
        original_json_file_path = "%s/%s.json" % (json_dir, json_file_name)
        translated_strings_file_path = "%s/%s" % (translations_dir, translated_strings_file_name)

        print "inserting localized strings into %s" % out_file_path

        # strings_file_name = "%s/%s.json" % (translations_dir, file_name)
        parse_file(original_json_file_path, translated_strings_file_path, out_file_path)

print "generating content for lessons"
cardcounts = {}
parent_dir = os.getcwd() + "/intermediates/translated_strings/lessons/burundi/"
for f in os.listdir(parent_dir):
    json_dir = os.getcwd() + "/assets/lessons/burundi/%s" % f
    translations_dir = os.getcwd() + "/intermediates/translated_strings/lessons/burundi/%s" % f
    gen_translations()


# FIXME make sure there's no translations present or we are going to double translate them, maybe go into a loop
json_dir = os.getcwd() + "/assets/default"
translations_dir = os.getcwd() + "/intermediates/translated_strings/default"
gen_translations()

json_dir = os.getcwd() + "/assets/default/learning_guide_1"
translations_dir = os.getcwd() + "/intermediates/translated_strings/learning_guide/learning_guide_1"
gen_translations()

json_dir = os.getcwd() + "/assets/default/learning_guide_2"
translations_dir = os.getcwd() + "/intermediates/translated_strings/learning_guide/learning_guide_2"
gen_translations()

json_dir = os.getcwd() + "/assets/default/learning_guide_3"
translations_dir = os.getcwd() + "/intermediates/translated_strings/learning_guide/learning_guide_3"
gen_translations()
