inventory = { "He": 1, "H": 4, "O": 3 }
formulas = {
    "water": { "H": 2, "O": 1 },
    "helium": { "He": 1 },
    "hydrogen": { "H": 2 }
}

counts = {}
for name, molecule in formulas.iteritems():
    number = None
    for atom in molecule:
        required = molecule[atom]
        available = inventory.get(atom, 0)
        limit = available / required
    if (number is None) or (limit < number):
        number = limit
    counts[name] = number

for name in sorted(counts):
    print name, counts[name]
