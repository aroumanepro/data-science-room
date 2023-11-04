# flake8: noqa
import random
import math

# Fonction d'activation tanh
def tanh(x):
    return math.tanh(x)

# Dérivée de la fonction d'activation tanh
def tanh_prime(x):
    return 1 - math.tanh(x)**2

# Initialisation des poids de manière aléatoire
def initialize_weights(input_size, hidden_size, output_size):
    weights_input_hidden = [[random.random() - 0.5 for _ in range(hidden_size)] for _ in range(input_size)]
    weights_hidden_output = [[random.random() - 0.5 for _ in range(output_size)] for _ in range(hidden_size)]
    return weights_input_hidden, weights_hidden_output

# Propagation avant pour obtenir les sorties cachées et les sorties finales
def forward_pass(input, weights_input_hidden, weights_hidden_output):
    hidden = [tanh(sum(i * w for i, w in zip(input, weights))) for weights in weights_input_hidden]
    output = [tanh(sum(h * w for h, w in zip(hidden, weights))) for weights in weights_hidden_output]
    return hidden, output

# Calcul de l'erreur et de la dérivée
def compute_error_and_gradient(target, output, hidden, weights_hidden_output):
    output_error = [t - o for t, o in zip(target, output)]
    output_gradient = [e * tanh_prime(o) for e, o in zip(output_error, output)]

    hidden_error = [sum(og * w for og, w in zip(output_gradient, col)) for col in zip(*weights_hidden_output)]
    hidden_gradient = [e * tanh_prime(h) for e, h in zip(hidden_error, hidden)]

    return output_error, output_gradient, hidden_error, hidden_gradient

# Mise à jour des poids
def update_weights(weights_input_hidden, weights_hidden_output, input, hidden, output_gradient, hidden_gradient, learning_rate):
    for i, (wg, h) in enumerate(zip(output_gradient, hidden)):
        for j in range(len(weights_hidden_output[i])):
            weights_hidden_output[i][j] += wg * h * learning_rate

    for i, (hg, inp) in enumerate(zip(hidden_gradient, input)):
        for j in range(len(weights_input_hidden[i])):
            weights_input_hidden[i][j] += hg * inp * learning_rate

    return weights_input_hidden, weights_hidden_output

# Entraînement de l'auto-encodeur
def train_auto_encoder(input, target, input_size, hidden_size, output_size, epochs, learning_rate):
    weights_input_hidden, weights_hidden_output = initialize_weights(input_size, hidden_size, output_size)

    for epoch in range(epochs):
        for inp, tar in zip(input, target):
            hidden, output = forward_pass(inp, weights_input_hidden, weights_hidden_output)
            output_error, output_gradient, hidden_error, hidden_gradient = compute_error_and_gradient(tar, output, hidden, weights_hidden_output)
            weights_input_hidden, weights_hidden_output = update_weights(weights_input_hidden, weights_hidden_output, inp, hidden, output_gradient, hidden_gradient, learning_rate)

    return weights_input_hidden, weights_hidden_output

# Données d'entraînement
input = [[0, 1], [1, 0], [1, 1], [0, 0]]
target = input  # Dans un auto-encodeur, la cible est la même que l'entrée
input_size = 2
hidden_size = 2
output_size = 2
epochs = 10000
learning_rate = 0.01

# Entraînement
weights_input_hidden, weights_hidden_output = train_auto_encoder(input, target, input_size, hidden_size, output_size, epochs, learning_rate)

# Affichage des résultats après entraînement
for i in input:
    _, output = forward_pass(i, weights_input_hidden, weights_hidden_output)
    print(f"Input: {i} Output: {[round(o, 2) for o in output]}")
