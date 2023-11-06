from pyradioconfig.parts.ocelot.calculators.calc_synth import CALC_Synth_ocelot

class Calc_Synth_Sol(CALC_Synth_ocelot):

    def calc_adc_rate_mode_reg(self, model):

        #This function handles writes to the registers impacting ADC clock mode and HFXO multiplier
        adc_rate_mode = model.vars.adc_rate_mode.value

        if(model.vars.adc_rate_mode.var_enum.FULLRATE == adc_rate_mode):
            reg = 0
        elif (model.vars.adc_rate_mode.var_enum.HALFRATE == adc_rate_mode):            
            reg = 1
        else:
            # Eigthrate
            reg = 0 # really a don't care in this mode

        self._reg_write(model.vars.RFFPLL0_RFFPLLCTRL1_DIVXADCSEL, reg)

    def calc_lo_side_regs(self, model):
        """
        calculate LOSIDE register in synth and matching one in modem

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        model.vars.lo_injection_side.value = model.vars.lo_injection_side.var_enum.HIGH_SIDE  # default to high-side
        lo_injection_side = model.vars.lo_injection_side.value

        if lo_injection_side == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            loside = 1
        else:
            loside = 0

        # Write the registers
        self._reg_write(model.vars.SYNTH_IFFREQ_LOSIDE, loside)

    def calc_digmixctrl_regs(self, model):
        """
        calculate LOSIDE register in synth and matching one in modem

        Args:
            model (ModelRoot) : Data model to read and write variables from
        """
        fefilt_selected = model.vars.fefilt_selected.value
        lo_injection_side = model.vars.lo_injection_side.value

        if lo_injection_side == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            digiqswapen = 1
            mixerconj = 0
        else:
            digiqswapen = 0
            mixerconj = 1

        # Write the registers
        self._reg_write_by_name_concat(model, fefilt_selected, 'DIGMIXCTRL_DIGIQSWAPEN', digiqswapen)
        self._reg_write_by_name_concat(model, fefilt_selected, 'DIGMIXCTRL_MIXERCONJ', mixerconj)


    def calc_tx_mode(self, model):

        modulation_type = model.vars.modulation_type.value

        if modulation_type == model.vars.modulation_type.var_enum.OFDM:
            model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE2
        else:
            CALC_Synth_ocelot.calc_tx_mode(self,model)

    def calc_adc_freq_actual(self, model):
        #For Sol this has been moved to the calc_fpll file
        pass


