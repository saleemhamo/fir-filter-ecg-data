from abc import abstractmethod


class FilterDesign:

    @abstractmethod
    def highpass_design(self, sampling_rate, f1):
        pass

    def band_stop_design(self, sampling_rate, f1, f2):
        pass
