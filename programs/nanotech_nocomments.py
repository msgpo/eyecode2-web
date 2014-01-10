inventory = { "He": 1, "H": 4, "O": 3 }
formulas = {
    "water": { "H": 2, "O": 1 },
    "helium": { "He": 1 },
    "hydrogen": { "H": 2 }
}

counts = {}
for name in sorted(formulas):
    molecule = formulas[name]
    number = None
    limiting = None
    for atom in molecule:
        required = molecule[atom]
        available = inventory.get(atom, 0)
        limit = available / required
        if (number is None) or (limit < number):
            number = limit
            limiting = atom
    counts[name] = number
    print name, "limited by", limiting

for name in sorted(counts):
    print name, counts[name]
