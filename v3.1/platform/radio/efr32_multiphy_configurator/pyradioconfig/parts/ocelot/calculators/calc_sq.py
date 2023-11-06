from pyradioconfig.calculator_model_framework.interfaces.icalculator import ICalculator
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum

class Calc_SQ_Ocelot(ICalculator):

    ###SIGNAL QUALIFIER CALCULATIONS###

    def buildVariables(self, model):
        self._addModelVariable(model, 'psm_max_sleep_us', int, ModelVariableFormat.DECIMAL, units='',
                               desc='Maximum time we can sleep in PSM mode including disable/enable times')
        var = self._addModelVariable(model, 'fast_detect_enable', Enum, ModelVariableFormat.DECIMAL,
                                     'Enable fast timing detection (for preamble sense and hopping applications)')
        member_data = [
            ['DISABLED', 0, 'Fast Detect Disabled'],
            ['ENABLED', 1, 'Fast Detect Enabled'],
        ]
        var.var_enum = CreateModelVariableEnum(
            'FastDetectEnum',
            'Fast Detect Enable/Disable Selection',
            member_data)

    def calc_fast_detect_enable(self, model):
        #Disable by default
        model.vars.fast_detect_enable.value = model.vars.fast_detect_enable.var_enum.DISABLED

    def calc_sq_timeout1_timeout2(self, model):
        #This function calculates the PSM timeout1 and timeout2 depending on demod configuration

        #Read in model variables
        demod_select = model.vars.demod_select.value
        delay_adc_to_demod = model.vars.delay_adc_to_demod.value #This is delay in sample rate at dec2 output
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)

        #Only calculate timeouts if fast detect is enabled
        if fast_detect_enable:
            if demod_select == model.vars.demod_select.var_enum.TRECS_VITERBI or demod_select == model.vars.demod_select.var_enum.TRECS_SLICER:
                trecs_pmacqingwin_actual = model.vars.pmacquingwin_actual.value
                phase_dsa_enabled = model.vars.MODEM_DSACTRL_DSAMODE.value
                trecs_pmdet_enabled = model.vars.MODEM_PHDMODCTRL_PMDETEN.value

                #PHDSA used for DSA detect
                if phase_dsa_enabled:
                    schprd = model.vars.MODEM_DSACTRL_SCHPRD.value
                    arrthd = model.vars.MODEM_DSACTRL_ARRTHD.value

                    symbols_in_schprd = 2*(schprd+1)
                    min_preamble_bits = symbols_in_schprd * arrthd

                    sqtimout = delay_adc_to_demod + min_preamble_bits # Set timeout1 from the DSA window
                    sqstg2timout = trecs_pmacqingwin_actual # Set timeout2 according to the CFE size

                #CFE used for DSA detect
                else:
                    min_preamble_bits = trecs_pmacqingwin_actual
                    sqtimout = delay_adc_to_demod + min_preamble_bits

                    if trecs_pmdet_enabled:
                        pmdetthd = model.vars.MODEM_PHDMODCTRL_PMDETTHD.value
                        # Between timeout1 and timeout2 we need pmdetthd bits
                        # Always use a value of at least 2 as 0 means "wait forever"
                        sqstg2timout = max(2,pmdetthd-min_preamble_bits)
                    else:
                        sqstg2timout = 0 #No separate preamble detect step

            elif demod_select == model.vars.demod_select.var_enum.LEGACY:
                phase_dsa_enabled = model.vars.MODEM_DSACTRL_DSAMODE.value
                symbols_in_timing_window = model.vars.symbols_in_timing_window.value
                number_of_timing_windows = model.vars.number_of_timing_windows.value

                # PHDSA used for DSA detect
                if phase_dsa_enabled:
                    schprd = model.vars.MODEM_DSACTRL_SCHPRD.value
                    arrthd = model.vars.MODEM_DSACTRL_ARRTHD.value

                    symbols_in_schprd = 2 * (schprd + 1)
                    min_preamble_bits = symbols_in_schprd * arrthd

                    sqtimout = delay_adc_to_demod + min_preamble_bits  # Set timeout1 from the DSA window
                    sqstg2timout = symbols_in_timing_window * number_of_timing_windows

            #Not yet calculating for other demods
            else:
                sqtimout = 0
                sqstg2timout = 0
        else:
            #Fast detect not enabled
            sqtimout = 0
            sqstg2timout = 0

        #Write the registers
        self._reg_write(model.vars.MODEM_SQ_SQTIMOUT, sqtimout)
        self._reg_write(model.vars.MODEM_SQEXT_SQSTG2TIMOUT, sqstg2timout)


    def calc_sq_timeout3(self, model):
        #This function calculates PSM timeout3

        #Read in model variables
        pmendschen = model.vars.MODEM_FRMSCHTIME_PMENDSCHEN.value
        preamble_length = model.vars.preamble_length.value #This is the TX preamble length
        syncword_length = model.vars.syncword_length.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)

        # Only calculate timeouts if fast detect is enabled
        if fast_detect_enable:
            # If we detect preamble quickly then we need to wait for preamble and syncword (plus some margin)
            sqstg3timout = int(preamble_length + syncword_length * 1.5)
        else:
            sqstg3timout = 0

        #Write the register
        self._reg_write(model.vars.MODEM_SQEXT_SQSTG3TIMOUT, sqstg3timout)

    def calc_psm_max_sleep_time(self, model):

        #Read in model variables
        preamble_length = model.vars.preamble_length.value #This is the TX preamble length
        sqtimout = model.vars.MODEM_SQ_SQTIMOUT.value
        sqstg2timout = model.vars.MODEM_SQEXT_SQSTG2TIMOUT.value
        baudrate = model.vars.baudrate.value
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)

        # Only calculate timeouts if fast detect is enabled
        if fast_detect_enable:
            #Calculate the max timeout
            psm_max_sleep_us = int((preamble_length - 2*sqtimout - sqstg2timout)/baudrate*1000000) #sleep time is in us
        else:
            psm_max_sleep_us = 0

        #Write the model variable
        model.vars.psm_max_sleep_us.value = max(0,psm_max_sleep_us) #Lower bound of 0

    def calc_sqen_reg(self, model):

        #Read in model variables
        fast_detect_enable = (model.vars.fast_detect_enable.value == model.vars.fast_detect_enable.var_enum.ENABLED)

        #Enable the signal qualifier when fast timing detection is enabled
        if fast_detect_enable:
            sqen_reg = 1
        else:
            sqen_reg = 0

        #Write the register
        self._reg_write(model.vars.MODEM_SQ_SQEN, sqen_reg)