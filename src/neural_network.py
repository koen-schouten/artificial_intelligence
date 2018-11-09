import numpy as np

class Sigmoid_Layer:
    def __init__(self, n_i):
        """
        Constructor for the sigmoid layer
        Creates an empty numpy vector for the output

        Keyword arguments:
        n_i -- an integer for the number of inputs/outputs for this layer
        """
        self.output = np.arange(n_i)
        

    def output_values(self, input):
        """
        Calculates and returns the output of the Sigmoid layer
        Stores the output inside the layer for backprop error calculation

        Keyword arguments:
        input -- An numpy vector of size n_i that's the input for this layer
        """
        f = np.vectorize(lambda x: 1/(1+ np.exp(-x)) , otypes=[np.float])

        self.output = f(input)

        #convert matrix back to vector
        if self.output.ndim == 2:
           self.output = np.squeeze(np.asarray(self.output))

        return self.output


    def backprop(self, error):
        """
        Calculates and returns the error for this layer

        Keyword arguments:
        error -- An numpy vector of size n_i
        """
        f = np.vectorize(lambda x: (1-x))
        input_error = self.output * f(self.output) * error
        return input_error

class Linear_complete_layer:
    def __init__(self, n_i, n_o):
        """
        Constructor for the Linear layer
        Creates an empty matrix for the weights
        Creates an empty numpy vector for the input

        Keyword arguments:
        n_i -- an integer for the number of inputs for this layer
        n_o -- an integer for the number of outputs for this layer
        """
        self.n_i = n_i
        self.n_o = n_o
        self.weights = np.zeros((n_o , n_i + 1))
        self.input = np.arange(n_i + 1)

    def output_values(self, input):
        """
        Calculates and returns the output of the Linear layer

        Keyword arguments:
        input -- An numpy vector of size n_i that's the input for this layer
        """

        self.input = np.append(input, [1])
        output = np.dot(self.weights, self.input)
        return output

    def backprop(self, error, learning_rate):
        """
        Calculates and propagates the error of the Linear_complete_layer

        Keyword arguments:
        error -- An numpy vector of size n_o 
        """
        for j in range(error.size):
            for i in range(self.input.size):
                self.weights[j,i] = self.weights[j,i] + learning_rate * self.input[i] * error[j]
        #calculate input error
        input_error = np.dot(np.transpose(self.weights)[:-1], error)
        
        #convert matrix back to vector
        if input_error.ndim == 2:
            input_error = np.squeeze(np.asarray(input_error))
            
        return input_error

    def set_weights(self, weights):
        self.weights = weights

        

#returns initial Backprop error
def sum_square_error_layer(Ys, predicted):
    """
        Calculates the initial Backprop error

        Keyword arguments:
        Ys -- An numpy vector of the actual result from the test set
        predicted -- An numpy vector of the prediction from the neural network
        """
    error = Ys - predicted

    #The error turns into a float when the result is a vector of size 1.
    #We need to turn this back into a vector
    if error.ndim == 0:
        error = np.array([error])
    return error

def Neural_network_learner(input_features, 
                           output_features, 
                           example_set, 
                           layers, 
                           learning_rate,
                           number_of_iterations):
    #TODO 
    pass

if __name__ == '__main__':
    input_features = ["x_1", "x_2"]
    output_features = ["y"]
    example_set = {"x1" : 1, "x2": 0, "y": 1}
    learning_rate = 0.1

    L1 = Linear_complete_layer(2,2)
    S1 = Sigmoid_Layer(2)
    L2 = Linear_complete_layer(2,1)
    S2 = Sigmoid_Layer(1)

    L1.set_weights(np.matrix([[0.5, 1.0, -0.5],[ -0.5, 1.0, -1.0]]))
    L2.set_weights(np.matrix([-0.5, -0.5, 1]))

    start = np.array([1,0])

    print(L1.output_values(start))
    print("-------")
    print(S1.output_values(L1.output_values(start)))
    print("-------")
    print(L2.output_values(S1.output_values(L1.output_values(start))))
    print("-------")
    print(S2.output_values(L2.output_values(S1.output_values(L1.output_values(start)))))

    print("Backprop error part:")
    output = S2.output_values(L2.output_values(S1.output_values(L1.output_values(start))))
    error = sum_square_error_layer(1,output)
    print(error)
    print("-------")
    print(L2.backprop(S2.backprop(error),learning_rate))
    print("-------")
    print(S1.backprop(L2.backprop(S2.backprop(error),learning_rate)))

    print(L1.backprop(S1.backprop(L2.backprop(S2.backprop(error),learning_rate)),learning_rate))

    print(L1.weights)

    layers = [L1, S1, L2, S2]


