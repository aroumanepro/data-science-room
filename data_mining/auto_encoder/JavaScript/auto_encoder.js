// Fonction d'activation tanh
function tanh(x) {
    return Math.tanh(x);
  }
  
  // Dérivée de la fonction d'activation tanh
  function tanhPrime(x) {
    return 1 - Math.pow(tanh(x), 2);
  }
  
  // Initialisation des poids de manière aléatoire
  function initializeWeights(inputSize, hiddenSize, outputSize) {
    // Poids entre l'entrée et la couche cachée
    let weightsInputHidden = new Array(inputSize).fill().map(() =>
      new Array(hiddenSize).fill().map(() => Math.random() - 0.5)
    );
    // Poids entre la couche cachée et la sortie
    let weightsHiddenOutput = new Array(hiddenSize).fill().map(() =>
      new Array(outputSize).fill().map(() => Math.random() - 0.5)
    );
  
    return { weightsInputHidden, weightsHiddenOutput };
  }
  
  // Propagation avant pour obtenir les sorties cachées et les sorties finales
  function forwardPass(input, weights) {
    let hidden = weights.weightsInputHidden.map(h =>
      tanh(input.reduce((sum, inp, idx) => sum + inp * h[idx], 0))
    );
  
    let output = weights.weightsHiddenOutput.map(o =>
      tanh(hidden.reduce((sum, hid, idx) => sum + hid * o[idx], 0))
    );
  
    return { hidden, output };
  }
  
  // Calcul de l'erreur et de la dérivée
  function computeErrorAndGradient(target, output, hidden, weights) {
    let outputError = output.map((o, idx) => target[idx] - o);
    let outputGradient = outputError.map((e, idx) => e * tanhPrime(output[idx]));
  
    let hiddenError = weights.weightsHiddenOutput.map(h =>
      outputGradient.reduce((sum, og, ogIdx) => sum + og * h[ogIdx], 0)
    );
    let hiddenGradient = hiddenError.map((e, idx) => e * tanhPrime(hidden[idx]));
  
    return { outputError, outputGradient, hiddenError, hiddenGradient };
  }
  
  // Mise à jour des poids
  function updateWeights(weights, gradients, learningRate) {
    // Mise à jour des poids de la couche cachée vers la sortie
    for (let i = 0; i < weights.weightsHiddenOutput.length; i++) {
      for (let j = 0; j < weights.weightsHiddenOutput[i].length; j++) {
        weights.weightsHiddenOutput[i][j] += gradients.outputGradient[j] * learningRate;
      }
    }
  
    // Mise à jour des poids de l'entrée vers la couche cachée
    for (let i = 0; i < weights.weightsInputHidden.length; i++) {
      for (let j = 0; j < weights.weightsInputHidden[i].length; j++) {
        weights.weightsInputHidden[i][j] += gradients.hiddenGradient[j] * learningRate;
      }
    }
  
    return weights;
  }
  
  // Entraînement de l'auto-encodeur
  function trainAutoEncoder(input, target, inputSize, hiddenSize, outputSize, epochs, learningRate) {
    let weights = initializeWeights(inputSize, hiddenSize, outputSize);
  
    for (let epoch = 0; epoch < epochs; epoch++) {
      input.forEach((inp, index) => {
        // Propagation avant pour un élément d'entrée unique
        let { hidden, output } = forwardPass(inp, weights);
  
        // Cible correspondant à l'entrée courante
        let currentTarget = target[index];
  
        // Calcul de l'erreur et du gradient pour l'élément courant
        let gradients = computeErrorAndGradient(currentTarget, output, hidden, weights);
  
        // Mise à jour des poids
        weights = updateWeights(weights, gradients, learningRate);
      });
    }
  
    return weights;
  }
  
  // Données d'entraînement
  let input = [[0, 1], [1, 0], [1, 1], [0, 0]];
  let target = input; // Dans un auto-encodeur, la cible est la même que l'entrée
  let inputSize = 2;
  let hiddenSize = 2;
  let outputSize = 2;
  let epochs = 10000;
  let learningRate = 0.01;
  
  // Entraînement
  let trainedWeights = trainAutoEncoder(input, target, inputSize, hiddenSize, outputSize, epochs, learningRate);
  
  // Affichage des résultats après entraînement
  input.forEach(i => {
    let { output } = forwardPass(i, trainedWeights);
    console.log(`Input: ${i} Output: ${output.map(o => o.toFixed(2))}`); // Utilisation de toFixed(2) pour limiter le nombre de décimales
  });
  