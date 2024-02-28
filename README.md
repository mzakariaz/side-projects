# **Projects**

**Welcome to my *Projects* repository on GitHub!** :wave:

This is a repository where I will post all of my side projects. I am currently working with iPython/Jupyter notebooks and focusing on showcasing <a href = 'https://github.com/mzakariaz/Projects/tree/main/mathematics/Python'>Pure Mathematics</a> and <a href = 'https://github.com/mzakariaz/Projects/tree/main/quantitative_finance/Python'>Quantitative Finance</a> projects using Python. Other projects, namely using R, are also included (see the `datacamp` folder <a href = 'https://github.com/mzakariaz/Projects/tree/main/datacamp'>here</a>). Here are a few of the projects I have produced at present:

- [Numerical Integral Estimator](https://github.com/mzakariaz/Projects/blob/main/mathematics/Python/numerical_integral_estimator.ipynb)
- [Function Root Estimator](https://github.com/mzakariaz/Projects/blob/main/mathematics/Python/function_root_estimator.ipynb)
- [Portfolio Optimizer](https://github.com/mzakariaz/Projects/blob/main/quantitative_finance/Python/portfolio_optimizer.ipynb)
- [Malliavin Calculus for Option Greeks Estimation](https://github.com/mzakariaz/Projects/blob/main/quantitative_finance/Python/malliavin_calculus_for_option_greeks_estimation.ipynb)

To get a sense of what you can expect, Here is a Python code snippet you can try out on a `.ipynb` file (I recommend using Python 3). The full project can be found [here](https://github.com/mzakariaz/Projects/blob/main/quantitative_finance/Python/malliavin_calculus_for_option_greeks_estimation.ipynb)

```Python
import time as tm
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

np.random.seed(30)
sns.set_style(style = "whitegrid", rc = {"font.family":"Times New Roman", "font.weight":"bold"})
warnings.simplefilter(action = 'ignore', category = FutureWarning)

r, sigma, S0, K, T, M, N = 0.1, 0.2, 100, 100, 1, 50, 1000000

def MonteCarloEuropeanCallDelta(r, sigma, S0, K, T, N, show_performance_metrics = False, show_visualisations = False):
    start = tm.time()
    W = np.random.normal(0, 1, N)
    S = S0 * np.exp((r - (sigma**2) / 2) * T + sigma * np.sqrt(T) * W)                                 
    V = np.maximum(S - K, 0)
    SAMPLE = np.exp(-r * T)* V * W / (S0 * T * sigma)
    PATH = np.cumsum(SAMPLE) / np.arange(1, N + 1)
    end = tm.time()
    estimate = PATH[-1]
    if show_performance_metrics:
        computation_time = end - start
        if computation_time == 0.0:
            iterations_per_second = "\u221E"
        else:
            iterations_per_second = f"{int(N / computation_time):,}"
        d = (np.log(S0 / K) + (r + (sigma**2 / 2)) * T) / (sigma * np.sqrt(T))
        Delta = sp.stats.norm.cdf(d)
        symbol = "S0".translate(str.maketrans("0", "₀"))
        relative_error = (estimate - Delta) / estimate
        print(f"Risk-free interest rate: r = {r}")
        print(f"Volatility: \u03C3 = {sigma}")
        print(f"Initial asset price: {symbol} = {S0}")
        print(f"Strike price: K = {K}")
        print(f"Maturity date: T = {T}")
        print(f"Number of simulations: N = {N:,}")
        print(f"Estimate: \u0394 \u2248 {estimate}")
        print(f"Exact value: \u0394 = {Delta}")
        print(f"Relative error: {100 * relative_error:.2f}%")
        print(f"Computation time: {computation_time:.3f} seconds")
        print(f"Iterations per second: {iterations_per_second}")
    else:
        pass
    if show_visualisations:
        fig, ax = plt.subplots(figsize = (10, 6), dpi = 300)
        sns.lineplot(data = PATH, linewidth = 0.75, color = "b", label = "Sample Mean").set(xlabel = "Number of Simulations", ylabel = "Estimated Delta")
        plt.axhline(Delta, color = "black", linestyle = "--", linewidth = 0.75, label = f"Exact Value ({Delta:.4f})")
        plt.legend(labelcolor = "black", facecolor = "#E1E1E1")
        plt.title("Monte-Carlo Simulation of the Delta of a European Call Option")
        plt.show()
    else:
        pass
    return estimate

MonteCarloEuropeanCallDelta(r, sigma, S0, K, T, N, True, True)
```
I intend to continue expanding this repository and make increasingly sophisticated projects, moving forward. :smile:
