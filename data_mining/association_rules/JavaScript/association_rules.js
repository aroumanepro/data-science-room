const data = [
    ["Lait", "Moutarde"],
    ["Pain", "Oignons"],
    ["Steak", "Pain", "Oignons", "Moutarde"],
    ["Lait", "Oignons", "Moutarde"],
    ["Pain", "Oignons", "Moutarde"],
    ["Steak", "Pain", "Oignons", "Moutarde"],
  ];
  
  const threshold = 0.4;
  
  let uniqueValues = [];
  let newPairs = [];
  let newSets = [];
  
  let combinations = [];
  let combinationsSupport = [];
  
  const include = (firstArray, secondArray) =>
    firstArray.every((value) => secondArray.includes(value));
  
  const generateSets = (n) => {
    if (n === 0) {
      data.forEach((row) => {
        uniqueValues = [...new Set([...uniqueValues, ...row])];
      });
      uniqueValues = uniqueValues.filter((value) => {
        const count = data.filter((row) => row.includes(value)).length;
        return count / data.length >= threshold;
      });
      return uniqueValues;
    } else if (n === 1) {
      uniqueValues.forEach((value, i) => {
        uniqueValues.slice(i + 1).forEach((otherValue) => {
          const tempResult = [value, otherValue];
          const count = data.filter((row) => include(tempResult, row)).length;
          if (count / data.length > threshold) {
            combinations.push(tempResult);
            combinationsSupport.push(count / data.length);
            newPairs.push(tempResult);
          }
        });
      });
      return newPairs;
    } else {
      newPairs.forEach((pair, i) => {
        newPairs.slice(i + 1).forEach((otherPair) => {
          const firstArr = pair.slice(0, n - 1).join(" ");
          const secondArr = otherPair.slice(0, n - 1).join(" ");
          if (firstArr === secondArr) {
            const tempResult = [...new Set([...pair, ...otherPair])];
            const count = data.filter((row) => include(tempResult, row)).length;
            if (count / data.length > threshold) {
              combinations.push(tempResult);
              combinationsSupport.push(count / data.length);
              newSets.push(tempResult);
            }
          }
        });
      });
      newSets = newSets.filter((set, i) => {
        return !newSets
          .slice(i + 1)
          .some((otherSet) => set.toString() === otherSet.toString());
      });
      if (newSets.length !== 0) {
        return newSets;
      } else {
        return (Stop = 1);
      }
    }
  };
  
  let n = 0;
  let Stop = 0;
  
  do {
    generateSets(n);
    if (n >= 2) {
      newPairs = newSets;
      newSets = [];
    }
    n++;
  } while (Stop === 0);
  
  combinations.forEach((combination, i) => {
    combination.forEach((element, j) => {
      const otherElement = combination.filter((_, index) => index !== j);
      const otherCount = data.filter((row) => include(otherElement, row)).length;
      const elementCount = data.filter((row) => include([element], row)).length;
      const confidence = combinationsSupport[i] / (otherCount / data.length);
      const lift = confidence / (elementCount / data.length);
      if (confidence > threshold && lift > 1) {
        console.log(`Rule : { ${otherElement.join(", ")} } => { ${element} }`);
        console.log(`Confidence : ${confidence * 100}`);
        console.log(`Lift : ${lift}`);
        console.log(
          "Explanation: This rule implies that when you have [" +
            otherElement.join(", ") +
            "], there is a " +
            confidence * 100 +
            "% chance of having " +
            element +
            " as well, and this relationship is " +
            lift +
            " times stronger than expected by chance.",
        );
        console.log(
          "Explication: Cette règle suggère que lorsque vous avez [" +
            otherElement.join(", ") +
            "], il y a une chance de " +
            confidence * 100 +
            "% d'avoir également " +
            element +
            ", et cette relation est " +
            lift +
            " fois plus forte que ce qui serait attendu par hasard.",
        );
        console.log("\n");
      }
    });
  });
  