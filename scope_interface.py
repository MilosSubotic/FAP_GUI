from abc import ABC, abstractmethod

class Scope(ABC):
    @abstractmethod
    def set(self, mode, sample_rate, record_length, CH_ranges, CH_couplings, trigger_source):
        pass

    @abstractmethod
    def getBlock(self):
        pass

    @abstractmethod
    def getBlockS(self):
        pass

    @abstractmethod
    def set_trigger(self, trigger_source):
        pass
    
