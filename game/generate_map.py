from collections import deque
from collections import defaultdict
import random
import re

symbol={1:'w', 2:'a', 3:'s', 4:'d'}
directions=[1, 2, 3, 4]
opposite={1:3, 2:4,  4:2, 3:1}
#direction offsets
offset={1:(0, 1), 2:(-1, 0), 3:(0, -1), 4:(1, 0)}

def write_delta(filepath, delta):
    lines = []
    for (state, sym), stack_map in delta.items():
        for top_stack, (next_state, push) in stack_map.items():
            lines.append(f"\t{state} {sym} {top_stack} {next_state} {push}")

    output = "\n".join(lines)

    with open(filepath, 'r') as f:
        content = f.read()

    new_block = f"delta{{\n{output}\n}}"
    updated = re.sub(r'delta\{.*?\}', new_block, content, flags=re.DOTALL)

    with open(filepath, 'w') as f:
        f.write(updated)

def updateLayout(layout, delta, dir, curr_state, next_state):
    layout[curr_state][dir]=1
    layout[next_state][opposite[dir]]=1
    delta[(curr_state, symbol[dir])]['epsilon']=(next_state, 'epsilon')
    delta[(next_state, symbol[opposite[dir]])]['epsilon']=(curr_state, 'epsilon')
    return (layout, delta)

def changeCoord(dir, layout, curr_state):
    dx, dy=offset[dir]
    x, y=layout[curr_state][0]
    return (x+dx, y+dy)

def assignRandom(delta, layout, used_states, unplaced, directions, curr_state, nr_connections):
    #reverse search
    coord_map={tuple(data[0]): state for state, data in layout.items()}

    for _ in range(nr_connections):
        #room has 4 connections
        available_dir=[d for d in directions if not layout[curr_state][d]]
        if not available_dir:
            return (delta, layout, used_states, unplaced)

        #if all rooms are placed
        if not unplaced:
            break
        next_state=unplaced[0]
        if next_state==curr_state:
            if len(unplaced)>=1:
                next_state=unplaced[1]
            else: break

        dir=random.choice(available_dir) 
        
        #check if room automatically connects to other rooms, by coordinates
        new_coord=changeCoord(dir, layout, curr_state)

        #change if neighbour would be start/a state that is not yet put
        while new_coord==(0,0):
            dir=random.choice(available_dir)
            new_coord=changeCoord(dir, layout, curr_state)
        #check if it automatically connects to other states
        if new_coord not in coord_map:
            layout[next_state][0]=list(new_coord)
        else:
            next_state=coord_map[new_coord]

        layout, delta=updateLayout(layout, delta, dir, curr_state, next_state)

        used_states.append(next_state)
        if unplaced and next_state in unplaced:
            unplaced.remove(next_state)

    return (delta, layout, used_states, unplaced)

def assignFinish(layout, delta, processed):
    finish='finish'
    last=len(processed)-1
    candidate=processed[last]
    available_dir=[d for d in directions if not layout[candidate][d]]

    if candidate=='entrance' and not available_dir:
        last-=1
        candidate=processed[last]
        available_dir=[d for d in directions if not layout[candidate][d]]

    dir=random.choice(available_dir)

    layout, delta=updateLayout(layout, delta, dir, candidate, finish)

    return (layout, delta)

def assignItems(delta, dependence, proccesed, items):
    length=len(items)-1
    proccesed.remove('entrance')
    while length>=0:
        state=random.choice(proccesed)
        item=items[length]
        delta[(state, 'pick')][dependence[item]]=(state, item)
        items.pop()
        length-=1

    return delta
   
def generate_map(sections, definition_file):
    start='start'
    delta=defaultdict(dict)
    #states only has the 'normal states, without start and finish
    unplaced=[x for x in sections['states'] if x!=start and x!='finish' and x!='entrance']
    
    #state: ([coordinates -> x, y], up, left, down, right)
    layout={state: [[0, 0], 0, 0, 0, 0] for state in sections['states']}
    
    #assign entrence to 'start'
    dir=random.choice(directions) 
    layout, delta=updateLayout(layout, delta, dir, start, 'entrance')
    layout['entrance'][0]=list(changeCoord(dir, layout, start))

    random.shuffle(unplaced)

    #starting with entrance
    used_states=deque()
    used_states.append('entrance')
    processed = set()

    while used_states or unplaced:
        if used_states:
            curr_state = used_states.popleft()
            if curr_state in processed:
                continue
            processed.add(curr_state)
            connection_range = [1, 2, 3]
        else:
            curr_state = unplaced.pop(0)
            connection_range = [1, 2, 3, 4]

        nr_connections = random.choice(connection_range)
        delta, layout, used_states, unplaced=assignRandom(delta, layout, used_states, unplaced, directions, curr_state, nr_connections)
    
    #now processed contains all the states
    processed=list(processed)
    #assign finish
    layout, delta=assignFinish(layout, delta, processed)

    #assign items to states
    items=[x for x in sections['gamma'] if x!='epsilon']
    dependence=sections['gammaRules']
    delta=assignItems(delta, dependence, processed, items)

    #write in definiton file
    write_delta(definition_file, delta)
    return delta