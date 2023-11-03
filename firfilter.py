class FIRFilter:

    # Use buffer to perform the convolution operation
    def __init__(self, _coefficients):
        self._coefficients = _coefficients
        self.buffer = [0] * len(_coefficients)

    def dofilter(self, value):
        self.buffer = [value] + self.buffer[:-1]
        result = 0
        for h, v in zip(self._coefficients, self.buffer):
            result = result + h * v
        # result = sum(c * v for c, v in zip(self._coefficients, self.buffer))
        return result

      
