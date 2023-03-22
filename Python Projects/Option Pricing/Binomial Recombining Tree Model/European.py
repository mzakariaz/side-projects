import numpy as np

# VARIABLES:
# S0:           asset price at initial time
# K:            strike price
# r:            risk-free interest rate
# u:            uptick factor
# d:            downtick factor
# T:            maturity date
# N:            number of time steps from initial time to maturity date
# option_type:  option type (here either put or call)

#----------------------------------------------------------------------------------------------------

# FUNCTIONS:
def european_option_binomial_tree_model_slow(S0,K,r,u,d,T,N,option_type="C"):
    # payoff function for a European option
    def pay_off(S):                                                                                             # specifies the payoff function for a European option
        if option_type == "C":                                                                                  # specifies a European call option
            return max(S-K,0)                                                                                   # payoff function for a European call option
        elif option_type == "P":                                                                                # specifies a European put option
            return max(K-S,0)                                                                                   # payoff function for a European put option
    
    # define the discrete time step, the discrete discount factor and the risk-neutral probability measure
    dt = T/N                # discrete time increment
    df = (1+r*dt)**(-1)     # discrete discount factor
    q = (1+r*dt-d)/(u-d)    # risk-neutral probability measure

    # specify asset prices as maturity date
    S = np.zeros(N + 1)
    for j in range(0,N+1):
        S[j] = S0*(u**j)*(d**(N-j))

    # specify option prices at maturity date
    V = np.zeros(N + 1)
    for j in range(0,N+1):
        V[j] = pay_off(S[j])
    
    # use the backwards-recursion formula for European option prices to compute the option price at initial date
    for i in np.arange(N,0,-1):
        for j in range(0,i):
            V[j] = df*(q*V[j+1]+(1-q)*V[j])
    
    return round(V[0],2)

def european_option_binomial_tree_model_fast(S0,K,r,u,d,T,N,option_type="C"):
    # define the discrete time step, the discrete discount factor and the risk-neutral probability measure
    dt = T/N                # discrete time step
    df = (1+r*dt)**(-1)     # discrete discount factor
    q = (1+r*dt-d)/(u-d)    # risk-neutral probability measure

    # specify asset prices as maturity date
    S = S0 * d **(np.arange(N,-1,-1)) * u **(np.arange(0,N+1,1))

    # specify option prices at maturity date
    if option_type == "C":
        V = np.maximum(S-K,np.zeros(N+1))
    elif option_type == "P":
        V = np.maximum(K-S,np.zeros(N+1))
    
    # use the backwards-recursion formula for European option prices to compute the option price at initial date
    for i in np.arange(N,0,-1):
        V = df*(q*V[1:i+1] + (1 - q)*V[0:i])
    
    return round(V[0],2)

print(european_option_binomial_tree_model_slow(100,100,0.02,1.1,0.9,1,20,"C"))
print(european_option_binomial_tree_model_fast(100,100,0.02,1.1,0.9,1,20,"C"))