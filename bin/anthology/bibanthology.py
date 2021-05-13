from utiltest import bibtexparser
import json
import os

def expand2json(anthology_bib_path, anthology_json_basefolder):
    # delete everything in json base path
    with open(anthology_bib_path, "r") as bib_file:
        bibstring = bib_file.read()
        for entry in bibtexparser.generate(bibstring, keep_input=False):
            print(entry.bibid())

            entry = entry.as_dict()
            key = entry["bibid"]

            if key.startswith("CRITERIA:"):
                subfolder = key[key.rfind(":")]
                subfolder = ''.join(filter(str.isalnum, subfolder))
                folder = os.path.join(anthology_json_basefolder, subfolder)
                os.makedirs(folder, exist_ok=True)
                path = os.path.join(folder, "meta.jsonl")
            else:
                entry["fields"]["personids"] = json.loads(bytes.fromhex(entry["fields"]["personids"]))
                subfolder = key[:key.rfind("/")]
                subfolder = ''.join(filter(str.isalnum, subfolder))
                if "crossref" in entry["fields"]:
                    filename = entry["fields"]["crossref"]
                else:
                    filename = entry["bibid"]
                filename = ''.join(filter(str.isalnum, filename))
                folder = os.path.join(anthology_json_basefolder, subfolder)
                os.makedirs(folder, exist_ok=True)
                path = os.path.join(folder, filename+".jsonl")
            with open(path, "a") as json_file:
                print(json.dumps(entry), file=json_file)

#expand2json("testdata/ir-anthology.bib", "testdata/json")