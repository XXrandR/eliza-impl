import os

from tools.startup import setup
from tools.rules import reset_all_last_used_reassembly_rule
from tools.response import prepare_response, generate_response
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = os.path.join(PROJECT_DIR, 'data')
GENERAL_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'basic.json')
SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'doctor.json')

def main():
    memory_stack = []
    general_script, script, memory_inputs, exit_inputs = setup(GENERAL_SCRIPT_PATH, SCRIPT_PATH)
    print("""
 _ |o_  _ 
(-`||/_(_|
          
          """)
    in_str = input("Eliza: Welcome.\nYou: ")
    in_str_l = in_str.lower()
    while in_str_l not in exit_inputs:
        if not in_str_l.islower():
            response = prepare_response('Eliza: Please, use letters. I am human, after all.')
        elif in_str_l == 'reset':
            reset_all_last_used_reassembly_rule(script)
            response = prepare_response('Eliza: Reset complete.')
        else:
            response = generate_response(in_str, script, general_script['substitutions'], memory_stack, memory_inputs)
        in_str = input(response)
        in_str_l = in_str.lower()
    print("Eliza: Goodbye.\n")

if __name__=="__main__":
   main()
