import numpy as np
import random
import copy


#neural network class made by Naomi <3 (based on codetrain's videos)
def sigmoid(z):
    return 1/(1+np.exp(-z))
def de_sigmoid(z):
    return z * (1 - z)



def translate_random(n):
    return (n*2)-1

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        
        
        #amount of nodes.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        #make Matrix arrays for the weights and put random values in it.
        self.weights_ih = np.random.rand(self.hidden_nodes, self.input_nodes)
        self.weights_ih = translate_random(self.weights_ih)
        self.weights_ho = np.random.rand(self.output_nodes, self.hidden_nodes)
        self.weights_ho = translate_random(self.weights_ho)

        #create biases
        self.bias_h = np.random.rand(self.hidden_nodes, 1)
        self.bias_h = translate_random(self.bias_h)
        self.bias_o = np.random.rand(self.output_nodes, 1)
        self.bias_o = translate_random(self.bias_o)

        #set learning rate
        self.learning_rate = 0.01
        self.mutation_nudge = 5



    def predict(self, input_array):
        #generate the Hidden outputs 
        inputs = np.array(input_array)
        inputs.shape = (self.input_nodes,1)
        hidden = np.dot(self.weights_ih, inputs)
        hidden = hidden + self.bias_h
        #activation function
        #hidden = sigmoid(hidden)
        hidden = np.tanh(hidden)

        #generate the outputs output:
        outputs = np.dot(self.weights_ho, hidden)
        outputs = outputs + self.bias_o
        #outputs = sigmoid(outputs)
        outputs = np.tanh(outputs)
        
        return np.ndarray.tolist(outputs)

    def train(self, input_array, target_array):
        #generate the Hidden outputs 
        inputs = np.array(input_array)
        inputs.shape = (self.input_nodes,1)

        hidden = np.dot(self.weights_ih, inputs)
        hidden = np.add(hidden, self.bias_h)
        #activation function
        hidden = sigmoid(hidden)

        #generate the outputs output:
        outputs = np.dot(self.weights_ho, hidden)
        outputs = np.add(outputs, self.bias_o)
        outputs = sigmoid(outputs)

        #convert target_array to array
        targets = np.array(target_array)
        targets.shape = (self.output_nodes, 1)

        #calculate error
        #error = targets - outputs
        output_errors = np.subtract(targets, outputs)

        #calc gradient
        gradients = de_sigmoid(outputs)
        gradients = np.multiply(gradients, output_errors)
        gradients = np.multiply(gradients, self.learning_rate)


        #calculate deltas
        hidden_T = hidden.T
        weight_ho_deltas = np.multiply(gradients, hidden_T)

        #adjust the weights by deltas
        self.weights_ho = np.add(self.weights_ho, weight_ho_deltas)
        #adjust the bias by its deltas (which is just the gradients)
        self.bias_o = np.add(self.bias_o, gradients)

        #calculate the hidden layer errors
        who_t = self.weights_ho.T
        hidden_errors = np.dot(who_t, output_errors)

        #calculate hidden gradient
        hidden_gradient = de_sigmoid(hidden)
        hidden_gradient = np.multiply(hidden_gradient, hidden_errors)
        hidden_gradient = np.multiply(hidden_gradient, self.learning_rate)

        #calculate inputs-> hidden deltas
        inputs_T = inputs.T
        weight_ih_deltas = np.dot(hidden_gradient, inputs_T)

        self.weights_ih= np.add(self.weights_ih, weight_ih_deltas)
        #adjust bias by deltas
        self.bias_h= np.add(self.bias_h, hidden_gradient)


    
    def apply_mutation(self,lst_array, rate):
        for row in lst_array:
            for item in row:
                if random.randint(0,100)>=rate: 
                    
                    item = item +((random.random()/self.mutation_nudge) * 2) - ((1)/self.mutation_nudge)
                    "rand str"


    #mutate the weights
    def mutate(self,rate):
        self.apply_mutation(self.weights_ih,rate)
        self.apply_mutation(self.weights_ho,rate)
        self.apply_mutation(self.bias_h,rate)
        self.apply_mutation(self.bias_o,rate)

    def copy(self):
        temp = NeuralNetwork(self.input_nodes,self.hidden_nodes,self.output_nodes)
        temp.weights_ih = copy.deepcopy(self.weights_ih)
        temp.weights_ho = copy.deepcopy(self.weights_ho)
        temp.bias_h = copy.deepcopy(self.bias_h)
        temp.bias_o = copy.deepcopy(self.bias_o)
        return temp