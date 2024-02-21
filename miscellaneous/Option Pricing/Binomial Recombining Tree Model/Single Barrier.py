import numpy as np

# VARIABLES
# S0:               asset price at initial time
# K:                strike price
# H:                barrier price
# r:                risk-free interest rate
# u:                uptick factor
# d:                downtick factor
# T:                maturity date
# N:                number of time steps from initial time to maturity date
# option_type:      option type (here either call or put)
# barrier_type:     barrier type (here either up-and-out or down-and-out)

#----------------------------------------------------------------------------------------------------

# FUNCTIONS:
def single_barrier_option_binomial_tree_model_slow(S0,K,H,r,u,d,T,N,option_type="C",barrier_type="U"):
    # payoff function for a barrier option
    def pay_off(S):                                                                                             # specifies the payoff function for a barrier option
        if option_type == "C":                                                                                  # specifies a barrier call option
            return max(S-K,0)                                                                                   # payoff function for a barrier call option
        elif option_type == "P":                                                                                # specifies a barrier put option
            return max(K-S,0)                                                                                   # payoff function for a barrier put option
    
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
        if (barrier_type == "U" and S[j] >= H) or (barrier_type == "D" and S[j] <= H):
            V[j] = 0
        else:
            V[j] = pay_off(S[j])
    
    # use the backwards-recursion formula for barrier option prices to compute the option price at initial date
    for i in np.arange(N-1,-1,-1):
        for j in range(0,i+1):
            if (barrier_type == "U" and S0*(u**j)*(d**(i-j)) >= H) or (barrier_type == "D" and S0*(u**j)*(d**(i-j)) <= H):
                V[j] = 0
            else:
                V[j] = df*(q*V[j+1]+(1-q)*V[j])

    return V[0]

def single_barrier_option_binomial_tree_model_fast(S0,K,H,r,u,d,T,N,option_type="C",barrier_type="U"):
    # define the discrete time step, the discrete discount factor and the risk-neutral probability measure
    dt = T/N                # discrete time increment
    df = (1+r*dt)**(-1)     # discrete discount factor
    q = (1+r*dt-d)/(u-d)    # risk-neutral probability measure

    # specify asset prices as maturity date
    S = S0 * d**(np.arange(N,-1,-1)) * u**(np.arange(0,N+1,1))

    # specify option prices at maturity date
    if option_type == "C":
        V = np.maximum(S - K,0)
    elif option_type == "P":
        V = np.maximum(K - S,0)
    if barrier_type == "U":
        V[S >= H] = 0
    elif barrier_type == "D":
        V[S <= H] = 0

    # use the backwards-recursion formula for barrier option prices to compute the option price at initial date
    for i in np.arange(N-1,-1,-1):
        W = S0 * d**(np.arange(i,-1,-1)) * u**(np.arange(0,i+1,1))
        V[:i+1] = df*(q*V[1:i+2]+(1-q)*V[:i+1])
        V = V[:-1]
        if barrier_type == "U":
            V[W >= H] = 0
        elif barrier_type == "D":
            V[W <= H] = 0

    return V[0]

print(single_barrier_option_binomial_tree_model_slow(100,100,125,0.06,1.1,1/1.1,1,3,"C","U"))
print(single_barrier_option_binomial_tree_model_fast(100,100,125,0.06,1.1,1/1.1,1,3,"C","U"))