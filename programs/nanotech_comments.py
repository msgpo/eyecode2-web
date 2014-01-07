# Our inventory of atoms and the kinds
# of molecules we can make.
inventory = { "He": 1, "H": 4, "O": 3 }
formulas = {
    "water": { "H": 2, "O": 1 },
    "helium": { "He": 1 },
    "hydrogen": { "H": 2 }
}

# Determine how many molecules we can
# make of each kind.
counts = {}
for name, molecule in formulas.iteritems():
    number = None
    limit = 0
    for atom in molecule:
        required = molecule[atom]
        available = inventory.get(atom, 0)
        limit = available / required
    if (number is None) or (limit < number):
        number = limit
    counts[name] = number

# Print atom name and count.
for name in sorted(counts):
    print name, counts[name]
