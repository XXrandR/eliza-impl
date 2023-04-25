import json

from tools.rules import process_decomp_rules

def setup(general_script_path, script_path):
    general_script = load_script(general_script_path)
    script = load_script(script_path)
    script = process_decomp_rules(script, general_script['tags'])
    memory_inputs = general_script['memory_inputs']
    exit_inputs = general_script['exit_inputs']

    return general_script, script, memory_inputs, exit_inputs

def load_script(script_path):
    with open(script_path) as f:
        script = json.load(f)
    return script
