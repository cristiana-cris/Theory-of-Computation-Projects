import sys
import os
import random
# Adds the parent directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parse

def grammarGetContent(sections):                      
    transition={}
    gr_content={}
    section_names=['sigma', 'start', 'variables', 'rules']

    for name in sections:
        if name not in section_names:
            return -1
        if name=='sigma':
            gr_content[name]=[line.strip() for line in sections[name]]
        elif name=='start':
            gr_content[name]=sections[name][0]
        elif name=='variables':
            gr_content['variables']=[line.strip() for line in sections[name]]
        elif name=='rules':
            for line in sections[name]:
                var, substitution_raw=line.split('->')
                if var not in transition:
                    transition[var]=[]
                
                transition[var].append(substitution_raw)
            gr_content[name]=transition
    return gr_content

def substitute(rules, variable, w):
    # check if variable is in w
    v_index=w.index(variable)
    if(v_index==-1): 
        return w
    #choose a random substitution for variable
    form=random.choice(rules[variable])
    w[v_index : v_index + 1]=[x for x in form]
    return w

def generate(rules, variables, w):
    index=0
    while index<len(w):
        
        while w[index] in variables:
            w=substitute(rules, w[index], w)
        index+=1
    return w
    

def CFGResults(sections):
    gr_content = grammarGetContent(sections)
    if gr_content == -1:
        print("Sections are not defined correctly for grammar.")
        return

    print(gr_content)
    print("Write the path for output file: ")
    # output_file = input()
    output_file="CFG/out.txt"
    
    first_var = gr_content['start']
    rules = gr_content['rules']
    variables = gr_content['variables']

    #in loc sa retin cuvantul ca string il retin la lista
    w=[first_var]
    # w=''.join(generate(rules, variables, w))
    # print(w)
    # # We start with a list containing just the start symbol
    # start_tokens = [first_var]
    
    # print(f"Starting generation from: {start_tokens}")
    # final_sentence = generate(rules, variables, first_var)
    
    # print(f"\nFinal Result: {final_sentence}")
    # # You can now save final_sentence to output_file


def start():
    print("Write path for file with definition: ")
    # definition_file=input()
    definition_file="CFG/def.txt"

    sections=parse.getSections(definition_file)
    if sections == -1:
        print('Syntax error')
        return
    
    CFGResults(sections)
    
start()
