from json import load
with open("stream-api.json","r") as f:
    api = load(f)

def decode_thronebutt_data(entry):
    decoded_entry = {}
    decoded_entry["rank"] = entry["rank"]
    decoded_entry["name"] = entry["name"]
    decoded_entry["character"] = entry["character"]
    decoded_entry["loops"] = entry["loops"]
    decoded_entry["wlevel"] = entry["level"]
    decoded_entry["score"] = entry["score"]
    print(entry["ultra"])
    decoded_entry["ultra"] = api["ultra-mutations"][entry["ultra"]]
    decoded_entry["mutations"] = [api["mutations"][x] for x in entry["mutations"]]
    decoded_entry["weapons"] = [api["weapons"][x] for x in entry["weapons"]]
    decoded_entry["crown"] = api["crowns"][entry["crown"]]
    decoded_entry["lasthit"] = api["enemies"][entry["lasthit"]]
    return decoded_entry

def encode_thronebutt_data(entry):
    encoded_entry = {}
    encoded_entry["rank"] = entry["rank"]
    encoded_entry["name"] = entry["name"]
    encoded_entry["char"] = api["characters"][entry["character"]]
    encoded_entry["loops"] = entry["loops"]
    encoded_entry["level"] = entry["wlevel"]
    encoded_entry["score"] = entry["score"]
    encoded_entry["ultra"] = api["ultra-mutations"][entry["ultra"]]

    mutations = [0] * 29
    for mutation in entry["mutations"]:
        mutations[api["mutations"][mutation]] = 1
    encoded_entry["mutations"] = mutations.join("")

    encoded_entry["wepA"] = api["weapons"][entry["weapons"][0]]
    encoded_entry["wepB"] = api["weapons"][entry["weapons"][1]]
    encoded_entry["crown"] = api["crowns"][entry["crown"]]
    encoded_entry["lasthit"] = api["enemies"][entry["lasthit"]]

    return encoded_entry

def decode_stream_data(entry):
    decoded_entry = {}
    decoded_entry["character"] = api["characters"][entry["char"]]
    decoded_entry["lasthit"] = api["enemies"][entry["lasthit"]]
    decoded_entry["world"] = api["worlds"][entry["world"]]
    decoded_entry["wlevel"] = entry["level"]
    decoded_entry["crown"] = api["crowns"][entry["crown"]]

    decoded_entry["weapons"] = []
    decoded_entry["weapons"].append(api["weapons"][entry["wepA"]])
    decoded_entry["weapons"].append(api["weapons"][entry["wepB"]])

    decoded_entry["skin"] = "B" if entry["skin"] == 1 else "A"
    # no clue how ultra works
    decoded_entry["charlvl"] = entry["charlvl"]
    decoded_entry["loops"] = entry["loops"]
    decoded_entry["win"] = entry["win"]

    decoded_entry["mutations"] = []
    pos = 0
    for mutation in entry["mutations"]:
        if mutation == 1:
            decoded_entry["mutations"].append(api["mutations"][pos])
        pos += 1

    decoded_entry["kills"] = entry["kills"]
    decoded_entry["health"] = entry["health"]
    decoded_entry["type"] = entry["type"]
    decoded_entry["timestamp"] = entry["timestamp"]
    return decoded_entry

def encode_stream_data(entry):
    encoded_entry = []
    encoded_entry["char"] = api["characters"][entry["character"]]
    encoded_entry["lasthit"] = api["enemies"][entry["lasthit"]]
    encoded_entry["world"] = api["worlds"][entry["world"]]
    encoded_entry["level"] = api["levels"][entry["wlevel"]]
    encoded_entry["crown"] = api["crown"][entry["crown"]]
    encoded_entry["wepA"] = api["weapons"][entry["weapons"][0]]
    encoded_entry["wepB"] = api["weapons"][entry["weapons"][1]]
    encoded_entry["skin"] = 1 if entry["skin"] == "B" else 0
    encoded_entry["ultra"] = entry["ultra"]
    encoded_entry["charlvl"] = entry["charlvl"]
    encoded_entry["loops"] = entry["loops"]
    encoded_entry["win"] = entry["win"]

    mutations = [0] * 29
    for mutation in entry["mutations"]:
        mutations[api["mutations"][mutation]] = 1
    encoded_entry["mutations"] = mutations.join("")

    encoded_entry["kills"] = entry["kills"]
    encoded_entry["health"] = entry["health"]
    encoded_entry["type"] = entry["type"]
    encoded_entry["timestamp"] = entry["timestamp"]
    return encoded_entry
