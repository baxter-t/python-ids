import csv

# with open('NUSW-NB15_features.csv') as features:
#     reader = csv.reader(features, delimiter=',')
#     types = {}
#     for line in reader:
#         types[line[2]] = types.get(line[2], []) + [line[1]]


nominalValues = {}


with open("UNSW_NB15_testing-set.csv") as trainingSet:

    reader = csv.DictReader(trainingSet, delimiter=",")
    counter = 0

    for line in reader:
        for field in line:
            try:
                float(line[field])
            except ValueError:
                if nominalValues.get(field) == None:
                    nominalValues[field] = set()

                nominalValues[field].add(line[field])

        counter += 1
        if counter % 100 == 0:
            print("{}: {}".format(counter, nominalValues.keys()))

with open("UNSW_NB15_training-set.csv") as trainingSet:

    reader = csv.DictReader(trainingSet, delimiter=",")
    counter = 0

    for line in reader:
        for field in line:
            try:
                float(line[field])
            except ValueError:
                if nominalValues.get(field) == None:
                    nominalValues[field] = set()

                nominalValues[field].add(line[field])

        counter += 1
        if counter % 100 == 0:
            print("{}: {}".format(counter, nominalValues.keys()))


for n in nominalValues:
    nominalValues[n] = sorted(list(nominalValues[n]))

print(nominalValues)

print("< || Mappings Used || >")
print()
for m in nominalValues:
    print("Mapping for field: {}".format(m))
    for i, x in enumerate(nominalValues[m]):
        print("    {} -> {}".format(i, x))
    print()
