from utiltest import bibtexparser
import json
import os
import re
from pathlib import Path
import shutil
from tqdm import tqdm

def expand2json(anthology_bib_path, anthology_json_basefolder, anthology_json_temp_basefolder):
    # convert bib to jsonl files
    # one file for each event
    os.makedirs("data/files", exist_ok=True)
    name2bucket = {}
    with open(anthology_bib_path, "r") as bib_file:
        bibstring = bib_file.read()
        with tqdm(total=bibstring.count("personids") + bibstring.count("@misc")) as pbar:
            for entry_obj in bibtexparser.generate(bibstring, keep_input=True):
                pbar.update(1)

                entry = entry_obj.as_dict()
                key = entry["bibid"]

                if key.startswith("CRITERIA:"):
                    # strip "CRITERIA:"
                    bucket = key[9:]
                    start = bucket.find(":")+1
                    bucket = bucket[start:]
                    bucket = os.path.join(*re.findall('[A-Za-z0-9]+', bucket))
                    names = map(lambda x: x.strip(), entry["fields"]["create-from"].split(","))
                    names = map(lambda x: os.path.join(*re.findall('[A-Za-z0-9]+', x)), names)
                    names = map(lambda x: os.path.join(anthology_json_temp_basefolder, x), names)
                    for name in names:
                        name2bucket[name] = bucket
                    folder = os.path.join(anthology_json_basefolder, "meta")
                    os.makedirs(folder, exist_ok=True)
                    path = os.path.join(folder, bucket+".json")
                else:
                    if key.startswith("MANUAL:"):
                        with open("data/files/"+key.replace(":", "_").replace("/", "_")+".bib", "w") as f:
                            for line in entry_obj.string().split("\n"):
                                i = 0
                                for _ in range(0, len(line)):
                                    if line[i] != " ":
                                        break
                                    i += 1
                                if line[i:].startswith("personids") or line[i:].startswith("xml-checksum"):
                                    continue
                                print(line, file=f)
                    start = key.find("/")+1
                    end = start+key[start:].find("/")
                    subfolder = key[:end]
                    subfolder = os.path.join(*re.findall('[A-Za-z0-9]+', subfolder))
                    entry["fields"]["personids"] = json.loads(bytes.fromhex(entry["fields"]["personids"]))
                    if entry["entrytype"]=="article" and  "volume" in entry["fields"]:
                        filename = "ir0anthology0volumeA"+entry["fields"]["volume"]
                        if "number" in entry["fields"]:
                            filename += "A"+entry["fields"]["number"]
                    else: 
                        if "crossref" in entry["fields"]:
                            filename = entry["fields"]["crossref"]
                        else:
                            filename = entry["bibid"]
                    start = filename.find("/")+1
                    end = start+filename[start:].find("/")
                    filename = filename[end+1:]
                    filename = ''.join(filter(str.isalnum, filename))
                    folder = os.path.join(anthology_json_temp_basefolder, subfolder)
                    os.makedirs(folder, exist_ok=True)
                    path = os.path.join(folder, filename+".jsonl")
                with open(path, "a") as json_file:
                    print(json.dumps(entry), file=json_file)
    # sort by actual type
    for name, bucket in name2bucket.items():
        for src_file in Path(name).glob('*.*'):
            src_file = str(src_file)
            if src_file.endswith("meta.jsonl"):
                folder = os.path.join(anthology_json_basefolder, venues)
                os.makedirs(folder, exist_ok=True)
                os.rename(src_file, os.path.join(folder, bucket+".json"))
                continue
            entries = {}
            head = None
            booktitle = None
            with open(src_file, "r") as file:
                for line in file:
                    line = json.loads(line)
                    entries[line["bibid"]] = line
                    head = line["fields"]["crossref"] if "crossref" in line["fields"] else head
                    booktitle = line["fields"]["booktitle"] if "booktitle" in line["fields"] else booktitle
            if len(entries)==1:
                print("WARNING: Volume {} has only one paper.".format(src_file))
            if head is not None:
                if head not in entries:
                    print("WARNING: crossref: "+head+" not found")
                    head = None
                else:
                    head_d = entries[head]
                    del entries[head]
                    head = head_d
                    del head_d
            t = outputType(src_file, head, booktitle)
            entries_values = sorted(entries.values(), key=entry_sort_key)
            fileName = os.path.basename(src_file)
            folder = os.path.join(anthology_json_basefolder, t, bucket)
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, fileName), "w") as file:
                if head is not None:
                    print(json.dumps(head), file=file)
                for entry in entries_values:
                    print(json.dumps(entry), file=file)

def entry_sort_key(entry):
    if "pages" in entry["fields"]:
        pages = entry["fields"]["pages"]
        l = re.findall(r'^\d+', pages)
        if len(l)!=0:
            return l[0].rjust(20,"0")
    if "title" in entry["fields"]:
        title = entry["fields"]["title"]
        return title[0:round(min(20, len(title)))].ljust(20, "z")
    return entry["bibid"].ljust(20, "z")
    

def outputType(src_file, head, booktitle):
    if head is not None:
        title = head["fields"]["title"].lower()
        if "workshop" in title:
            return "workshop"
        if "conference" in title:
            return "conference"
        if "journal" in title:
            return "journal"
    if booktitle is not None:
        booktitle = booktitle.lower()
        if "workshop" in booktitle:
            return "workshop"
        if "conference" in booktitle:
            return "conference"
        if "journal" in booktitle:
            return "journal"
    if "/conf/" in src_file:
        return "conference"
    if "/journals/" in src_file:
        return "journal"
    if "/workshop/" in src_file:
        return "workshop"
    raise Exception("unkown type")

#expand2json("testdata/ir-anthology.small.bib", "testdata/final", "testdata/temp")
expand2json("data/ir-anthology.bib", "data/final", "data/temp")