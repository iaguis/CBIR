#!/usr/bin/env python
 
import numpy as np
import sys
import scipy.optimize as sp

from fmincg import fmincg
 
def read_training_examples(file_X, file_y):
    X = np.genfromtxt(file_X, delimiter=" ")
    y = np.genfromtxt(file_y)
    return X, y

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))
    
def sigmoid_gradient(z):
    #print (z.shape)
    g = np.zeros(z.shape)
    #print(g)
    
    g = sigmoid(z) * (1 - sigmoid(z))
    
    return g

def rand_initialize_weights(L_in, L_out):
    W = np.zeros((L_out, 1+L_in))
    
    epsilon_init = 0.12
    
    W = np.random.rand(L_out, 1+L_in) * 2 * epsilon_init - epsilon_init
    
    return W

def nn_cost_function(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lambd):
    theta_size = hidden_layer_size*(input_layer_size+1)
    
    Theta1 = nn_params[:theta_size].reshape(hidden_layer_size, input_layer_size+1).copy()
    Theta2 = nn_params[theta_size:].reshape(num_labels, hidden_layer_size+1).copy()
    
    m = X.shape[0]
    
    J = 0.
    Theta1_grad = np.zeros(Theta1.shape)
    Theta2_grad = np.zeros(Theta2.shape)
        
    X = np.concatenate((np.ones((m,1)), X),1)
    
    for i in range(m):
        y_encoded = np.zeros((num_labels,1))
        # FIXME Change this when training the net
        #what = y[i]
        #if what == 0:
            #what = 9
        #else:
            #what = y[i]-1

        y_encoded[y[i]] = [1]
        
        
        a_1 = X[i, :].T.copy()
        a_1 = a_1[np.newaxis].T
                
        z_2 = np.dot(Theta1, a_1)
        a_2 = sigmoid(z_2)
        
        a_2 = np.concatenate((np.array([[1]]), a_2))

        z_3 = np.dot(Theta2, a_2)
        
        a_3 = sigmoid(z_3)
        h = a_3.copy()
        
        delta_3 = a_3 - y_encoded

        delta_2 = np.dot(Theta2.T, delta_3) * sigmoid_gradient(np.concatenate((np.array([[1]]), z_2)))
        
        delta_2 = delta_2[1:].copy()

        Theta2_grad = Theta2_grad + np.dot(delta_3, a_2.T)
        
        Theta1_grad = Theta1_grad + np.dot(delta_2, a_1.T)
        
        J = J + (np.dot(-y_encoded.T, np.log(h)) - np.dot((1 - y_encoded).T, np.log(1-h))).item()
    J = J/m
    
    J = J + (lambd/(2*m)) * (sum(sum(Theta1[:, 1:]**2)) + sum(sum(Theta2[:, 1:]**2)))
    
    Theta1_grad = Theta1_grad/m
    Theta2_grad = Theta2_grad/m
    
    Theta1_grad[:, 1:] = Theta1_grad[:, 1:] + (lambd/m) * Theta1_grad[:, 1:]
    Theta2_grad[:, 1:] = Theta2_grad[:, 1:] + (lambd/m) * Theta2_grad[:, 1:]
    grad = np.concatenate((Theta1_grad.flatten(), Theta2_grad.flatten()))
    
    return J, grad
    
def predict(Theta1, Theta2, X):
    m = X.shape[0]
    num_labels = Theta2.shape[0]
        
    h1 = sigmoid(np.dot(np.concatenate((np.ones((m, 1)), X), 1), Theta1.T))
    h2 = sigmoid(np.dot(np.concatenate((np.ones((m, 1)), h1), 1), Theta2.T))
    #p = np.max(h2, axis=1)[np.newaxis].T
    p = h2.argmax(axis=1)[np.newaxis].T
    
    return p
    
def train(X, y):
    input_layer_size  = 400
    hidden_layer_size = 25
    num_labels = 10
    
    initial_Theta1 = rand_initialize_weights(input_layer_size, hidden_layer_size)
    initial_Theta2 = rand_initialize_weights(hidden_layer_size, num_labels)
       
    initial_nn_params = np.concatenate((initial_Theta1.flatten(), initial_Theta2.flatten()))
        
    lambd = 3
       
    def costFunction(p):
        return nn_cost_function(p, input_layer_size, hidden_layer_size, num_labels, X, y, lambd)
        
       
    nn_params, cost, i = fmincg(costFunction, initial_nn_params, 50)
        
    theta_size = hidden_layer_size*(input_layer_size+1)
        
    Theta1 = nn_params[:theta_size].reshape(hidden_layer_size, input_layer_size+1).copy()
    Theta2 = nn_params[theta_size:].reshape(num_labels, hidden_layer_size+1).copy()
    if cost[len(cost)-1] < 0.8:
        np.savetxt("Theta1.txt", Theta1)
        np.savetxt("Theta2.txt", Theta2)
    return Theta1, Theta2
        
def usage():
    print("Usage: ", sys.argv[0], " train|predict")

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if len(sys.argv) < 2:
            usage()
            return
        
        if sys.argv[1] == "train":
            X, y = read_training_examples("training_X.txt", "training_y.txt")
            Theta1, Theta2 = train(X, y)
        elif sys.argv[1] == "predict":
            X, y = read_training_examples("training_X.txt", "training_y.txt")
            Theta1 = np.genfromtxt("Theta1.txt")
            Theta2 = np.genfromtxt("Theta2.txt")
        else:
            usage()
            return
        
        pred = predict(Theta1, Theta2, X)

        print("Training Set Accuracy ", np.mean(pred == y[np.newaxis].T))
    except Exception:
        print(Exception.msg, file=sys.stderr)
        return -1

if __name__ == "__main__":
    sys.exit(main())
     
