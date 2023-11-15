# reinforcement_learning
Reinforcement learning made from scratch to play games in Python

# Resources
- [Neural network](https://www.youtube.com/watch?v=aircAruvnKk)
- [Reinforcement Learning in 10 min](https://www.youtube.com/watch?v=vXtfdGphr3c)
- [Weight initialization](https://machinelearningmastery.com/weight-initialization-for-deep-learning-neural-networks/)

# Results Examples

<details>
  <summary><b>1) Simple Neural Network</b></summary>

The objective is to guide squares towards a circle.

https://github.com/thfavre/reinforcement_learning/assets/67341005/021a0a3d-1de3-4f64-9a93-83011b33acfb

- **Input Neurons:** 4 neurons representing square's X and Y positions, and circle's X and Y positions.
- **Hidden Layer:** 1 layer with 12 neurons to process the input data.
- **Output Neurons:** 4 neurons representing movement directions (UP, RIGHT, LEFT, DOWN) for the squares.
- **Population size:** 1000
</details>


<details>
  <summary><b>2) +Velocity +Checkpoints</b></summary>

Checkpoints and velocity have been integrated into the neural network architecture to enhance its learning capabilities.

https://github.com/thfavre/reinforcement_learning/assets/67341005/9b75bdfe-8d08-4e93-b09a-6d5490ad6801

- **Input Neurons:** 8 neurons (posX, posY, goalPosX, goalPosY, velocityX, velocityY, nextGoalPosX, nextGoalPosY)
- **Hidden Layer:** 1 layer with 12 neurons
- **Output Neurons:** 4 neurons (UP, RIGHT, LEFT, DOWN)
- **Population size:** 500
</details>
