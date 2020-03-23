import random
import math
import copy
from obj import Bird

class EvolutionManager:
    def __init__(self, population=20, mutation=5):
        
        self.debug = False
        self.population_amount = population
        self.mutation_rate = mutation
        self.population = self.create_population(self.population_amount)
        self.dead_population = []
        self.generation = 0
        self.best_alltime_fitness = 0
        self.best_fitness = 0
        self.worst_fitness = 0

    def create_population(self, amount):
        temp_lst = []
        for i in range(amount):
            #create new bird
            bird = Bird.bird(150,random.randint(200,600))
            bird.debug=self.debug
            bird.mutation_rate = self.mutation_rate
            bird.color= (random.randint(10,255),random.randint(10,255),random.randint(10,255))
            #get amount of hidden nodes
            hidden = random.randint(1,16)
            bird.create_neural_network(hidden)
            #append to list
            temp_lst.append(bird)
        return temp_lst

    def new_generation(self):
        lst_fitness, total_fitness = self.calculate_fitness()
        self.generation += 1 
        self.make_babies(lst_fitness, total_fitness)
        print("Generation: "+str(self.generation)+" avg fitness: "+str(total_fitness/self.population_amount)+ " Alltime best: "+str(self.best_alltime_fitness)+" best: "+str(self.best_fitness)+" worst: " + str(self.worst_fitness))

    def calculate_fitness(self):
        total_fitness = 0
        best_fit = 0
        for bird in self.dead_population:
            total_fitness+=bird.fitness
        sorted_by_fitness = sorted(self.dead_population ,key= lambda bird: bird.fitness)
        return (sorted_by_fitness, total_fitness)

    def make_babies(self, lst_fitness, total_fitness):
        if total_fitness > 0: 
            lst_survivors = []
            lst_babies = []
            best_bird = lst_fitness[-1]
            worst_bird = lst_fitness[0]
            self.best_fitness = best_bird.fitness
            self.worst_fitness = worst_bird.fitness
            if self.best_fitness > self.best_alltime_fitness:
                self.best_alltime_fitness = self.best_fitness

            """
            lst_survivors.append(self.create_new_bird(best_bird))
            lst_babies.append(self.create_new_bird(best_bird))

            for i in range((math.floor(self.population_amount/2))-1):
                amount = random.randint(0,math.floor(total_fitness))
                choice = self.get_choice(lst_fitness,amount)
                #lst_survivors.append(copy.deepcopy(choice))
                #lst_babies.append(copy.deepcopy(choice))
                

                lst_survivors.append(self.create_new_bird(choice))
                lst_babies.append(self.create_new_bird(choice))
            """ 
            for i in range(math.floor(self.population_amount/2),self.population_amount):
                lst_survivors.append(self.create_new_bird(self.dead_population[i]))
                lst_babies.append(self.create_new_bird(self.dead_population[i]))
            lst_mutated_babies = self.crazy_mutation(lst_babies)
            final_lst = lst_survivors+lst_mutated_babies
            self.population = final_lst
            self.dead_population = []
            
            
            

        else:
            self.population = self.create_population(self.population_amount)
            self.dead_population = []
            self.generation = 0

    def crazy_mutation(self,lst):
        temp_lst = []
        for y in lst:
            x = copy.deepcopy(y)
            x.mutate_neural_network()
            temp_lst.append(x)
        return temp_lst


    def get_population(self):
        return self.population

    def add_dead(self,b):
        self.dead_population.append(b)
        self.population.remove(b)
    
    def is_population_dead(self):
        return (len(self.population)<=0)

    
    def get_choice(self, lst, amount):
        found = False
        counter = 0
        c_amount = 0
        while found:
            c_amount += lst[counter].fitness
            if amount <= c_amount:
                found = True
            else:
                counter+=1
        
        return lst[counter]


    def create_new_bird(self, p):
        bird = Bird.bird(150, random.randint(390,410), True, True, p.get_nn())
        bird.color = p.color
        bird.debug= self.debug
        bird.mutation_rate = self.mutation_rate
        return bird