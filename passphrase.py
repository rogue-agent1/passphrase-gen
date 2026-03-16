#!/usr/bin/env python3
"""passphrase - Generate secure passphrases and passwords. Zero deps."""
import sys, os, random, string, math, hashlib

# EFF short wordlist (subset - 200 common words for offline use)
WORDS = [
    "acid","acme","aged","also","arch","area","army","atom","aunt","away",
    "axis","back","bail","bake","band","bank","barn","base","bath","bead",
    "beam","bean","bear","beat","beef","been","bell","belt","bend","best",
    "bike","bird","bite","blow","blue","blur","boat","body","bold","bolt",
    "bomb","bond","bone","book","boot","born","boss","both","bowl","bulk",
    "burn","busy","buzz","cafe","cage","cake","calm","came","camp","cape",
    "card","care","cart","case","cash","cast","cave","chef","chin","chip",
    "chop","city","clad","clan","clap","clay","clip","club","clue","coal",
    "coat","code","coin","cold","come","cook","cool","cope","copy","cord",
    "core","cork","corn","cost","cozy","crew","crop","crow","cube","cult",
    "curb","cure","curl","cute","dare","dark","dart","dash","data","dawn",
    "dead","deaf","deal","dear","debt","deck","deed","deem","deep","deer",
    "demo","deny","desk","dial","dice","diet","dine","dip","dire","dirt",
    "disc","dish","dock","dome","done","door","dose","dove","down","drab",
    "drag","drip","drop","drum","dusk","dust","duty","each","earl","earn",
    "ease","east","easy","echo","edge","edit","else","emit","envy","epic",
    "euro","even","ever","evil","exam","exec","exit","expo","face","fact",
    "fade","fail","fair","fake","fall","fame","fang","fare","farm","fast",
    "fate","fawn","fear","feed","feel","feet","fell","felt","fend","fern",
    "fest","file","fill","film","find","fine","fire","firm","fish","fist",
]

def gen_passphrase(words=4, sep="-", capitalize=False):
    selected = [random.choice(WORDS) for _ in range(words)]
    if capitalize: selected = [w.capitalize() for w in selected]
    entropy = math.log2(len(WORDS)) * words
    return sep.join(selected), entropy

def gen_password(length=16, exclude=""):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    chars = "".join(c for c in chars if c not in exclude)
    pwd = "".join(random.choice(chars) for _ in range(length))
    entropy = math.log2(len(chars)) * length
    return pwd, entropy

def gen_pin(length=6):
    pin = "".join(str(random.randint(0,9)) for _ in range(length))
    entropy = math.log2(10) * length
    return pin, entropy

def strength(entropy):
    if entropy >= 80: return "🟢 Very Strong"
    if entropy >= 60: return "🟢 Strong"
    if entropy >= 40: return "🟡 Moderate"
    if entropy >= 28: return "🟠 Weak"
    return "🔴 Very Weak"

def cmd_phrase(args):
    words = 4; sep = "-"; cap = "--cap" in args
    for i, a in enumerate(args):
        if a in ("-w","--words") and i+1 < len(args): words = int(args[i+1])
        if a in ("-s","--sep") and i+1 < len(args): sep = args[i+1]
    count = 1
    for i, a in enumerate(args):
        if a in ("-n","--count") and i+1 < len(args): count = int(args[i+1])
    
    for _ in range(count):
        phrase, entropy = gen_passphrase(words, sep, cap)
        print(f"  {phrase}")
    print(f"\n  Entropy: {entropy:.0f} bits — {strength(entropy)}")

def cmd_password(args):
    length = 16
    for i, a in enumerate(args):
        if a in ("-l","--length") and i+1 < len(args): length = int(args[i+1])
    count = 1
    for i, a in enumerate(args):
        if a in ("-n","--count") and i+1 < len(args): count = int(args[i+1])
    
    for _ in range(count):
        pwd, entropy = gen_password(length)
        print(f"  {pwd}")
    print(f"\n  Entropy: {entropy:.0f} bits — {strength(entropy)}")

def cmd_pin(args):
    length = 6
    for i, a in enumerate(args):
        if a in ("-l","--length") and i+1 < len(args): length = int(args[i+1])
    pin, entropy = gen_pin(length)
    print(f"  {pin}")
    print(f"\n  Entropy: {entropy:.0f} bits — {strength(entropy)}")

def cmd_check(args):
    if not args: print("Usage: passphrase check <password>"); sys.exit(1)
    pwd = args[0]
    checks = {"length ≥ 8": len(pwd) >= 8, "uppercase": any(c.isupper() for c in pwd),
              "lowercase": any(c.islower() for c in pwd), "digit": any(c.isdigit() for c in pwd),
              "special": any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in pwd),
              "length ≥ 12": len(pwd) >= 12, "length ≥ 16": len(pwd) >= 16}
    score = sum(checks.values())
    print(f"🔍 Password Analysis\n")
    for name, ok in checks.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    
    # Rough entropy estimate
    charset = 0
    if any(c.islower() for c in pwd): charset += 26
    if any(c.isupper() for c in pwd): charset += 26
    if any(c.isdigit() for c in pwd): charset += 10
    if any(not c.isalnum() for c in pwd): charset += 32
    entropy = math.log2(charset) * len(pwd) if charset else 0
    print(f"\n  Entropy: ~{entropy:.0f} bits — {strength(entropy)}")

CMDS = {"phrase":cmd_phrase,"p":cmd_phrase,"password":cmd_password,"pw":cmd_password,
        "pin":cmd_pin,"check":cmd_check}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h","--help"):
        print("passphrase - Generate secure passphrases and passwords")
        print("Commands: phrase, password, pin, check")
        print("  phrase [-w 4] [-s '-'] [--cap] [-n 3]")
        print("  password [-l 16] [-n 3]")
        print("  pin [-l 6]")
        print("  check <password>")
        sys.exit(0)
    cmd = args[0]
    if cmd not in CMDS: print(f"Unknown: {cmd}"); sys.exit(1)
    CMDS[cmd](args[1:])
