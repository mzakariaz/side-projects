import numpy as np

# VARIABLES
# S0:               asset price at initial time
# K:                strike price
# H:                Asian price
# r:                risk-free interest rate
# u:                uptick factor
# d:                downtick factor
# T:                maturity date
# N:                number of time steps from initial time to maturity date
# option_type:      option type (here either call or put)
# strike_type:      strike type (here either fixed or floating)
# mean_type:        mean type (here either maximum, quadratic, arithmetic, geometric, harmonic or minimum)

#----------------------------------------------------------------------------------------------------

# FUNCTIONS:
def asian_option_binomial_tree_model_slow(S0,K,H,r,u,d,T,N,option_type="C",strike_type="FI",mean_type="AM"):    
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
        if (Asian_type == "U" and S[j] >= H) or (Asian_type == "D" and S[j] <= H):
            V[j] = 0
        else:
            V[j] = pay_off(S[j])
    
    # use the backwards-recursion formula for Asian option prices to compute the option price at initial date
    for i in np.arange(N-1,-1,-1):
        for j in range(0,i+1):
            if (Asian_type == "U" and S0*(u**j)*(d**(i-j)) >= H) or (Asian_type == "D" and S0*(u**j)*(d**(i-j)) <= H):
                V[j] = 0
            else:
                V[j] = df*(q*V[j+1]+(1-q)*V[j])

    return V[0]