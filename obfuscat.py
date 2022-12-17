#!/usr/bin/env python

# SPDX-FileCopyrightText: 2022, Marsiske Stefan
# SPDX-License-Identifier: AGPL-3.0-or-later

import os, sys, pysodium, binascii, itertools, tempfile

pgpwords=[["aardvark", "absurd", "accrue", "acme", "adrift", "adult", "afflict", "ahead", "aimless", "Algol", "allow", "alone", "ammo", "ancient", "apple",
           "artist", "assume", "Athens", "atlas", "Aztec", "baboon", "backfield", "backward", "banjo", "beaming", "bedlamp", "beehive", "beeswax", "befriend", "Belfast",
           "berserk", "billiard", "bison", "blackjack", "blockade", "blowtorch", "bluebird", "bombast", "bookshelf", "brackish", "breadline", "breakup", "brickyard", "briefcase", "Burbank",
           "button", "buzzard", "cement", "chairlift", "chatter", "checkup", "chisel", "choking", "chopper", "Christmas", "clamshell", "classic", "classroom", "cleanup", "clockwork",
           "cobra", "commence", "concert", "cowbell", "crackdown", "cranky", "crowfoot", "crucial", "crumpled", "crusade", "cubic", "dashboard", "deadbolt", "deckhand", "dogsled",
           "dragnet", "drainage", "dreadful", "drifter", "dropper", "drumbeat", "drunken", "Dupont", "dwelling", "eating", "edict", "egghead", "eightball", "endorse", "endow",
           "enlist", "erase", "escape", "exceed", "eyeglass", "eyetooth", "facial", "fallout", "flagpole", "flatfoot", "flytrap", "fracture", "framework", "freedom", "frighten",
           "gazelle", "Geiger", "glitter", "glucose", "goggles", "goldfish", "gremlin", "guidance", "hamlet", "highchair", "hockey", "indoors", "indulge", "inverse", "involve",
           "island", "jawbone", "keyboard", "kickoff", "kiwi", "klaxon", "locale", "lockup", "merit", "minnow", "miser", "Mohawk", "mural", "music", "necklace",
           "Neptune", "newborn", "nightbird", "Oakland", "obtuse", "offload", "optic", "orca", "payday", "peachy", "pheasant", "physique", "playhouse", "Pluto", "preclude",
           "prefer", "preshrunk", "printer", "prowler", "pupil", "puppy", "python", "quadrant", "quiver", "quota", "ragtime", "ratchet", "rebirth", "reform", "regain",
           "reindeer", "rematch", "repay", "retouch", "revenge", "reward", "rhythm", "ribcage", "ringbolt", "robust", "rocker", "ruffled", "sailboat", "sawdust", "scallion",
           "scenic", "scorecard", "Scotland", "seabird", "select", "sentence", "shadow", "shamrock", "showgirl", "skullcap", "skydive", "slingshot", "slowdown", "snapline", "snapshot",
           "snowcap", "snowslide", "solo", "southward", "soybean", "spaniel", "spearhead", "spellbind", "spheroid", "spigot", "spindle", "spyglass", "stagehand", "stagnate", "stairway",
           "standard", "stapler", "steamship", "sterling", "stockman", "stopwatch", "stormy", "sugar", "surmount", "suspense", "sweatband", "swelter", "tactics", "talon", "tapeworm",
           "tempest", "tiger", "tissue", "tonic", "topmost", "tracker", "transit", "trauma", "treadmill", "Trojan", "trouble", "tumor", "tunnel", "tycoon", "uncut",
           "unearth", "unwind", "uproot", "upset", "upshot", "vapor", "village", "virus", "Vulcan", "waffle", "wallet", "watchword", "wayside", "willow", "woodlark", "Zulu"],
          ["adroitness", "adviser", "aftermath", "aggregate", "alkali", "almighty", "amulet", "amusement", "antenna", "applicant", "Apollo", "armistice", "article", "asteroid", "Atlantic",
           "atmosphere", "autopsy", "Babylon", "backwater", "barbecue", "belowground", "bifocals", "bodyguard", "bookseller", "borderline", "bottomless", "Bradbury", "bravado",
           "Brazilian", "breakaway", "Burlington", "businessman", "butterfat", "Camelot", "candidate", "cannonball", "Capricorn", "caravan", "caretaker", "celebrate",
           "cellulose", "certify", "chambermaid", "Cherokee", "Chicago", "clergyman", "coherence", "combustion", "commando", "company", "component", "concurrent",
           "confidence", "conformist", "congregate", "consensus", "consulting", "corporate", "corrosion", "councilman", "crossover", "crucifix", "cumbersome", "customer", "Dakota",
           "decadence", "December", "decimal", "designing", "detector", "detergent", "determine", "dictator", "dinosaur", "direction", "disable", "disbelief", "disruptive",
           "distortion", "document", "embezzle", "enchanting", "enrollment", "enterprise", "equation", "equipment", "escapade", "Eskimo", "everyday", "examine", "existence",
           "exodus", "fascinate", "filament", "finicky", "forever", "fortitude", "frequency", "gadgetry", "Galveston", "getaway", "glossary", "gossamer", "graduate", "gravity",
           "guitarist", "hamburger", "Hamilton", "handiwork", "hazardous", "headwaters", "hemisphere", "hesitate", "hideaway", "holiness", "hurricane", "hydraulic",
           "impartial", "impetus", "inception", "indigo", "inertia", "infancy", "inferno", "informant", "insincere", "insurgent", "integrate", "intention", "inventive", "Istanbul",
           "Jamaica", "Jupiter", "leprosy", "letterhead", "liberty", "maritime", "matchmaker", "maverick", "Medusa", "megaton", "microscope", "microwave", "midsummer", "millionaire",
           "miracle", "misnomer", "molasses", "molecule", "Montana", "monument", "mosquito", "narrative", "nebula", "newsletter", "Norwegian", "October", "Ohio", "onlooker", "opulent",
           "Orlando", "outfielder", "Pacific", "pandemic", "Pandora", "paperweight", "paragon", "paragraph", "paramount", "passenger", "pedigree", "Pegasus", "penetrate",
           "perceptive", "performance", "pharmacy", "phonetic", "photograph", "pioneer", "pocketful", "politeness", "positive", "potato", "processor", "provincial",
           "proximate", "puberty", "publisher", "pyramid", "quantity", "racketeer", "rebellion", "recipe", "recover", "repellent", "replica", "reproduce", "resistor", "responsive",
           "retraction", "retrieval", "retrospect", "revenue", "revival", "revolver", "sandalwood", "sardonic", "Saturday", "savagery", "scavenger", "sensation", "sociable",
           "souvenir", "specialist", "speculate", "stethoscope", "stupendous", "supportive", "surrender", "suspicious", "sympathy", "tambourine", "telephone", "therapist",
           "tobacco", "tolerance", "tomorrow", "torpedo", "tradition", "travesty", "trombonist", "truncated", "typewriter", "ultimate", "undaunted", "underfoot", "unicorn", "unify",
           "universe", "unravel", "upcoming", "vacancy", "vagabond", "vertigo", "Virginia", "visitor", "vocalist", "voyager", "warranty", "Waterloo", "whimsical", "Wichita",
           "Wilmington", "Wyoming", "yesteryear", "Yucatan"]]

