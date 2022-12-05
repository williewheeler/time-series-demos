import math
import numpy as np
import pandas as pd


class EwmaBatchDetector:
    """Anomaly detection based on the exponentially weighted moving average.
    
    Attributes:
        alpha: A float current weight in (0.0, 1.0]
        k: A float band multiplier
        min_periods: A nonnegative int training period
    
    Typical usage example:
    
        ewma = EwmaBatchDetector(alpha=0.2, k=3.0, min_periods=5)
    """
    
    # Shouldn't alpha=0.0 be permissible? May have to implement it myself.
    def __init__(self, alpha=0.5, k=3.0, min_periods=1):
        """Initializes a new EWMA batch detector.

        Args:
            alpha: A float current weight in (0.0, 1.0]
            k: A float band multiplier
            min_periods: A nonnegative int training period
        """
        
        self.alpha = alpha
        self.k = k
        self.min_periods = min_periods

    def detect(self, x):
        """Runs the detector on the given series

        Args:
            x: A pandas Series containing the time series data

        Returns:
            A pandas DataFrame containing anomaly detection results
        """

        ewm = x.shift().ewm(alpha=self.alpha, min_periods=self.min_periods)
        return _to_result(x, ewm.mean(), ewm.std(bias=True), self.k)


class PewmaBatchDetector:
    """Anomaly detection based on the probabilistic exponentially weighted moving average.
    
    Based on Probabilistic Reasoning for Streaming Anomaly Detection
    (https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.375.2193&rep=rep1&type=pdf)
    
    Attributes:
        alpha: A float current weight in (0.0, 1.0]. Note that this is the reverse of what's
            in the paper (i.e., they use alpha for the history weight).
        beta: A float probability weight in [0.0, 1.0], applied to alpha
        k: A float band multiplier
        min_periods: An nonnegative int training period

    Typical usage example:
    
        pewma = PewmaBatchDetector(alpha=0.2, beta=0.9, k=3.0, min_periods=5)
    """
    
    def __init__(self, alpha=0.5, beta=0.5, k=3.0, min_periods=1):
        """Initializes a new PEWMA batch detector.

        Args:
            alpha: A float current weight in (0.0, 1.0]. Note that this is the reverse of what's
                in the paper (i.e., they use alpha for the history weight).
            beta: A float probability weight in [0.0, 1.0], applied to alpha
            k: A float band multiplier
            min_periods: An nonnegative int training period
        """
        
        self.alpha = alpha
        self.beta = beta
        self.k = k
        self.min_periods = min_periods

    # FIXME Not correctly incorporating the training period.
    # Notice that the stdev starts tight even with training.
    def detect(self, x):
        """Runs the detector on the given series

        Args:
            x: A pandas Series containing the time series data

        Returns:
            A pandas DataFrame containing anomaly detection results
        """

        PR_DENOM = math.sqrt(2.0 * math.pi)

        # Flip this to match pandas EWMA.
        # So alpha is the weight for the most recent value, and gamma
        # is the weight for the most recent estimate (i.e., history).
        gamma = 1.0 - self.alpha

        n = len(x)
        s1 = x[0]
        s2 = x[0] * x[0]
        mean = np.repeat(x[0], n)
        std = np.repeat(0.0, n)

        for t in range(1, n):
            if t < self.min_periods:
                gamma_t = 1.0 - 1.0 / t
            elif std[t-1] == 0:
                gamma_t = gamma
            else:
                # Use z-score to calculate probability
                z = (x[t-1] - mean[t-1]) / std[t-1]
                p = np.exp(-0.5 * z * z) / PR_DENOM
                gamma_t = (1.0 - self.beta * p) * gamma

            s1 = gamma_t * s1 + (1.0 - gamma_t) * x[t-1]
            s2 = gamma_t * s2 + (1.0 - gamma_t) * x[t-1] * x[t-1]
            mean[t] = s1
            std[t] = math.sqrt(s2 - s1 * s1)

        return _to_result(x, mean, std, self.k)


def _to_result(x, mean, std, k):
    upper = mean + k * std
    lower = mean - k * std
    anom = (x < lower) | (x > upper)
    return pd.DataFrame({
        "x": x,
        "mean": mean,
        "stdev": std,
        "upper": upper,
        "lower": lower,
        "anomaly": anom,
    })
