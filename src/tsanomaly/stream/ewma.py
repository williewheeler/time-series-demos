import math

class EwmaStreamingDetector:
    PR_DENOM = sqrt(2.0 * pi)

    def __init__(self, alpha, k):
        self.alpha = alpha
        self.k = k
        self.s1 = None
        self.s2 = 0
    
    def detect(self, x):
        if self.s1 == None:
            self.s1 = x
            self.s2 = x * x
            result = None
        else:
            m = self.s1
            s = math.sqrt(self.s2 - self.s1 * self.s1)
            result = math.abs(x - m) > k * s:
            m = alpha * x + (1.0 - alpha) * m
            s = alpha * x * x + (1.0 - alpha) * s
        return result
