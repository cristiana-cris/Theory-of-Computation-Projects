import sys
import os
# Adds the parent directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parse

def dfaGetContent(sections):                      
    transition={}
    dfa_content={}
    section_names=['sigma', 'delta', 'states', 'final', 'start']

    for name in sections:
        if name not in section_names:
            return -1
        if name=='sigma' or name=='states' or name=='final':
            dfa_content[name] = [line.strip() for line in sections[name]]
        elif name=='start':
            dfa_content[name]=sections[name][0]
        elif name=='delta':
            for line in sections[name]:
                initial, symbol, final=line.split(maxsplit=2)
                transition[(initial, symbol)] = final
            dfa_content[name]=transition
    return dfa_content

def dfaRules(sections, w, state, index):
    if state not in sections['states']:
        return 'State is not valid'
    if index==len(w):
        if state in sections['final']:
            return 'Accepted'
        return 'Not accepted'
    if w[index] not in sections['sigma']:
        return 'Symbol not in alphabet'
    return dfaRules(sections, w, sections['delta'][(state, w[index])], index+1)

def dfaResults(sections):
    dfa_content=dfaGetContent(sections) 
    #erorrs
    if dfa_content == -1:
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
            x = dfaRules(dfa_content, w, dfa_content['start'], 0)
            result=result+w+" "+x+" "+"\n"
    
    print(result, file=output_file)

def start():
    print("Introdu calea catre fisierul cu definitia: ")
    definition_file=input()

    sections=parse.getSections(definition_file)
    if sections == -1:
        print('Syntax error')
        return
    
    dfaResults(sections)
    
start()
