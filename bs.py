"""
This module contains backscholes calculations of prices and greeks for options
"""
# http://www.quantacademy.com/2014/09/options-greeks-calculation-with-python/
 
 
#===============================================================================
# LIBRARIES
#===============================================================================
import math
from scipy.stats import norm
import pandas as pd
from datetime import date
import numpy as np
 
 
#===============================================================================
# CLASS OPTION  
#===============================================================================
class Option:
    """
    This class will group the different black-shcoles calculations for an opion
    """
    def __init__(self, right, s, k, eval_date, exp_date, price = None, rf = 0.01, vol = 0.3,
                 div = 0):
        self.k = float(k)
        self.s = float(s)
        self.rf = float(rf)
        self.vol = float(vol)
        self.eval_date = eval_date
        self.exp_date = exp_date
        self.t = self.calculate_t()
        if self.t == 0: self.t = 0.000001 ## Case valuation in expiration date
        self.price = price
        self.right = right   ## 'C' or 'P'
        self.div = div
 
    def calculate_t(self):
        if isinstance(self.eval_date, str):
            if '/' in self.eval_date:
                (day, month, year) = self.eval_date.split('/')
            else:
                (day, month, year) = self.eval_date[6:8], self.eval_date[4:6], self.eval_date[0:4]
            d0 = date(int(year), int(month), int(day))
        elif type(self.eval_date)==float or type(self.eval_date)==int or type(self.eval_date)==np.float64:
            (day, month, year) = (str(self.eval_date)[6:8], str(self.eval_date)[4:6], str(self.eval_date)[0:4])
            d0 = date(int(year), int(month), int(day))
        else:
            d0 = self.eval_date 
 
        if isinstance(self.exp_date, str):
            if '/' in self.exp_date:
                (day, month, year) = self.exp_date.split('/')
            else:
                (day, month, year) = self.exp_date[6:8], self.exp_date[4:6], self.exp_date[0:4]
            d1 = date(int(year), int(month), int(day))
        elif type(self.exp_date)==float or type(self.exp_date)==int or type(self.exp_date)==np.float64:
            (day, month, year) = (str(self.exp_date)[6:8], str(self.exp_date)[4:6], str(self.exp_date)[0:4])
            d1 = date(int(year), int(month), int(day))
        else:
            d1 = self.exp_date
 
        return (d1 - d0).days / 365.0
 
    def get_price_delta(self):
        d1 = ( math.log(self.s/self.k) + ( self.rf + self.div + math.pow( self.vol, 2)/2 ) * self.t ) / ( self.vol * math.sqrt(self.t) )
        d2 = d1 - self.vol * math.sqrt(self.t)
        if self.right == 'C':
            self.calc_price = ( norm.cdf(d1) * self.s * math.exp(-self.div*self.t) - norm.cdf(d2) * self.k * math.exp( -self.rf * self.t ) )
            self.delta = norm.cdf(d1)
        elif self.right == 'P':
            self.calc_price =  ( -norm.cdf(-d1) * self.s * math.exp(-self.div*self.t) + norm.cdf(-d2) * self.k * math.exp( -self.rf * self.t ) )
            self.delta = -norm.cdf(-d1) 
 
    def get_call(self):
        d1 = ( math.log(self.s/self.k) + ( self.rf + math.pow( self.vol, 2)/2 ) * self.t ) / ( self.vol * math.sqrt(self.t) )
        d2 = d1 - self.vol * math.sqrt(self.t)
        self.call = ( norm.cdf(d1) * self.s - norm.cdf(d2) * self.k * math.exp( -self.rf * self.t ) )
        #put =  ( -norm.cdf(-d1) * self.s + norm.cdf(-d2) * self.k * math.exp( -self.rf * self.t ) ) 
        self.call_delta = norm.cdf(d1)
 
 
    def get_put(self):
        d1 = ( math.log(self.s/self.k) + ( self.rf + math.pow( self.vol, 2)/2 ) * self.t ) / ( self.vol * math.sqrt(self.t) )
        d2 = d1 - self.vol * math.sqrt(self.t)
        #call = ( norm.cdf(d1) * self.s - norm.cdf(d2) * self.k * math.exp( -self.rf * self.t ) )
        self.put =  ( -norm.cdf(-d1) * self.s + norm.cdf(-d2) * self.k * math.exp( -self.rf * self.t ) )
        self.put_delta = -norm.cdf(-d1) 
 
 
    def get_theta(self, dt = 0.0027777):
        self.t += dt
        self.get_price_delta()
        after_price = self.calc_price
        self.t -= dt
        self.get_price_delta()
        orig_price = self.calc_price
        self.theta = (after_price - orig_price) * (-1)
 
    def get_gamma(self, ds = 0.01):
        self.s += ds
        self.get_price_delta()
        after_delta = self.delta
        self.s -= ds
        self.get_price_delta()
        orig_delta = self.delta
        self.gamma = (after_delta - orig_delta) / ds
 
    def get_all(self):
        self.get_price_delta()
        self.get_theta()
        self.get_gamma()
        return self.calc_price, self.delta, self.theta, self.gamma
 
 
    def get_impl_vol(self):
        """
        This function will iterate until finding the implied volatility
        """
        ITERATIONS = 100
        ACCURACY = 0.05
        low_vol = 0
        high_vol = 1
        self.vol = 0.5  ## It will try mid point and then choose new interval
        self.get_price_delta()
        for i in range(ITERATIONS):
            if self.calc_price > self.price + ACCURACY:
                high_vol = self.vol
            elif self.calc_price < self.price - ACCURACY:
                low_vol = self.vol
            else:
                break
            self.vol = low_vol + (high_vol - low_vol)/2.0
            self.get_price_delta()
 
        return self.vol
 
    def get_price_by_binomial_tree(self):
        """
        This function will make the same calculation but by Binomial Tree
        """
        n=30
        deltaT=self.t/n
        u = math.exp(self.vol*math.sqrt(deltaT))
        d=1.0/u
        # Initialize our f_{i,j} tree with zeros
        fs = [[0.0 for j in range(i+1)] for i in range(n+1)]
        a = math.exp(self.rf*deltaT)
        p = (a-d)/(u-d)
        oneMinusP = 1.0-p 
        # Compute the leaves, f_{N,j}
        for j in range(i+1):
            fs[n][j]=max(self.s * u**j * d**(n-j) - self.k, 0.0)
        print(fs)
 
        for i in range(n-1, -1, -1):
            for j in range(i+1):
                fs[i][j]=math.exp(-self.rf * deltaT) * (p * fs[i+1][j+1] +
                                                        oneMinusP * fs[i+1][j])
        print(fs)
 
        return fs[0][0]
 
