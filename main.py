from kafkaFunctions.producer import send_message
import pandas as pd
import numpy as np
import json

# Load the dataset
df = pd.read_csv('dataset.csv', sep=';')
pd.set_option('display.max_columns', None)

# Send each row of the dataset as a message to the Kafka topic
for line in df.iterrows():

    center = {
        "year": line[1]['annee'],
        "location": "center",
        "day": line[1]['lden_exposition_vr_pariscentre'],
        "night": line[1]['ln_exposition_vr_pariscentre']
    }

    north = {
        "year": line[1]['annee'],
        "location": "north",
        "day": np.mean([
            line[1]['lden_exposition_vr_9eme'],
            line[1]['lden_exposition_vr_10eme'],
            line[1]['lden_exposition_vr_17eme'],
            line[1]['lden_exposition_vr_18eme'],
            line[1]['lden_exposition_vr_19eme'],
        ]),
        "night": np.mean([
            line[1]['ln_exposition_vr_9eme'],
            line[1]['ln_exposition_vr_10eme'],
            line[1]['ln_exposition_vr_17eme'],
            line[1]['ln_exposition_vr_18eme'],
            line[1]['ln_exposition_vr_19eme'],
        ])
    }

    east = {
        "year": line[1]['annee'],
        "location": "east",
        "day": np.mean([
            line[1]['lden_exposition_vr_11eme'],
            line[1]['lden_exposition_vr_12eme'],
            line[1]['lden_exposition_vr_20eme'],
        ]),
        "night": np.mean([
            line[1]['ln_exposition_vr_11eme'],
            line[1]['ln_exposition_vr_12eme'],
            line[1]['ln_exposition_vr_20eme'],
        ])
    }

    south = {
        "year": line[1]['annee'],
        "location": "south",
        "day": np.mean([
            line[1]['lden_exposition_vr_5eme'],
            line[1]['lden_exposition_vr_6eme'],
            line[1]['lden_exposition_vr_13eme'],
            line[1]['lden_exposition_vr_14eme'],
        ]),
        "night": np.mean([
            line[1]['ln_exposition_vr_5eme'],
            line[1]['ln_exposition_vr_6eme'],
            line[1]['ln_exposition_vr_13eme'],
            line[1]['ln_exposition_vr_14eme'],
        ])
    }

    west = {
        "year": line[1]['annee'],
        "location": "west",
        "day": np.mean([
            line[1]['lden_exposition_vr_7eme'],
            line[1]['lden_exposition_vr_8eme'],
            line[1]['lden_exposition_vr_15eme'],
            line[1]['lden_exposition_vr_16eme'],
        ]),
        "night": np.mean([
            line[1]['ln_exposition_vr_7eme'],
            line[1]['ln_exposition_vr_8eme'],
            line[1]['ln_exposition_vr_15eme'],
            line[1]['ln_exposition_vr_16eme'],
        ])
    }

    # Send the messages to the Kafka topic
    send_message(topic='center', message=json.dumps(center))
    send_message(topic='north', message=json.dumps(north))
    send_message(topic='east', message=json.dumps(east))
    send_message(topic='south', message=json.dumps(south))
    send_message(topic='west', message=json.dumps(west))