import Environment
from obj import Bird,PillarManager, EvolutionManager
import os

os.system('cls')
#create window/visuals/controls for the game
ENV = Environment.Environment(1280, 720, "Flappy bird")

#add the birds to the game.
ENV.evolution_manager = EvolutionManager.EvolutionManager(500,15)
ENV.lst_birds = ENV.evolution_manager.get_population()

#add the pillarManager
ENV.pillar_manager = PillarManager.PillarManager()

ENV.run()