mode="map"
if "-d" in sys.argv:
    mode="ummap"
    del sys.argv[sys.argv.index('-d')]
    if len(sys.argv) != 3:
        print("usage: obfuscat 'sensitive' 'salt' length")
        print("usage: obfuscat -d 'asdf-zxcv-qwer...' 'salt'")
        sys.exit(1)

elif len(sys.argv) != 4:
    print("usage: obfuscat 'sensitive' 'salt' length")
    print("usage: obfuscat -d 'asdf-zxcv-qwer...' 'salt'")
    sys.exit(1)

pepper = sys.argv[2]

# load serialized mapping table
mapping = {}
unmapping = {}
if os.path.exists(f"{pepper}.map"):
    # yeah, the salt could be a path traversal 0day!!!5!
    with open(f"{pepper}.map","rb") as fd:
        for line in fd.readlines():
            if line == b"\n": continue
            shorthex, longhex, plain = line.decode('utf8').strip().split(":",2)
            short = binascii.unhexlify(shorthex)
            if short in mapping:
                print(f"ERROR: duplicate detected: {plain} is already in {pepper}.map")
                sys.exit(1)
            long = binascii.unhexlify(longhex)
            mapping[short]=(long, plain)
            if mode=="map":
                unmapping[(plain,int(sys.argv[3]))]=short

if mode == "map":
    salt = pysodium.crypto_generichash(pepper.encode("utf8"), outlen=pysodium.crypto_pwhash_SALTBYTES)
    sensitive = sys.argv[1]
    obfus_len = int(sys.argv[3])

    obfusbin = unmapping.get((sensitive,obfus_len))
    if not obfusbin:
        if len(mapping) >= 2**(obfus_len*8):
            print(f"ERROR: cannot add new mapping without colliding with other inputs")
            sys.exit(1)

        # streamkey is a kind of a long&slow hash of the sensitive input to be obfuscated
        # chance of collisions is negligible
        streamkey = pysodium.crypto_pwhash(pysodium.crypto_stream_KEYBYTES, sensitive.encode('utf8'), salt,
                                        pysodium.crypto_pwhash_OPSLIMIT_INTERACTIVE, pysodium.crypto_pwhash_MEMLIMIT_INTERACTIVE)
        # obfusbin is a short high entropy derived from the sensitive input to be obfuscated
        # depending on the length of obfusbin there might be collisions. handle those

        nonce = b'\x00'*pysodium.crypto_stream_NONCEBYTES
        obfusbin = pysodium.crypto_stream(obfus_len, nonce, streamkey)
        while(mapping.get(obfusbin) and mapping[obfusbin][0]!=streamkey):
            pysodium.sodium_increment(nonce)
            obfusbin = pysodium.crypto_stream(obfus_len, nonce, streamkey)

        # add new mapping to mapping
        mapping[obfusbin]=(streamkey, sensitive)

        fd, fname = tempfile.mkstemp(dir=".")
        for k, v in mapping.items():
            os.write(fd,f"{k.hex()}:{v[0].hex()}:{v[1]}\n".encode("utf8"))
        os.close(fd)
        os.replace(fname,f"{pepper}.map")

    words = (pgpwords[idx][b] for b, idx in zip(obfusbin, itertools.cycle((0,1))))
    print('-'.join(words))

else: # unmap
    pgpwords = {(table,word):i for table in range(2) for i, word in enumerate(pgpwords[table])}

    words = sys.argv[1].split("-")

    obfusbin = []
    for word, idx in zip(words, itertools.cycle((0,1))):
        if (idx,word) not in pgpwords:
            print(f"ERROR '{word}' is invalid, possibly corrupted input")
            sys.exit(1)
        obfusbin.append(pgpwords[(idx,word)])
    obfusbin = bytes(obfusbin)
    plain = mapping.get(obfusbin)
    if not plain:
        print(f"ERROR: {'-'.join(words)} not found in {pepper}.map")
        sys.exit(1)
    print(plain[1])
