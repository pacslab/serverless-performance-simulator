import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, poisson

from Utility import convert_hist_pdf

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)
# warnings.simplefilter(action='ignore', category=NotImplementedError)
# import modin.pandas as pd

class ArrivalProcess:
    def __init__(self, *args, **kwargs):
        # if your class has pdf or cdf functions, switch the booleans to True
        self.has_pdf = False
        self.has_cdf = False

    def generate_inter_arrival(self):
        raise NotImplementedError

    def visualize_histogram(self, num_traces=10000, num_bins=100):
        traces = np.array([self.generate_inter_arrival() for i in range(num_traces)])
        print(f"Simulated Average Inter-Arrival Time: {np.mean(traces):.6f}")
        print(f"Simulated Average Arrival Rate: {num_traces / np.sum(traces):.6f}")

        base, hist_values, cumulative = convert_hist_pdf(traces, num_bins)

        plt.figure()
        plt.plot(base, hist_values, label='Sim Hist')
        if self.has_pdf:
            pdf_vals = np.array([0] + [self.pdf(x) for x in base[1:]])
            plt.plot(base, pdf_vals, ls='--', label="Model PDF")
        plt.legend()
        plt.grid(True)

        plt.figure()
        plt.plot(base, cumulative, label='Sim Cumulative')
        if self.has_cdf:
            cdf_vals = np.array([0] + [self.cdf(x) for x in base[1:]])
            plt.plot(base, cdf_vals, ls='--', label="Model CDF")
        plt.legend()
        plt.grid(True)


class ExponentialArrivalProcess(ArrivalProcess):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_pdf = True
        self.has_cdf = True

        _rps = kwargs.get('rps')
        if _rps is None:
            raise Exception("You need to provied a request rate!")
        self.rps = _rps

    def pdf(self, x):
        return expon.pdf(x, scale=1/self.rps)

    def cdf(self, x):
        return expon.cdf(x, scale=1/self.rps)

    def generate_inter_arrival(self):
        return np.random.exponential(1/self.rps)

if __name__ == "__main__":
    exp_arr = ExponentialArrivalProcess(rps=5)
    exp_arr.visualize_histogram(num_traces=10000, num_bins=100)
    plt.show()