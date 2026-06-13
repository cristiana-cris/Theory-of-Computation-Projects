Automata implementations for 'Limbaje formale si automate'/Theory of computation course. I also added text-based game.

### Supported Models
* **DFA** (Deterministic Finite Automata)
* **NFA** (Nondeterministic Finite Automata)
* **DPDA** (Deterministic Pushdown Automata)
* **CFG** (Context-Free Grammar) – Generates strings based on defined production rules.

### How to Run the Automata
Each automaton resides in its own specific directory and relies on two simple text files:

1. **`definition.txt`**: Contains the formal definition of the automaton (states, alphabet, transition function, start state, and accept states).
2. **`in.txt`**: Contains the input strings you want to test.

**Output:** Running the script will process all strings from `in.txt` and clearly output which strings are **Accepted** or **Rejected** by the language.
<br/><br/>
<br/><br/>
### The Game: Eery Facility (DPDA-Driven Adventure)

This is text-based sci-fi survival game that shows how DPDA can be used in useful ways. **every room is a state**, and your inventory is managed entirely via the **Automaton Stack**. The stack dynamically tracks the items you pick up and validates whether you have the proper "keys" to transition into locked areas. Every playthrough is completely unique. Maps are procedurally generated on the fly using the `generate_random.py` script.

#### Story: 
The player is transported in a weird and futuristic facility, that emits dangerous radiations. It was used for all kind of experiments, and our goal is to find an exit as soon as possible. The most dangerous entity in this game are the walls, be wary of them.

### Level Breakdown & Win Conditions
The game features 3 distinct levels, each utilizing the stack mechanic differently:

| Level | Objective | Stack/DPDA Mechanic | Failure Penalty |
| :--- | :--- | :--- | :--- |
| **Level 1** | Navigate the eerie corridors and find the exit. | Basic state transitions to locate the exit. | Can't be failed |
| **Level 2** | The lights are dimming. Find a **Flashlight** to escape. | Stack pushes the Flashlight item; transition to exit requires Flashlight to pop. | Loop: You must replay Level 2 until you succeed. |
| **Level 3** | Find a **Key** to unlock a **Radiation Potion** to cleanse yourself. | The Key must be on the stack to "unlock" and push the Potion state. | **The Final Verdict:** Without the potion the power of the radiations kills you. |

