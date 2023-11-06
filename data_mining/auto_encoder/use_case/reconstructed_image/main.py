from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from PIL import Image

# Charger l'image et la transformer en tableau numpy
image = Image.open('./input_image/image_path.jpeg')
# Choisissez une nouvelle résolution plus petite
img_resized = image.resize((256, 160))

# -1 pour aplatir l'image, 3 pour les canaux RGB
image_np = np.array(img_resized).reshape(-1, 3)

# Normaliser les valeurs des pixels
scaler = MinMaxScaler(feature_range=(-1, 1))
image_np_normalized = scaler.fit_transform(image_np)

# Données d'entraînement
X_train = image_np_normalized

# Dimension des couches cachées pour la compression
# Par exemple, pour une compression à 128 dimensions
hidden_layer_sizes = (128,)

# Création de l'auto-encodeur
auto_encoder = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes,
                            activation='tanh',
                            solver='adam',
                            learning_rate_init=0.01,
                            max_iter=10000)

# Entraînement de l'auto-encodeur
auto_encoder.fit(X_train, X_train)

# Prédiction (réconstruction)
X_predicted = auto_encoder.predict(X_train)

# Dénormaliser les valeurs des pixels
X_predicted = scaler.inverse_transform(X_predicted)

# Reconstituer l'image
reconstructed_image = X_predicted.reshape(
    img_resized.size[1], img_resized.size[0], 3)
reconstructed_image = np.clip(reconstructed_image, 0, 255).astype('uint8')
reconstructed_image = Image.fromarray(reconstructed_image)

# Créer l'image originale et la reconstitution
image.save('./output_image/original_image.png')
print("Image originale crée")
reconstructed_image.save('./output_image/reconstructed_image.png')
print("Image reconstitution crée")