#===============================================================================
# CLASS OPTIONS STRATEGY
#=============================================================================== 
class Options_strategy:
    """
    This class will calculate greeks for a group of options (called Options Strategy)
    """
    def __init__(self, df_options): 
        self.df_options = df_options       #It will store the different options in a pandas dataframe
 
    def get_greeks(self):
        """
        For analysis underlying (option chain format)
        """
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        for k,v in self.df_options.iterrows():
 
            ## Case stock or future
            if v['m_secType']=='STK':
                self.delta += float(v['position']) * 1
 
            ## Case option
            elif v['m_secType']=='OPT':    
                opt = Option(s=v['underlying_price'], k=v['m_strike'], eval_date=date.today(), # We want greeks for today
                             exp_date=v['m_expiry'], rf = v['interest'], vol = v['volatility'],
                             right = v['m_right'])
 
                price, delta, theta, gamma = opt.get_all()
 
                self.delta += float(v['position']) * delta
                self.gamma += float(v['position']) * gamma
                self.theta += float(v['position']) * theta
 
            else:
                print("ERROR: Not known type")
 
        return self.delta, self.gamma, self.theta 
 
    def get_greeks2(self):
        """
        For analysis_options_strategy
        """
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        for k,v in self.df_options.iterrows():
 
            ## Case stock or future
            if v['m_secType']=='STK':
                self.delta += float(v['position']) * 1
 
            ## Case option
            elif v['m_secType']=='OPT':    
                opt = Option(s=v['underlying_price'], k=v['m_strike'], eval_date=date.today(), # We want greeks for today
                             exp_date=v['m_expiry'], rf = v['interest'], vol = v['volatility'],
                             right = v['m_right'])
 
                price, delta, theta, gamma = opt.get_all()
 
                if v['m_side']=='BOT':
                    position = float(v['position'])
                else:
                    position = - float(v['position']) 
                self.delta += position * delta
                self.gamma += position * gamma
                self.theta += position * theta
 
            else:
                print("ERROR: Not known type")
 
        return self.delta, self.gamma, self.theta 
 
 
