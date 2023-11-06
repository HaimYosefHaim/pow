from pyradioconfig.parts.ocelot.calculators.calc_modulator import CALC_Modulator_Ocelot
from pycalcmodel.core.variable import ModelVariableFormat
from math import ceil,log2

class Calc_Modulator_Sol(CALC_Modulator_Ocelot):

    def buildVariables(self, model):
        super().buildVariables(model)
        self._addModelVariable(model, 'ofdm_rate_hz', float, ModelVariableFormat.DECIMAL,
                               desc='OFDM rate for softmodem')
        self._addModelVariable(model, 'softmodem_tx_interpolation1',int,ModelVariableFormat.DECIMAL,desc='interpolation rate 1 for softmodem TX')
        self._addModelVariable(model, 'softmodem_tx_interpolation2', int, ModelVariableFormat.DECIMAL,
                               desc='interpolation rate 2 for softmodem TX')

    def calc_softmodem_tx_interpolation(self, model):
        #This method calculates the interpolation rates for softmodem PHYs

        #Read in model vars
        demod_select = model.vars.demod_select.value
        ofdm_option = model.vars.ofdm_option.value

        #Set only when softmodem is used
        if demod_select == model.vars.demod_select.var_enum.SOFT_DEMOD:
            softmodem_tx_interpolation1 = 7 #Static for now

            if ofdm_option == model.vars.ofdm_option.var_enum.OPT1:
                softmodem_tx_interpolation2 = 2
            elif ofdm_option == model.vars.ofdm_option.var_enum.OPT2:
                softmodem_tx_interpolation2 = 4
            elif ofdm_option == model.vars.ofdm_option.var_enum.OPT3:
                softmodem_tx_interpolation2 = 8
            else:
                softmodem_tx_interpolation2 = 16

        else:
            softmodem_tx_interpolation1 = 0
            softmodem_tx_interpolation2 = 0

        model.vars.softmodem_tx_interpolation1.value = softmodem_tx_interpolation1
        model.vars.softmodem_tx_interpolation2.value = softmodem_tx_interpolation2


    def calc_int1cfg_reg(self, model):
        #This method calculates the int1cfg register fields

        #Read in model vars
        demod_select = model.vars.demod_select.value
        softmodem_tx_interpolation1 = model.vars.softmodem_tx_interpolation1.value

        # Set only when softmodem is used
        if demod_select == model.vars.demod_select.var_enum.SOFT_DEMOD:
            ratio = softmodem_tx_interpolation1-1
            gainshift = 12 #Static for now
        else:
            ratio=0
            gainshift=0

        #Write the registers
        self._reg_write(model.vars.TXFRONT_INT1CFG_RATIO,ratio)
        self._reg_write(model.vars.TXFRONT_INT1CFG_GAINSHIFT, gainshift)

    def calc_int2cfg_reg(self, model):
        #This method calculates the int2cfg register fields

        #Read in model vars
        demod_select = model.vars.demod_select.value
        softmodem_tx_interpolation2 = model.vars.softmodem_tx_interpolation2.value

        # Set only when softmodem is used
        if demod_select == model.vars.demod_select.var_enum.SOFT_DEMOD:
            ratio = softmodem_tx_interpolation2-1
            gainshift = ceil(log2(softmodem_tx_interpolation2**2))
        else:
            ratio = 0
            gainshift = 0

        #Write the registers
        self._reg_write(model.vars.TXFRONT_INT2CFG_RATIO, ratio)
        self._reg_write(model.vars.TXFRONT_INT2CFG_GAINSHIFT, gainshift)

    def calc_srccfg_ratio_reg(self, model):
        #This method calulates the softmodem SRCCFG RATIO value

        #Read in model vars
        demod_select = model.vars.demod_select.value
        dac_freq_actual = model.vars.dac_freq_actual.value
        baudrate = model.vars.baudrate.value
        softmodem_tx_interpolation1 = model.vars.softmodem_tx_interpolation1.value
        softmodem_tx_interpolation2 = model.vars.softmodem_tx_interpolation2.value

        # Set only when softmodem is used
        if demod_select == model.vars.demod_select.var_enum.SOFT_DEMOD:
            ratio = (2**18) * (2.0*baudrate*softmodem_tx_interpolation1*softmodem_tx_interpolation2)/dac_freq_actual #2^18 * (2*OFDM_RATE*INT1*INT2)/DAC_FREQ
        else:
            ratio = 0

        #Write the reg
        self._reg_write(model.vars.TXFRONT_SRCCFG_RATIO, int(ratio))