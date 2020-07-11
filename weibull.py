from collections import Counter
import numpy as np
from sklearn.linear_model import LinearRegression


class WeibullDistSolver:
    """
    Solver for searching Weibull distribution parameters.
    """
    
    def __init__(self):
        pass
    
    
    def bin2tte(self, activity_list):
        """
        Transform binary activity list into times to events.
        
        Parameters?
            activity_list (np.array) - binary activity array
        """
        
        np.where(activity_list > 0)[0]
        
        tte_list = [1]
        for act in activity_list:
            if act == 0:
                tte_list[-1] += 1
            else:
                tte_list.append(1)
                
        self.delta = tte_list[-1]
        
        self.tte_list = []
        for i in tte_list:
            self.tte_list.extend([j for j in reversed(range(1, i + 1))])
            
    
    def linearization(self, tte_list):
        """
        Data linearization.
        
        Parameters:
            tte_list (list) list of times to events.
        """
        
        array = np.array(sorted(list(Counter(tte_list).items())))
        X, y = array[:, 0], array[:, 1] / array[:, 1]
        y = (y / y.sum()).cumsum()
        
        self.X_lin = np.log(X + 1e-6).reshape(-1, 1)
        self.y_lin = np.log((np.log(1 / (1 - y + 1e-6))))
            
            
    def calculate_parameters(self, X, y):
        """
        Calculate parameters of weibull distribution and reliability lvl.
        
        Parameters:
            X (array) features;
            y (array) target.
        """

        lr = LinearRegression().fit(X, y)
        self.score = lr.score(X, y)
        self.beta = lr.coef_[0]
        self.alpha = np.exp( - lr.intercept_ / self.beta)
    
        
    def prob(self, delta, alpha, beta):
        """
        The probability that the event will occur during the specified period.
        
        Parameters:
            delta (int) - specified period
            alpha (float) - parameter lambda in Weibull distribution
            beta (float) - parameter k in Weibull distribution
            
        Returns:
            probability (float, [0;1])
        """
        
        return 1 - np.exp( -((delta + 1e-6) / (alpha + 1e-6)) ** (beta + 1e-6))
    
    
    def fit(self, activity_list):
        """
        Compute Weibull parameters over binary activity list.
        
        Parameters:
            activity_list (np.array) - binary activity array
        """
        
        self.bin2tte(activity_list)
        
        if len(self.tte_list) < 5:
            raise ValueError("not representative activity list")
        
        self.linearization(self.tte_list)
        
        if len(self.y_lin) < 3:
            raise ValueError("not representative activity list")
        
        self.calculate_parameters(self.X_lin, self.y_lin)
    
    
    def predict(self):
        """
        Compute Prob and reliability lvl
        
        Returns:
            prob (float, [0;1]) - weibull probability (client alive)
            score (float, [0;1]) - quality lvl
        """
        
        return self.prob(self.delta, self.alpha, self.beta), self.score
            
        
activity_list = np.random.randint(0, 2, 200)
print(activity_list)
wds = WeibullDistSolver()
wds.fit(activity_list)
wds.predict()