
import re
from utiltest.util import find_char_after
from utiltest.util import find_char_after_no_error
from utiltest.latexparser import LatexParser

class BibtexEntry:
    def __init__(self, entrytype, bibid, fields_data, string=lambda: raise_(Exception("not defined"))):
        self.entrytype = entrytype
        self.bibid = bibid
        self.fields_data = fields_data
        self.string = string
        self.fields_data_cache = None

    def fields(self):
        if self.fields_data_cache is None:
            self.fields_data_cache = self.fields_data()
        return self.fields_data_cache

    def as_dict(self):
        d = {}
        d["entrytype"] = self.entrytype()
        d["bibid"] = self.bibid()
        d["fields"] = self.fields()
        return d


def create_bibtex_entry(entrytype, bibid, fields):
    return BibtexEntry(lambda: entrytype, lambda: bibid, lambda: fields)

def find_char_after_mirrorchar(string, target_char, index, open_char, close_char, espace_char="\\"):
    opened = 0
    if open_char==close_char:
        raise ValueError("open_char must not equal close_char")
    jump_next = False
    for i in range(index, len(string)):
        if jump_next:
            jump_next = False
            continue
        if string[i]==espace_char:
            jump_next = True
            continue
        if string[i]==open_char:
            opened += 1
            continue
        if string[i]==target_char:
            if opened==0:
                return i
        if string[i]==close_char:
            opened -= 1
    raise IndexError("Can't find the char >"+target_char+"< in the string >"+string[index:]+"<")

def contains_only_after(string, allowed, start, end_exclusive):
    for i in range(start, end_exclusive):
        if string[i] not in allowed:
            return False
    return True


def load_fields(input):
    start = 1
    final_end = input.rfind("}")
    end = find_char_after(input, "{", 1)
    start = end+1
    end = find_char_after(input, ",", start)
    start = end+1
    fields = {}
    latex = LatexParser()
    while True:
        if contains_only_after(input, " \t\n\r", start, final_end):
            break
        end = find_char_after(input, "=", start)
        key = input[start:end].strip()
        start = find_char_after(input, "{", end)+1
        end = find_char_after_mirrorchar(input, "}", start, "{", "}")+1
        value = "{"+re.sub('[\t \n\r]+', ' ', input[start:end]).strip()
        start = end+1
        fields[key] = latex.decode(value)
    return fields

def raise_(ex):
    raise ex

def loads_entry(input, skip_fields=False, keep_input=True):
    lastchar_index = input.rfind("}")
    start = 1
    end = find_char_after(input, "{", 1)
    entrytype = input[start:end]
    start = end+1
    end = find_char_after(input, ",", start)
    bibid = input[start:end]
    return BibtexEntry(
        lambda: entrytype, 
        lambda: bibid, 
        (lambda: load_fields(input)) if not skip_fields else (lambda: raise_(Exception("not computed because 'skip_fields' was set"))), 
        (lambda: input) if keep_input else (lambda: raise_(Exception("was not stored because keep_input was not set")))
    )


def dumps_entry(bibtex_entry, use_raw=[]):
    output = "@"+bibtex_entry.entrytype+"{"+bibtex_entry.bibid+",\n"
    latex = LatexParser()
    l = []
    for key in sorted(bibtex_entry.fields.keys()):
        if key in use_raw:
            text = bibtex_entry.fields[key]
        else:
            text = latex.encode(bibtex_entry.fields[key])
        l.append("  "+key+" = {"+text+"}")
    output += ",\n".join(l)+"\n}"
    return output


def loads(input, skip_fields=False, keep_input=True):
    start = 0
    output = []
    lastchar_index = input.rfind("}")
    while True:
        if contains_only_after(input, " \t\n\r", start, lastchar_index):
            break
        temp = find_char_after(input, "{", start)+1
        end = find_char_after_mirrorchar(input, "}", temp, "{", "}")+1
        output.append(loads_entry(input[start:end], skip_fields, keep_input))
        start = end
    return output




def generate(input, skip_fields=False, keep_input=True):
    start = 0
    l = len(input)-1
    lastchar_index = input.rfind("}")
    while True:
        while not input[start] == "@":
            if start == l:
                return
            start += 1
        temp = find_char_after(input, "{", start)+1
        end = find_char_after_mirrorchar(input, "}", temp, "{", "}")+1
        yield loads_entry(input[start:end], skip_fields, keep_input)
        start = end