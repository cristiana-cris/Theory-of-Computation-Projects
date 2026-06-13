import sys
import os
import re
# Adds the parent directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parse
import DPDA
import visuals
import generate_map as genmap

def next_level(definition_file):
    def increment(match):
        return f"lvl{int(match.group(1)) + 1}.txt"
    
    next_file = re.sub(r'lvl(\d+)\.txt', increment, definition_file)
    
    if not os.path.exists(next_file):
        visuals.print_game_complete()
        return None

    visuals.print_level_transition(next_file)
    return next_file

def gameCheck(sections):
    name='gammaRules'
    if name not in sections:
        return {}
    dependence={}
    for line in sections[name]:
        needed, has_need=line.split('->')
        dependence[has_need]=needed

    for item in sections['gamma']:
        if item not in dependence:
            dependence[item]='epsilon'

    sections[name]=dependence
    return sections

def gameTransition(delta, state, action, stack):
    top=stack[-1] if stack else 'epsilon'
    key=(state, action)

    if key in delta:
        if top not in delta[key]:
            top='epsilon'
        if top in delta[key]:
            next_state=delta[key][top][0]
            symbol_push=delta[key][top][1]

            #item picked
            if action=='pick':
                if symbol_push in stack:
                    print(f"You already have the {symbol_push}!")
                else:
                    print(f"You picked up a {symbol_push}.")

            if top!='epsilon' and stack:
                stack.pop()
            if symbol_push!='epsilon':
                stack.append(symbol_push)
                
            return (next_state, stack)
        
        #locked item
        elif action=='pick':
            print("Can't access that item yet. Be more curious!")

    #no item
    elif action=='pick':
        print("No items to pick up from this room :(")

    return -1

def playLVL(game_content, level=1):
    result=0
    stack=[]
    state=game_content['start']

    while result==0:
        print()
        visuals.print_room(state, game_content, stack, level=level)
        action=input().strip()
        action.lower()

        #forced exit
        if(action=='exit'):
            return -1
        if action not in game_content['sigma']:
            print('Wrong action input. Try again')
            continue

        #changing state
        next=gameTransition(game_content['delta'], state, action, stack)
        if next==-1:
            if action in ('w', 'a', 's', 'd'):  # movement hit a wall
                visuals.print_wall()
            continue
        
        state,stack=next
        top=stack[-1] if stack else 'epsilon'
            
        #if state is not defined in 'states' but mentioned in 'delta'
        if state not in game_content['states']:
            print('Invalid state.')
            continue

        #finish state
        if state in game_content['final']:
            if not game_content['gamma'] or top==game_content['gamma'][0]:
                result='good ending'
                visuals.print_ending(result, stack, game_content)
            else:
                result=1
                visuals.print_ending(result, stack, game_content)

    return result

def game(definition_file): 
    if not definition_file:
        return
    sections=parse.getSections(definition_file)
    #error
    if sections==-1:
        print('Syntax error')
        return
    
    game_content=gameCheck(sections)
    game_content=DPDA.dpdaGetContent(game_content) 
    game_content['delta']=genmap.generate_map(game_content, definition_file)

    #error 
    if not game_content:
        print("Sections are not defined correctly for the game.")
        return

    #start playing loop
    m=re.search(r'lvl(\d+)', definition_file)
    level=int(m.group(1)) if m else 1
    next_file=re.sub(r'lvl(\d+)\.txt', lambda x: f"lvl{int(x.group(1))+1}.txt", definition_file)
    is_last_level=not os.path.exists(next_file)

    result=playLVL(game_content, level)
    while result!='good ending':
        if result==-1:
            print('You broke the 4th wall and escaped.')
            return
        if result==1:
            if is_last_level:
                return
            print('Restarted the lvl')
        result=playLVL(game_content, level)

    game(next_level(definition_file))



def start_game():
    definition_file='game/levels/lvl1.txt'

    visuals.print_banner()
    game(definition_file)
    
start_game()