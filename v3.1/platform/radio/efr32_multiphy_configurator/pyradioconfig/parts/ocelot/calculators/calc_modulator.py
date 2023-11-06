from pyradioconfig.parts.common.calculators.calc_modulator import CALC_Modulator
from pyradioconfig.calculator_model_framework.Utils.CustomExceptions import CalculationException

class CALC_Modulator_Ocelot(CALC_Modulator):

    def calc_txbr_value(self, model):
        #Overriding this function due to variable name change

        #Load model values into local variables
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        baudrate = model.vars.baudrate.value

        #calculate baudrate to fxo ratio
        #For the phase modulator this should always be based on xtal rate (https://jira.silabs.com/browse/MCUW_RADIO_CFG-1626)
        ratio = xtal_frequency_hz / (8.0 * baudrate)

        #Load local variables back into model variables
        model.vars.txbr_ratio.value = ratio

    def calc_tx_baud_rate_actual(self, model):
        #Overriding this function due to variable name change

        #Load model values into local variables
        xtal_frequency_hz = model.vars.xtal_frequency_hz.value
        txbr_ratio = model.vars.txbr_ratio_actual.value

        tx_baud_rate = xtal_frequency_hz / (8.0 * txbr_ratio)

        #Load local variables back into model variables
        model.vars.tx_baud_rate_actual.value = tx_baud_rate

    #Class variable to store the max PA value (needs to be correct for full power output)
    max_pa_value = (63 << 2)

    def calc_modindex_value(self, model):
        #Overriding this function due to variable name change

        hardmodem_freq_actual = model.vars.hardmodem_freq_actual.value * 1.0
        modformat = model.vars.modulation_type.value
        freq_dev_hz = model.vars.deviation.value * 1.0
        synth_res = model.vars.synth_res_actual.value
        shaping_filter_gain = model.vars.shaping_filter_gain_actual.value
        interpolation_gain = model.vars.interpolation_gain_actual.value

        if modformat == model.vars.modulation_type.var_enum.FSK2 or \
           modformat == model.vars.modulation_type.var_enum.MSK or \
           modformat == model.vars.modulation_type.var_enum.FSK4:
            modindex = freq_dev_hz * 16.0 / (synth_res * shaping_filter_gain * interpolation_gain)

        elif modformat == model.vars.modulation_type.var_enum.OQPSK:
            modindex = hardmodem_freq_actual / (synth_res * 2 * shaping_filter_gain * interpolation_gain)

        elif modformat == model.vars.modulation_type.var_enum.OOK or \
                modformat == model.vars.modulation_type.var_enum.ASK or \
                modformat == model.vars.modulation_type.var_enum.BPSK or \
                modformat == model.vars.modulation_type.var_enum.DBPSK:
            modindex = self.max_pa_value * 16.0 / (shaping_filter_gain * interpolation_gain)
        else:
            modindex = 0.0  # don't care in OFDM

        model.vars.modindex.value = modindex

    def calc_tx_freq_dev_actual(self, model):
        """
        given register setting return actual frequency deviation used in the modulator
        Using Equations in Table 5.25 of EFR32 Reference Manual (internal.pdf)

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """

        modformat = model.vars.modulation_type.value
        modindex = model.vars.modindex_actual.value
        synth_res = model.vars.synth_res_actual.value
        shaping_filter_gain = model.vars.shaping_filter_gain_actual.value
        interpolation_gain = model.vars.interpolation_gain_actual.value

        if modformat == model.vars.modulation_type.var_enum.FSK2 or \
           modformat == model.vars.modulation_type.var_enum.MSK or \
           modformat == model.vars.modulation_type.var_enum.FSK4:
            freq_dev_hz = modindex * (synth_res * shaping_filter_gain * interpolation_gain) / 16.0
        else:
            freq_dev_hz = 0.0

        model.vars.tx_deviation_actual.value = freq_dev_hz

    def calc_symbol_rates_actual(self, model):
        encoding = model.vars.symbol_encoding.value
        encodingEnum = model.vars.symbol_encoding.var_enum
        demod_select = model.vars.demod_select.value

        baud_per_symbol = 1

        if demod_select == model.vars.demod_select.var_enum.LONGRANGE:
            # In case of BLE LR 125 kps, baud_per_symbol is 8
            if model.vars.FRC_CTRL_RATESELECT.value == 0:
                baud_per_symbol = 8
            # In case of BLE LR 500 kps, baud_per_symbol is 2
            elif model.vars.FRC_CTRL_RATESELECT.value == 2:
                baud_per_symbol = 2
            else:
                raise ValueError("Invalid FRC_CTRL_RATESELECT value used in LONGRANGE configuration")
        if model.vars.FRC_CTRL_RATESELECT.value == 1:
            encoding = model.vars.MODEM_CTRL6_CODINGB
        if encoding == encodingEnum.LINECODE:
            baud_per_symbol *= 4
        if encoding == encodingEnum.DSSS:
            baud_per_symbol *= model.vars.dsss_len.value
        elif encoding == encodingEnum.Manchester:
            baud_per_symbol *= 2
        model.vars.baud_per_symbol_actual.value = baud_per_symbol

        if encoding == encodingEnum.DSSS:
            bits_per_symbol = model.vars.dsss_bits_per_symbol.value
        else:
            modFormat = model.vars.modulation_type.value
            modFormatEnum = model.vars.modulation_type.var_enum
            if modFormat in [modFormatEnum.FSK4, modFormatEnum.OQPSK]:
                bits_per_symbol = 2
            else:
                bits_per_symbol = 1
        model.vars.bits_per_symbol_actual.value = bits_per_symbol

    def calc_txbases_reg(self, model):

        #Read in model variables
        preamble_length = model.vars.preamble_length.value #This is the TX preamble length
        preamble_pattern_len_actual = model.vars.preamble_pattern_len_actual.value

        #Calculate txbases
        txbases = preamble_length / preamble_pattern_len_actual

        #Limit checking
        if (txbases) > 0xffff:
            raise CalculationException("Calculated TX preamble sequences (TXBASE) value of %s exceeds limit of 65535! Adjust preamble inputs." % txbases )

        #Write the register
        self._reg_write(model.vars.MODEM_PRE_TXBASES, int(txbases))
