
from . import Transformer
import logging

class Simple(Transformer):
    """
    Simple Transformers always have a simple input output relation with a
    constant efficiency
    """
    model_param = {'linear_constr': ('io_relation', 'out_max'),
                   'milp_constr' : (),
                   'objective' : ('cvar', 'cfix', 'cfuel', 'rsell'),
                   'investment': False}
    lower_name = 'simple_transformer'

    def __init__(self, **kwargs):
        """
        :param eta: eta as constant efficiency for simple transformer
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', None)


class CHP(Transformer):
    """
    A CombinedHeatPower Transformer always has a simple input output relation
    with a constant efficiency
    """
    model_param = {'linear_constr': ('io_relation', 'out_max',
                                     'simple_chp_relation'),
                   'milp_constr' : (),
                   'objective' : ('cvar', 'cfix', 'cfuel', 'rsell'),
                   'investment': False}
    lower_name = "simple_chp"

    def __init__(self, **kwargs):
        """
        :param eta: eta as constant efficiency for simple transformer
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', [None, None])

class SimpleExtractionCHP(Transformer):
    """
    Class for combined heat and power unit with extraction turbine and constant
    efficiencies

    """
    model_param = {'linear_constr': ('in_max', 'out_max',
                                     'simple_extraction_relation'),
                   'milp_constr' : (),
                   'objective' : ('cvar', 'cfix', 'cfuel', 'rsell'),
                   'investment': False}
    lower_name = "simple_extraction_chp"

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------
        eta : eta as constant efficiency for transformer output
        beta : power loss index (max: at full load, min: at minimal load)
        sigma : power to heat ratio P/Q
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', [None, None])
        self.beta = kwargs.get('beta', None)
        self.sigma = kwargs.get('sigma', None)


class Storage(Transformer):
    """
    """
    model_param = {'investment': False}

    lower_name = "simple_storage"

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------
        cap_max : maximal sate of charge
        cap_min : minimum state of charge
        cap_initial : state of charge at timestep 0 (default cap_max*0.5)
        add_cap_limit : limit of additional installed capacity (only investment
        models)
        eta_in : efficiency at charging
        eta_out : efficiency at discharging
        cap_loss : capacity loss per timestep in p/100
        c_rate_in : c-rate for charging (unit is s^-1)
        c_rate_out : c-rate for discharging (unit is s^-1)
        """
        super().__init__(**kwargs)

        self.cap_max = kwargs.get('cap_max', None)
        self.cap_min = kwargs.get('cap_min', None)
        self.add_cap_limit = kwargs.get('add_cap_limit', None)
        self.cap_initial = kwargs.get('cap_initial', None)
        if self.cap_initial is None:
            self.cap_initial = self.cap_max*0.5
        logging.info('No initial storage capacity set. Setting capacity to' +
                     ' 0.5 of max. capacity for component: %s', self.uid)
        self.eta_in = kwargs.get('eta_in', 1)
        self.eta_out = kwargs.get('eta_out', 1)
        self.cap_loss = kwargs.get('cap_loss', 0)
        self.c_rate_in = kwargs.get('c_rate_in', None)
#        if self.c_rate_in is None:
#            self.c_rate_in = next(iter(self.in_max.values())) / self.cap_max
        self.c_rate_out = kwargs.get('c_rate_out', None)
#        if self.c_rate_out is None:
#            self.c_rate_out = next(iter(self.out_max.values())) / self.cap_max
