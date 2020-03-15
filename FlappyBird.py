import Environment
from obj import Bird,PillarManager

#create window/visuals/controls for the game
ENV = Environment.Environment(1280, 720, "Flappy bird")

#add the birds to the game.
bird = Bird.bird()
bird.debug= True
ENV.add_bird(bird)

#add the pillarManager
ENV.pillar_manager = PillarManager.PillarManager()

ENV.run()