if __name__ == '__main__':
 
 
    #===========================================================================
    # TO CHECK OPTION CALCULATIONS
    #===========================================================================
    s = 56.37  # spot
    k = 60  # strike
    exp_date = '20171215'
    eval_date = '20140528'
    rf = 0.01
    vol = 0.2074
    div = 0.014
    right = 'C'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, right=right,
                 div = div)
    price, delta, theta, gamma = opt.get_all()
    print("-------------- FIRST OPTION -------------------")
    print("Price CALL: " + str(price))  # 2.97869320042
    print("Delta CALL: " + str(delta))  # 0.664877358932
    print("Theta CALL: " + str(theta))  # 0.000645545628288
    print("Gamma CALL:" + str(gamma))   # 0.021127937082
 

    #===========================================================================
    # TO CHECK OPTION CALCULATIONS
    #===========================================================================
    s = 50  # spot
    k = 100  # strike
    exp_date = '20150528'
    eval_date = '20140528'
    rf = 0.05  # 5%
    vol = 0.25  # 25
    div = 0.1
    right = 'P'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, right=right,
                 div = div)
    price, delta, theta, gamma = opt.get_all()
    print("-------------- FIRST.2 OPTION -------------------")
    print("Price CALL: " + str(price))  # 2.97869320042
    print("Delta CALL: " + str(delta))  # 0.664877358932
    print("Theta CALL: " + str(theta))  # 0.000645545628288
    print("Gamma CALL:" + str(gamma))   # 0.021127937082
    # price = opt.get_price_by_binomial_tree()
    # print("Price by BT:" + str(price))
 
    s = 110.41
    k = 112
    exp_date = '20160115'
    eval_date = '20140429'
    rf = 0.01
    vol = 0.11925
    right = 'C'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, vol=vol, right=right)
    price, delta, theta, gamma = opt.get_all()
    print("-------------- SECOND OPTION -------------------")
    print("Price CALL: " + str(price))   # 7.02049813137
    print("Delta CALL: " + str(delta))   # 0.53837898036
    print("Theta CALL: " + str(theta))   # -0.00699852931575
    print("Gamma CALL:" + str(gamma))    # 0.0230279263655
 
    #===========================================================================
    # TO CHECK OPTIONS STRATEGIES CALCULATIONS
    #===========================================================================
    d_option1 = {'m_secType': 'OPT', 'm_expiry': '20150116', 'm_right': 'C', 'm_symbol': 'TLT', 'm_strike': '115', 
                 'm_multiplier': '100', 'position': '-2', 'trade_price': '3.69', 'comission': '0',
                 'eval_date': '20140422', 'interest': '0.01', 'volatility': '0.12353', 'underlying_price': '109.96'}
    d_option2 = {'m_secType': 'OPT', 'm_expiry': '20150116', 'm_right': 'C', 'm_symbol': 'TLT', 'm_strike': '135', 
                 'm_multiplier': '100', 'position': '2', 'trade_price': '0.86', 'comission': '0',
                 'eval_date': '20140422', 'interest': '0.01', 'volatility': '0.12353', 'underlying_price': '109.96'}
 
    # df_options = pd.DataFrame([d_option1, d_option2])
    # opt_strat = Options_strategy(df_options)
    # delta, gamma, theta = opt_strat.get_greeks()
    # print("-------- OPTIONS STRATEGY --------------")
    # print("Delta: " + str(delta))
    # print("Gamma: " + str(gamma))
    # print("Theta: " + str(theta))
 
    #===========================================================================
    # TO CHECK OPTION IMPLIED VOLATILITY CALCULATION 
    #===========================================================================
    s = 110.63
    k = 115
    exp_date = '20150116'
    eval_date = '20140424'
    rf = 0.01
    price = 3.18  ## Calculated for a vol = 0.12353
    right = 'C'
    opt = Option(s=s, k=k, eval_date=eval_date, exp_date=exp_date, rf=rf, price=price, right=right)
    ivol = opt.get_impl_vol()
    print("-------------- FIRST OPTION -------------------")
    print("Implied Volatility: " + str(ivol))