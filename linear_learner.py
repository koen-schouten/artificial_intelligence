def linear_learner(input_features, target_features, examples, learning_rate, num_of_iterations):
    """
    An implementation of the incremental gradient descent function from the book 
    Artificial Inteligence: Foundations of computational agents
    Figure 7.8 p293
    
    
    Keyword arguments:
    input_features -- a list of the names of the input features 
    target_feature -- the name of the target features
    examples -- a list of training examples. A training example is dictionary with input-and target features as key 
    learningRate -- the learning rate.
    num_of_iterations -- the number of iterations that should be performed
    
    returns a linear function. This function takes an dictionary of input-features and values 
    
    Example usage:
    input_features = ["x"]
    input_features = "y"
    examples = [{"x":5, "y":5}]
    learning rate = 0.01
    num_of_iterations = 10000
    
    linear_function = Linear_learner(input_features, target_feature, examples, learningRate, num_of_iterations)
    >> linear_function({"x":5})
    4.99999999999969
    """
    #initialize named weights to 0.
    weights = {key: 0 for key in input_features}
    
    #add a weight for X_0
    weights.update({"X_0":0})

    #add X_0 to each example
    for example in examples:
        example.update({"X_0":1})

    #init some variables
    update = 0
    error = 0

    #define pred(e) = sum(w_i * X_i(e))
    def pred_func(weights):
        def pred_func2(args):
            sum = 0
            for weight_name in args:
                if(weight_name in weights):
                    sum += weights[weight_name] * args[weight_name]
            return sum
        return pred_func2

    
    for i in range(0,num_of_iterations):
        #for each example e inEs do
        for example in examples:
            error = example[target_feature] - pred_func(weights)(example)
            update = learning_rate * error

            #update each weight
            for weight_name in weights:
                weights[weight_name] = weights[weight_name] + update * example[weight_name]

   
    #This function creates the final linear function from the pred(e) function
    #the pred(e) function requires X_0 as an input
    #we don't want this for our resulting linear function
    #This function removes the requirement the X_0 parameter
    def generate_linear_function(pred_func):
        def linear_function(args):
            args.update({"X_0":1})
            return pred_func(args)
        return linear_function

    return generate_linear_function(pred_func(weights))

#Below is an example based on figure 7.3 p277
if __name__ == '__main__':
    import matplotlib.pylab as plt
    import numpy as np

    input_features = ["x"]
    target_feature = "y"
    examples = [{"x":0.7, "y":1.7},
                {"x":1.1, "y":2.4},
                {"x":1.3, "y":2.5},
                {"x":1.9, "y":1.7},
                {"x":2.6, "y":2.1},
                {"x":3.9, "y":7}]
    learning_rate = 0.001
    num_of_iterations = 10000
    linear_function = linear_learner(input_features, target_feature, examples, learning_rate, num_of_iterations)


    def regression_function(fn, x):
        return fn({"x":x})


    plt.plot([data['x'] for data in examples],
            [data['y'] for data in examples],'ro')

    plt.plot(np.arange(0, 5, 1), regression_function(linear_function, np.arange(0, 5, 1)).astype(np.float) )

    plt.show()