# flake8: noqa
from sklearn.neural_network import MLPRegressor
import numpy as np

# Données d'entraînement
X_train = np.array([[0, 1], [1, 0], [1, 1], [0, 0]])

# Création de l'auto-encodeur
auto_encoder = MLPRegressor(hidden_layer_sizes=(2,),
                            activation='tanh',
                            solver='adam',
                            learning_rate_init=0.01,
                            max_iter=10000)

# Entraînement de l'auto-encodeur
auto_encoder.fit(X_train, X_train)

# Prédiction (réconstruction)
X_predicted = auto_encoder.predict(X_train)

# Affichage des résultats
for i, x in enumerate(X_train):
    print(f"Input: {x}, Predicted: {X_predicted[i]}")
