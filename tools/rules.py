import re

def decompose(keyword, in_str, script):
    comps = []
    reassembly_rule = ''
    for d in script: 
        if d['keyword'] == keyword:
            for rule in d['rules']:
                m = re.match(rule['decomp'], in_str, re.IGNORECASE)
                if m:
                    comps = list(m.groups())
                    reassembly_rule = get_reassembly_rule(rule)
                    break
            break
    return comps, reassembly_rule

def reassemble(components, reassembly_rule):
    response = 'Eliza: '
    reassembly_rule = reassembly_rule.split() 
    for comp in reassembly_rule:
        if comp.isnumeric():
            response += components[int(comp)-1] + ' '
        else:
            response += comp + ' '
    response = response[:-1]
    return response

def process_decomp_rules(script, tags):
    for d in script:
        for rule in d['rules']:
            rule['decomp'] = decomp_to_regex(rule['decomp'], tags) 
    return script

def preprocess_decomp_rule(in_str):
    in_str = re.sub('[()]', '', in_str)
    return in_str.split()


def decomp_to_regex(in_str, tags):
    out_str = ''
    in_str = preprocess_decomp_rule(in_str)
    for w in in_str:
        w = regexify(w, tags)
        out_str += '(' + w + r')\s*' 
    return out_str

def regexify(w, tags):
    if w == '0': 
        w = '.*'
    elif w.isnumeric() and int(w) > 0:
        w = r'(?:\b\w+\b[\s\r\n]*){' + w + '}'
    elif w[0] == "@":
        tag_name = w[1:].lower()
        w = tag_to_regex(tag_name, tags)
    else:
        w = r'\b' + w + r'\b'
    return w

def tag_to_regex(tag_name, tags):
    w = ''
    if tag_name in tags:
        w = r'\b(' + '|'.join(tags[tag_name]) + r')\b'
    return w

def update_last_used_reassembly_rule(rule):
    next_id = rule['last_used_reassembly_rule']+1
    if next_id >= len(rule['reassembly']):
        next_id = 0
    rule['last_used_reassembly_rule'] = next_id

def reset_all_last_used_reassembly_rule(script):
    for d in script:
        for rule in d['rules']:
            rule['last_used_reassembly_rule'] = 0

def get_reassembly_rule(rule):
    reassembly_rule = rule['reassembly'][rule['last_used_reassembly_rule']]
    update_last_used_reassembly_rule(rule)
    return reassembly_rule



def rank(sentences, script, substitutions):
    all_keywords = []
    all_ranks = []
    maximums = []

    for i in range(0, len(sentences)):
        sentences[i] = re.sub(r'[#$%&()*+,-./:;<=>?@[\]^_{|}~]', '', sentences[i])
        sentences[i] = substitute(sentences[i], substitutions)
        if sentences[i]:
            keywords = sentences[i].lower().split()
            all_keywords.append(keywords)
            ranks = get_ranks(keywords, script)
            maximums.append(max(ranks))
            all_ranks.append(ranks)
    max_rank = max(maximums)
    max_index = maximums.index(max_rank)
    keywords = all_keywords[max_index]
    ranks = all_ranks[max_index]
    sorted_keywords = [x for _,x in sorted(zip(ranks, keywords), reverse=True)]
    return sentences[max_index], sorted_keywords

def get_ranks(keywords, script):
    ranks = []
    for keyword in keywords:
        for d in script:
            if d['keyword'] == keyword:
                ranks.append(d['rank'])
                break
        else:
            ranks.append(0)
    return ranks

def substitute(in_str, substitutions):
    out_str = ''
    for word in in_str.split():
        if word.lower() in substitutions:
            out_str += substitutions[word.lower()] + ' '
        else:
            out_str += word + ' '
    return out_str
