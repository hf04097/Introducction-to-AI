
"""
CS 351 - Artificial Intelligence 
Assignment 3

Student ID = hf04097
"""

import numpy as np
import matplotlib.pyplot as plt


"""This function takes actual and predicted ratings and compute total mean square error(mse) in observed ratings.
"""
def computeError(R,predR):
    
    """Your code to calculate MSE goes here"""
    predR = np.asarray(predR)
    MSE = 0
    n =0
    for i in range(predR.shape[0]):
        for j in range(predR.shape[1]):
            if R[i,j]!= 0:
                MSE = MSE + np.square(np.subtract(R[i][j], predR[i][j]))
                n +=1
    MSE = MSE/n
    return MSE


"""
This fucntion takes P (m*k) and Q(k*n) matrices alongwith user bias (U) and item bias (I) and returns predicted rating. 
where m = No of Users, n = No of items
"""
def getPredictedRatings(P,Q,U,I):

    """Your code to predict ratinngs goes here"""  
    R_cap = np.zeros((P.shape[0],Q.shape[1]))
    for i in range(P.shape[0]):
        for j in range(Q.shape[1]):
            R_cap[i,j] = U[i] + I[j] + P[i, :].dot(Q[:,j])

    return R_cap


"""This fucntion runs gradient descent to minimze error in ratings by adjusting P, Q, U and I matrices based on gradients.
   The functions returns a list of (iter,mse) tuple that lists mse in each iteration
"""
def runGradientDescent(R,P,Q,U,I,iterations,alpha):
    iter_mse =[]
    
    for iter in range (iterations):
        R_cap = getPredictedRatings(P,Q,U,I)
        errorMatrix = np.zeros((P.shape[0],Q.shape[1])) 
        for i in range(P.shape[0]):
            for j in range(Q.shape[1]):
                errorMatrix[i,j] = R[i,j]-R_cap[i,j]
        for i in range(P.shape[0]):
            for j in range(Q.shape[1]):
                
                if R[i, j] == 0:
                    continue
                
                U[i] = U[i] - 2* alpha * (errorMatrix[i,j])
                I[j] = I[j] - 2*alpha * (errorMatrix[i,j])
                P[i,:] = P[i,:] + 2 * (alpha * (errorMatrix[i,j] * Q[:,j]))
                Q[:,j] = Q[:,j] + 2 * alpha * (errorMatrix[i,j] * P[i, :])
        
        iter_mse.append((iter,computeError(R,R_cap)))
    
    
    """"finally returns (iter,mse) values in a list"""
    return iter_mse

def matrixFactorization(R,k,iterations, alpha):

    """Your code to initialize P, Q, U and I matrices goes here. P and Q will be randomly initialized whereas U and I will be initialized as zeros. 
    Be careful about the dimension of these matrices
    """
    
    p_rows = R.shape[0]
    q_col = R.shape[1]
    P = np.random.rand(p_rows,k)
    Q = np.random.rand(k,q_col)
    U = np.zeros(p_rows)
    I = np.zeros(q_col)
    
    
    #Run gradient descent to minimize error
    stats = runGradientDescent(R,P,Q,U,I,iterations,alpha)
    print('P matrx:')
    print(P)
    print('Q matrix:')
    print(Q)
    print("User bias:")
    print(U)
    print("Item bias:")
    print(I)
    print("P x Q:")
    print(getPredictedRatings(P,Q,U,I))
    plotGraph(stats)

def plotGraph(stats):
    i = [i for i,e in stats]
    e = [e for i,e in stats]
    plt.plot(i,e)
    plt.xlabel("Iterations")
    plt.ylabel("Mean Square Error")
    plt.show()    


""""
User Item rating matrix given ratings of 5 users for 6 items.
Note: If you want, you can change the underlying data structure and can work with starndard python lists instead of np arrays
We may test with different matrices with varying dimensions and number of latent factors. Make sure your code works fine in those cases.
"""
R = np.array([
[5, 3, 0, 1, 4, 5],
[1, 0, 2, 0, 0, 0],
[3, 1, 0, 5, 1, 3],
[2, 0, 0, 0, 2, 0],
[0, 1, 5, 2, 0, 0],
])

R = np.asarray(R) #even if list is passed I want a numpy array
k = 3
alpha = 0.01
iterations = 500

matrixFactorization(R,k,iterations, alpha)







