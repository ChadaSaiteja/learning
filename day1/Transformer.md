# Day 1

## Tokens

Tokens are the smallest units of data that a model processes (it can be word, char, phrases, image tokens (pixels), byte pair encoding). Tokenization helps in breaking large sentences into smaller units for learning patterns and relationships, which improves performance and accuracy.

### Key Concepts

- Simplification
- Standardization

## Parameters

Parameters are the variables that dictate how the model behaves and what results it produces. It is like a controller to get the required output. They are not set to default; they change during training to minimize the prediction error rate.

### Types of Parameters

**Weights**

Numeric values assigned to features of a model that determine the importance of making predictions.



**Biases**

Constant value added to the weighted sum to get the expected output from a neuron.

**Formula:**
```
z = wx + b
```



**Learning Rate**

It is a hyperparameter that controls how much weight and bias change during training.





**Activation Functions**

Determines how the input signal is converted into an output signal.

Common activation functions: sigmoid, ReLU



**Context Window**

Maximum amount of text (tokens) that a model can process without losing information to give the response.



**Temperature**

It controls randomness. It always lies between 0 to 2.

- temp = 0: More accurate/high probability
- temp = 2: More creative
- temp = 1: For balance



**Top K**

Takes the top K words with higher probability.

**Top P**

Considers words until the sum of all the words' probabilities match the threshold (e.g., 70%).



## Next-Token Prediction

LLMs do not generate sentences directly; they predict the next token based on probability using previous tokens.

**How does the model know the probability of a token?** This is where training comes in.

### During Training

- Model predicts next token
- Compare it with the real answer
- Adjust its weights
- Repeat billions of times

The above process teaches the model statistical patterns of language.

## Hallucinations

**Why Hallucinations Happen**

LLMs are trained to predict the next token based on probability, but whatever they generate may not be true or accurate. This happens for several reasons:

- **Confidence in Patterns**: The model learns statistical patterns from training data and generates text based on probability. Even if the information is incorrect, if it follows common patterns, the model will generate it confidently.

- **Lack of Ground Truth**: During training, the model only learns to predict the next token. It doesn't have access to real-world facts or verification mechanisms to confirm if the generated text is factually correct.

- **Training Data Limitations**: If the training data contains false or incomplete information, the model will learn and reproduce those inaccuracies.

- **Probabilistic Nature**: Since LLMs work on probability, they sometimes generate plausible-sounding text that follows the language pattern but may be completely fabricated.

- **No Real Understanding**: LLMs don't truly "understand" the meaning of words; they just predict what token should come next based on statistical patterns.
