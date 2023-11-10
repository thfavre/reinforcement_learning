from neural_network import NeuralNetwork

default_layers_size = [4, 12, 4]

class Brain:
	def __init__(self, layers_size: list[int]=default_layers_size):
		self.neural_network = NeuralNetwork(layers_size)

	def update(self, posX, posY, goalPosX, goalPosY):
		outputs = self.neural_network.feed_forward([posX, posY, goalPosX, goalPosY])
		return outputs

	def mutate(self, mutation_rate: float):
		self.neural_network.mutate(mutation_rate)
