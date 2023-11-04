# flake8: noqa

# Définir la fonction include pour vérifier si tous les éléments de firstArray sont dans secondArray
def include(firstArray, secondArray):
    return all(value in secondArray for value in firstArray)

# Définir la fonction generate_sets pour trouver des valeurs uniques et créer des ensembles basés sur le seuil


def generate_sets(data, threshold):
    # Liste plate de tous les éléments
    flat_list = [item for sublist in data for item in sublist]
    unique_values = list(set(flat_list))  # Éléments uniques
    unique_values = [value for value in unique_values if flat_list.count(
        # Filtrer les valeurs uniques en fonction du seuil
        value) / len(data) >= threshold]
    return unique_values

# Fonction pour trouver des combinaisons de la taille suivante


def find_combinations(source, n, data, threshold):
    results = []
    for i in range(len(source)):
        for j in range(i + 1, len(source)):
            combined = list(set(source[i] + source[j]))
            if len(combined) == n + 1:
                count = sum(include(combined, row) for row in data)
                if count / len(data) >= threshold:
                    results.append(combined)
    return results

# Fonction pour déterminer si une règle est unique


def is_unique(rule, unique_rules):
    return not any(rule == unique_rule for unique_rule in unique_rules)

# Fonction pour filtrer des règles uniques


def filter_unique_rules(rules):
    unique_rules = []
    for rule in rules:
        if is_unique(rule, unique_rules):
            unique_rules.append(rule)
    return unique_rules


# Les données initiales et le seuil
data = [
    ['Lait', 'Moutarde'],
    ['Pain', 'Oignons'],
    ['Steak', 'Pain', 'Oignons', 'Moutarde'],
    ['Lait', 'Oignons', 'Moutarde'],
    ['Pain', 'Oignons', 'Moutarde'],
    ['Steak', 'Pain', 'Oignons', 'Moutarde']
]
threshold = 0.4

# Générer les valeurs uniques initiales
unique_values = generate_sets(data, threshold)
# Commencer avec des éléments uniques comme premier ensemble de combinaisons
combinations = [[value] for value in unique_values]

# Générer des combinaisons de longueur croissante
n = 1
while True:
    new_combinations = find_combinations(combinations, n, data, threshold)
    if not new_combinations:
        break
    combinations += new_combinations
    n += 1

# Calculer le support pour les combinaisons
combinations_support = [sum(include(combo, row)
                            for row in data) / len(data) for combo in combinations]

# Définir une fonction pour calculer la confiance et le lift


def calculate_confidence_and_lift(combination, combinations_support, data, threshold):
    rules = []
    for i, combo in enumerate(combination):
        for element in combo:
            other_elements = [x for x in combo if x != element]
            other_count = sum(include(other_elements, row) for row in data)
            element_count = sum(include([element], row) for row in data)
            confidence = combinations_support[i] / (other_count / len(data))
            lift = confidence / (element_count / len(data))
            if confidence > threshold and lift > 1:
                rules.append({'base': other_elements, 'add': element,
                             'confidence': confidence, 'lift': lift})
    return rules


# Calculer et collecter toutes les règles avec confiance et lift
all_rules = calculate_confidence_and_lift(
    combinations, combinations_support, data, threshold)

# Filtrer les règles uniques
unique_rules = filter_unique_rules(all_rules)

# Imprimer les règles uniques
for rule in unique_rules:
    print(f"Règle: {rule['base']} => {rule['add']}")
    print(f"Confiance: {rule['confidence'] * 100:.2f}%")
    print(f"Lift: {rule['lift']:.2f}")
    print(f"Explanation: This rule implies that when you have {rule['base']} => {rule['add']}, there is a { rule['confidence'] * 100:.2f}% chance of having {rule['add']} as well, and this relationship is {rule['lift']:.2f} times stronger than expected by chance.'")
    print(f"Explication: Cette règle suggère que lorsque vous avez {rule['base']} => {rule['add']}, il y a une chance de {rule['confidence'] * 100:.2f}% d'avoir également {rule['add']}, et cette relation est {rule['lift']:.2f} fois plus forte que ce qui serait attendu par hasard.")
    print()
