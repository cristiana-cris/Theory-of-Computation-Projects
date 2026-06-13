import os
import random

# ── ANSI colour helpers ────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    GRAY    = "\033[90m"
    WHITE   = "\033[97m"

def c(color, text):
    return f"{color}{text}{C.RESET}"

# ── Room flavour text ──────────────────────────────────────────────────────────
ROOM_LORE = {
    "entrance":  "Cracked green tiles, flickering emergency lights. The air smells of ozone.",
    "lab":       "Strange potions are surrouding you. The walls seem to curve and move like they are fluid. Some experiment has definetly gone wrong.",
    "library":   "Data-slates scattered across the floor. One terminal still pulses faintly.",
    "workshop":  "Burnt circuitry and soldering fumes. Something exploded here recently.",
    "garden":    "Overgrown hydroponic bays. Pale bioluminescent moss clings to the pipes. Even this little piece of 'nature' is not free from the concrete.",
    "finish":    "The emergency exit. Cold air bleeds through the seal. Freedom.",
    "start":     "You wake up on the floor. Something has gone very wrong. The walls seem to get closer and closer to you.",
}

ROOM_ICONS = {
    "entrance":  "▶",
    "lab":       "⚗",
    "library":   "◈",
    "workshop":  "⚙",
    "garden":    "❧",
    "finish":    "◎",
    "start":     "◎",
}

ITEM_ICONS = {
    "key":    "🔑",
    "potion": "⚗ ",
    "torch":  "🕯 ",
}

# ── Exits derived from delta ───────────────────────────────────────────────────
DIRECTION_LABELS = {
    "w": "north",
    "s": "south",
    "a": "west",
    "d": "east",
}

# ── Inventory bar ──────────────────────────────────────────────────────────────
def print_inventory(stack, gamma):
    width = 46
    print(c(C.GRAY, "  ┌" + "─" * width + "┐"))
    print(c(C.GRAY, "  │ ") + c(C.MAGENTA, "PACK") + c(C.GRAY, " " * (width - 4) + "│"))

    if not stack:
        print(c(C.GRAY, "  │  ") + c(C.DIM, "(nothing carried)") + c(C.GRAY, " " * (width - 18) + "│"))
    else:
        needed = gamma[0] if gamma else None
        for item in stack:
            icon = ITEM_ICONS.get(item, "◆ ")
            if item == needed:
                tag = c(C.GREEN, f"{icon}{item}") + c(C.GRAY, " ← needed")
                pad = width - 3 - len(item) - 11
            else:
                tag = c(C.YELLOW, f"{icon}{item}")
                pad = width - 3 - len(item) - 2
            print(c(C.GRAY, "  │  ") + tag + c(C.GRAY, " " * max(pad, 0) + "│"))

    print(c(C.GRAY, "  └" + "─" * width + "┘"))

# ── Room display ───────────────────────────────────────────────────────────────
def print_room(state, game_content, stack, level=1):
    _clear()

    # Header
    print(c(C.GRAY, f"  ── ABANDONED LABS · level {level} " + "─" * 21))
    print()

    # Room name + lore
    icon = ROOM_ICONS.get(state, "○")
    lore = ROOM_LORE.get(state, "A nondescript room. Something feels off.")
    print(c(C.CYAN, f"  {icon}  ") + c(C.BOLD + C.WHITE, state.upper()))
    print(c(C.DIM,  f"     {lore}"))
    print()

    print()

    # Inventory
    print_inventory(stack, game_content.get('gamma', []))
    print()

    # Prompt
    print(c(C.GRAY, "  ─" * 24))
    print(c(C.GRAY, "  ❯ "), end="", flush=True)

# ── Banner (call once at game start) ──────────────────────────────────────────
def print_banner():
    _clear()
    print()
    print(c(C.CYAN,  "  ╔══════════════════════════════════════════════╗"))
    print(c(C.CYAN,  "  ║") + c(C.BOLD + C.WHITE, "        A B A N D O N E D   L A B S          ") + c(C.CYAN, "║"))
    print(c(C.CYAN,  "  ║") + c(C.DIM,            "        sector 7 · containment failed         ") + c(C.CYAN, "║"))
    print(c(C.CYAN,  "  ╚══════════════════════════════════════════════╝"))
    print()
    print(c(C.GRAY,  "  wasd to move  ·  pick to grab  ·  exit to quit"))
    print()
    input(c(C.DIM,   "  [ press enter to begin ]"))

# ── Ending screens ─────────────────────────────────────────────────────────────
def print_ending(result, stack, game_content):
    _clear()
    print()
    if result == 'good ending':
        print(c(C.GREEN,  "  ✦━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✦"))
        print(c(C.GREEN,  "  ✦") + c(C.BOLD + C.WHITE, "         E S C A P E D  —  G O O D  E N D   ") + c(C.GREEN, "✦"))
        print(c(C.GREEN,  "  ✦━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✦"))
        print()
        print(c(C.DIM, "  You slipped through the emergency exit, the vial clutched"))
        print(c(C.DIM, "  tightly in your fist. The lab collapses behind you."))
    else:
        needed = game_content.get('gamma', ['???'])[0]
        print(c(C.RED,    "  ✗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✗"))
        print(c(C.RED,    "  ✗") + c(C.BOLD + C.WHITE, "             B A D   E N D I N G             ") + c(C.RED, "✗"))
        print(c(C.RED,    "  ✗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✗"))
        print()
        print(c(C.DIM, f"  You escaped — but without the ") + c(C.YELLOW, needed) + c(C.DIM, "."))
        print(c(C.DIM,  "  Whatever was in that vial, someone else has it now."))
        print()
        print(c(C.GRAY, "  Restarting..."))
        print()
        input(c(C.DIM, "  [ press enter to try again ]"))
    print()

# ── Wall / dead end messages ───────────────────────────────────────────────────
def print_wall():
    import time
    nr = random.choice([1, 2, 3])
    if nr == 1:
        print(c(C.DIM, "  A wall challenges you to a staring contest."), end="", flush=True)
        for _ in range(3):
            time.sleep(2)
            print(c(C.DIM, "."), end="", flush=True)
        print(c(C.GRAY, "\n  Somehow, he manages to win :/"))
    elif nr == 2:
        print(c(C.GRAY, "  You have stumbled into a wall. Be more carefull, you might upset them!"))
    else:
        print(c(C.GRAY, "  Dead end."))
    input(c(C.DIM, "  [ press enter to continue ]"))

# ── Level transition ───────────────────────────────────────────────────────────
def print_level_transition(next_file):
    import re as _re
    m = _re.search(r'lvl(\d+)', next_file)
    next_lvl = m.group(1) if m else '?'
    print()
    print(c(C.CYAN,  "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
    print(c(C.WHITE, "  ▶  Sector cleared. Proceeding deeper..."))
    print(c(C.GRAY,  f"     Entering level {next_lvl}"))
    print(c(C.CYAN,  "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
    print()
    input(c(C.DIM,   "  [ press enter to continue ]"))

def print_game_complete():
    _clear()
    print()
    print(c(C.MAGENTA, "  ★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★"))
    print(c(C.MAGENTA, "  ★") + c(C.BOLD + C.WHITE, "      Y O U   B E A T   T H E   G A M E     ") + c(C.MAGENTA, "★"))
    print(c(C.MAGENTA, "  ★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★"))
    print()
    print(c(C.DIM, "  The facility is behind you. Whatever happened here,"))
    print(c(C.DIM, "  you survived it. The world outside waits."))
    print()

# ── Internal helpers ───────────────────────────────────────────────────────────
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')