import sys
import os
# Adds the parent directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parse import *

def dpdaGetContent(sections):  
    #parses sections and extracts information for a DPDA   
    #returns -1 if the information is not good for a DPDA              
    transition={}
    dpda_content={}
    section_names=['sigma', 'delta', 'states', 'final', 'start', 'gamma']

    for name in sections:
        if name not in section_names:
            return -1
        if name in ['sigma', 'states', 'final', 'gamma']:
            #x.strip to accept ', '
            dpda_content[name]=[x.strip() for line in sections[name] for x in line.split(',')] 
        elif name=='start':
            dpda_content[name]=sections[name][0]
        elif name=='delta':
            #has the form (current state, symbol): top_stack: (next state, what is going to pe pushed)
            for line in sections[name]:
                initial, symbol, s_stack, final, f_stack=line.split(maxsplit=4)
                key=(initial, symbol)
                if key not in transition:
                    transition[key]={}
                if s_stack not in transition[key]:
                    transition[key][s_stack]={}
                if (final, f_stack) not in transition[key][s_stack]:
                    transition[key][s_stack]=(final, f_stack)

            dpda_content[name]=transition

    dpda_content['sigma'].append('epsilon')
    dpda_content['gamma'].append('epsilon')
    return dpda_content

def transition(delta, key, stack):
    top=stack[-1] if stack else 'epsilon'
    if key in delta:
        if top not in delta[key]:
            top='epsilon'
        if top in delta[key]:
            next_state=delta[key][top][0]
            symbol_push=delta[key][top][1]
            if symbol_push=='epsilon':
                if stack: stack.pop()
            else:
                stack.append(symbol_push)
            return (next_state, stack)
    return -1

def dpdaRules(sections, w, state, index, stack):
    if state not in sections['states']:
        return 'State is not valid'
    
    delta=sections['delta']
    #epsilon transitions
    key=(state, 'epsilon')
    next=transition(delta, key, stack)
    if next!=-1:
        state, stack=next

    #exit condition
    if index==len(w):
        if state in sections['final'] and not stack:
            return 'Accepted'
        return 'Not Accepted'
    #checking alphabet
    if w[index] not in sections['sigma']:
        return 'Symbol not in alphabet'

    key=(state, w[index])
    next=transition(delta, key, stack)

    if next==-1:
        return "No valid transitions for input"
    next_state, stack=next
    
    return dpdaRules(sections, w, next_state, index+1, stack)


def dpdaResults(sections):
    dpda_content=dpdaGetContent(sections) 
    #erorrs
    if dpda_content == -1:
        print("Sections are not defined correctly for DFA")
        return

    #defining files
    print("Write the path for input file: ")
    input_file=input()
    print("Write the path for output file: ")
    output_file=input()
    output_file=open(output_file, 'w')

    #checking each string
    result=''
    with open(input_file, 'r') as f:
        for line in f.readlines():
            w=line.strip()
            x = dpdaRules(dpda_content, w, dpda_content['start'], 0, [])
            result=result+w+" "+x+" "+"\n"
    
    print(result, file=output_file)

def start():
    print("Write path for the file with the definition: ")
    definition_file=input()

    sections=getSections(definition_file)
    if sections == -1:
        print('Syntax error')
        return
    
    dpdaResults(sections)
    
start()