import math
import numpy as np

# activation functions
def sigmoid(x): # value between 0 and 1
	return 1 / (1 + math.exp(-x))

def relu(x): # value of 0 or x (should use the He initialization)
	return max(0, x)

# initialization functions
def xavier_initialization(current_layer_size: int, next_layer_size: int) -> np.ndarray:
	return np.random.randn(next_layer_size, current_layer_size) / np.sqrt(current_layer_size)

def normalized_xavier_initialization(current_layer_size: int, next_layer_size: int) -> np.ndarray:
	return np.random.randn(next_layer_size, current_layer_size) * np.sqrt(6.0 / (current_layer_size + next_layer_size))

def he_initialization(current_layer_size: int, next_layer_size: int) -> np.ndarray: # TODO check if it's correct
	return np.random.randn(next_layer_size, current_layer_size) * np.sqrt(2.0 / current_layer_size)


class NeuralLayer:

	def __init__(self):
		self.weights = []

	def set_weights(self, weights: np.ndarray):
		self.weights = weights

	def activation(self, x: float) -> float:
		return sigmoid(x)

	def feed_forward(self, inputs: list[float]) -> list[float]:
		outputs = []
		for i in range(len(self.weights)):
			outputs.append(self.activation(np.dot(self.weights[i], inputs)))
		return outputs

	def mutate(self, mutation_rate: float):
		for i in range(len(self.weights)):
			for j in range(len(self.weights[i])):
				if np.random.rand() < mutation_rate:
					self.weights[i][j] += np.random.rand() * 2 - 1



class Network:
	def __init__(self, layersSize: list[int]) -> None:
		self.layers = self.create_neural_layers(layersSize)

	def create_neural_layers(self, layersSize: list[int]) -> list[NeuralLayer]:
		layers = []
		for i in range(len(layersSize) - 1):
			layer = NeuralLayer()
			layer.set_weights(normalized_xavier_initialization(layersSize[i], layersSize[i+1]))
			layers.append(layer)
		return layers

	def feed_forward(self, inputs: list[float]) -> list[float]:
		for i in range(len(self.layers)):
			inputs = self.layers[i].feed_forward(inputs)
		return inputs

	def mutate(self, mutation_rate: float):
		for i in range(len(self.layers)):
			self.layers[i].mutate(mutation_rate)

