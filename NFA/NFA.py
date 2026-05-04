import sys
import os
# Adds the parent directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parse

def nfaGetContent(sections):  
    #parses sections and extracts information for a NFA   
    #returns -1 if the information is not good for a NFA                 
    transition={}
    nfa_content={}
    section_names=['sigma', 'delta', 'states', 'final', 'start']

    nfa_content['sigma']=['epsilon']
    for name in sections:
        if name not in section_names:
            return -1
        if name=='sigma' or name=='states' or name=='final':
            #x.strip to accept ', '
            nfa_content[name]=[x.strip() for line in sections[name] for x in line.split(',')] 
        elif name=='start':
            nfa_content[name]=sections[name][0]
        elif name=='delta':
            for line in sections[name]:
                initial, symbol, final=line.split(maxsplit=2)
                if not ((initial, symbol) in transition):
                    transition[(initial, symbol)]=[]
                transition[(initial, symbol)].append(final)
            nfa_content[name]=transition
    return nfa_content

def epsilonTransition(delta, current):
    #returns a list with all the states that are reached with epsilon,
    #for every state that we are in. Works for q0 -epsilon-> q1 -epsilon-> q2(adds all)
    stack = [x for x in current]
    while stack:
        state = stack.pop()
        key = (state, 'epsilon')
        if key in delta:
            for next_state in delta[key]:
                if next_state not in current:
                    current.append(next_state)
                    stack.append(next_state)
    return current

def nfaRules(sections, w, current):
    #in current we put all the states that the automata could be in at this specific step
    for symbol in w:
        #verify alphabet
        if symbol not in sections['sigma']:
            return 'Symbol not in alphabet'
        
        #adding states reached by epsilon
        current=epsilonTransition(sections['delta'], current)
        next_states=[]
        
        for c_state in current:
            key = (c_state, symbol)
            if key in sections['delta']:
                for n_state in sections['delta'][key]:
                    if n_state not in next_states:
                        next_states.append(n_state)
        #if automata dies
        if next_states==[]:
            return 'Not Accepted'
        current=epsilonTransition(sections['delta'], next_states)

    #exit condition
    for x in sections['final']:
        if x in current:
            return 'Accepted'
        return 'Not Accepted'

def nfaResults(sections):
    nfa_content=nfaGetContent(sections) 
    #erorrs
    if nfa_content == -1:
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
            x = nfaRules(nfa_content, w, [nfa_content['start']])
            result=result+w+" "+x+" "+"\n"
    
    print(result, file=output_file)

def start():
    print("Write path for the file with the definition: ")
    definition_file=input()

    sections=parse.getSections(definition_file)
    if sections == -1:
        print('Syntax error')
        return
    
    nfaResults(sections)
    
start()