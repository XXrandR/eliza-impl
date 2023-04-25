import re

from tools.rules import rank
from tools.rules import decompose, reassemble

def generate_response(in_str, script, substitutions, memory_stack, memory_inputs):
    sentences = re.split(r'[.,!?](?!$)', in_str)
    sentence, sorted_keywords = rank(sentences, script, substitutions)
    for keyword in sorted_keywords:
        comps, reassembly_rule = decompose(keyword, sentence, script)
        if comps:
            response = reassemble(comps, reassembly_rule)
            if keyword in memory_inputs:
                generate_memory_response(sentence, script, memory_stack)
            break
    else:
        if memory_stack:
            response = memory_stack.pop()
        else:
            response = generate_generic_response(script)
    response = prepare_response(response)
    return response

def generate_generic_response(script):
    comps, reassembly_rule = decompose('$', '$', script)
    return reassemble(comps, reassembly_rule)

def generate_memory_response(sentence, script, memory_stack):
    mem_comps, mem_reassembly_rule = decompose('^', sentence, script)
    mem_response = reassemble(mem_comps, mem_reassembly_rule)
    memory_stack.append(mem_response)

def prepare_response(response):
    response = clean_string(response)
    response += "\nYou: "
    return response

def clean_string(in_str):
    in_str = ' '.join(in_str.split())
    in_str = re.sub(r'\s([?.!"](?:\s|$))', r'\1', in_str)

    return in_str
