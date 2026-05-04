import sys
import os
# Adds the parent directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parse
import DPDA

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

    #end of map
    else:
        #make it random
        print("A wall challenges you to a staring contest.")
        #sleep/ make the dots slowly appear
        print("...")
        print("Somehow, he manages to win :/")
    return -1

def game(sections):
    dpda_content=DPDA.dpdaGetContent(sections) 
    #error 
    if dpda_content==-1:
        print("Sections are not defined correctly for the game.")
        return

    result = 0
    stack=[]
    state=dpda_content['start']

    while not result:
        print()
        print(f'You are at the {state}. Where do you want to go next?')
        action=input().strip()

        #forced exit
        if(action=='exit'):
            result=1
            continue
        if action not in dpda_content['sigma']:
            print('Wrong action input. Try again')
            continue
        #changing state
        next=gameTransition(dpda_content['delta'], state, action, stack)
        if next==-1:
            continue
        state,stack=next
        top=stack[-1] if stack else 'epsilon'
            
        #if state is not defined in 'states' but mentioned in 'delta'
        if state not in dpda_content['states']:
            print('Invalid state.')
            continue

        if state in dpda_content['final']:
            if top=='potion':
                print('You got the good ending. Congratulations!')
            else:
                print('Bad ending. Next time try to get the potion!')
            result=1        

def start_game():
    print("Write path for the file with the definition: ")
    definition_file=input()

    sections=parse.getSections(definition_file)
    if sections == -1:
        print('Syntax error')
        return
    
    print("In this game you can pick up items and use wasd to move between rooms. Type 'exit' to exit the game.")
    game(sections)
    
start_game()