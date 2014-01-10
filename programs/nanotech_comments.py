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

    # Print molecule name and which atom
    # is limiting how much # we can make.
    print name, "limited by", limiting

# Print atom name and count.
for name in sorted(counts):
    print name, counts[name]
