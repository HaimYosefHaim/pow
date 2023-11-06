from . import ExporterModel
from . import WTIMER_model
from . import RuntimeModel


class WTIMER(ExporterModel.Module):
    def __init__(self, name=None):
        if not name:
            name = self.__class__.__name__
        super(WTIMER, self).__init__(name, visible=True, core=True)
        self.model = WTIMER_model

    def set_runtime_hooks(self):
        pass
