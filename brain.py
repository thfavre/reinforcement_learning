import test

layers_size = [4, 12, 4]

print(layers_size)

class Brain:
	def __init__(self):
		self.network = test.Network(layers_size)

	def update(self, posX, posY, goalPosX, goalPosY):
		outputs = self.network.feed_forward([posX, posY, goalPosX, goalPosY])
		return outputs

	def mutate(self, mutation_rate: float):
		self.network.mutate(mutation_rate)



# 4 8 4
# 4 16 4
# 4 8 8 4

# 4 8 8 4
# 4 20 20 4
# 4 50 4
# 4 6 6 6 6 4
