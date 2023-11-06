from pyradioconfig.parts.ocelot.calculators.calc_synth import CALC_Synth_ocelot
from enum import Enum
from pycalcmodel.core.variable import ModelVariableFormat, CreateModelVariableEnum

class Calc_Synth_Bobcat(CALC_Synth_ocelot):

    def buildVariables(self, model):
        """Populates a list of needed variables for this calculator
        Args:
            model (ModelRoot) : Builds the variables specific to this calculator
        """

        # Build variables from Lynx
        calc_synth_ocelot_obj = CALC_Synth_ocelot()
        calc_synth_ocelot_obj.buildVariables(model)

        # : Modify synth RX modes from Ocelot
        model.vars.synth_rx_mode.var_enum = CreateModelVariableEnum(
            enum_name='SynthRxModeEnum',
            enum_desc='Defined Synth RX Mode',
            member_data=[
                ['MODE1', 0, 'RX Mode 1'],
                ['MODE2', 1, 'RX Mode 2'],
            ])
        model.vars.synth_rx_mode_actual.var_enum = model.vars.synth_rx_mode.var_enum

        # : Modify synth settling modes from Ocelot
        model.vars.synth_settling_mode.var_enum = CreateModelVariableEnum(
            enum_name='SynthSettlingMode',
            enum_desc='Synth Settling Mode',
            member_data=[
                ['NORMAL', 0, 'Normal Operation Mode (Recommended)'],
                ['BLE_LR', 1, 'BLE Longrange Mode'],
            ])

        # : Modify tx synth modes from Ocelot
        model.vars.synth_tx_mode.var_enum = CreateModelVariableEnum(
            enum_name='SynthTxModeEnum',
            enum_desc='Defined Synth TX Mode',
            member_data=[
                ['MODE1', 0, 'TX Mode 1'],
                ['MODE2', 1, 'TX Mode 2'],
                ['MODE3', 2, 'TX Mode 3'],
                ['MODE4', 3, 'TX Mode 4'],
                ['MODE_BLE', 0, 'TX BLE Mode'],
                ['MODE_BLE_FULLRATE', 3, 'TX BLE Fullrate Mode'],
                ['MODE_IEEE802154', 2, 'TX IEEE802154 Mode'],
            ])
        model.vars.synth_tx_mode_actual.var_enum = model.vars.synth_tx_mode.var_enum

    def calc_synth_settling_mode(self, model):
        #Set synth settling mode to Normal for now
        model.vars.synth_settling_mode.value = model.vars.synth_settling_mode.var_enum.NORMAL

    def calc_rx_mode(self, model):
        synth_settling_mode = model.vars.synth_settling_mode.value

        if synth_settling_mode == model.vars.synth_settling_mode.var_enum.BLE_LR:
            model.vars.synth_rx_mode.value = model.vars.synth_rx_mode.var_enum.MODE1
        else:
            model.vars.synth_rx_mode.value = model.vars.synth_rx_mode.var_enum.MODE2

    def calc_tx_mode(self, model):
        baudrate = model.vars.baudrate.value
        modulation_type = model.vars.modulation_type.value

        # Set FSK and OQPSK settings based on baudrate
        if modulation_type == model.vars.modulation_type.var_enum.FSK2 or modulation_type == model.vars.modulation_type.var_enum.FSK4:
            if baudrate > 1250e3:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE2  # 1.5 MHz
            else:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE1  # 1 MHz
        elif modulation_type == model.vars.modulation_type.var_enum.OQPSK:
            if baudrate > 1250e3:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE3  # 2.5 MHz
            elif baudrate > 1000e3:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE2  # 1.5 MHz
            else:
                model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE1  # 1 MHz
        # Fixed settings for OOK, DBPSK, BPSK - transferred from Ocelot
        if modulation_type == model.vars.modulation_type.var_enum.DBPSK:
            model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE4  # 3 MHz
        elif modulation_type == model.vars.modulation_type.var_enum.BPSK:
            model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE3  # 2.5 MHz
        elif modulation_type == model.vars.modulation_type.var_enum.OOK:
            model.vars.synth_tx_mode.value = model.vars.synth_tx_mode.var_enum.MODE1  # 1000 kHz

    # overwrite this function from Ocelot to make VCODIV the default clock for ADC
    def calc_adc_clock_config(self, model):
        # This function calculates both the ADC mode (e.g. fullrate, halfrate, etc) as well as the ADC clock divider path

        # Load model values into local variables
        bandwidth_hz = model.vars.bandwidth_hz.value

        if (bandwidth_hz < 1.25e6):
            # 1/2 rate mode
            # Use the HFXO along with DPLL for the ADC clock
            adc_rate_mode = model.vars.adc_rate_mode.var_enum.HALFRATE
            adc_clock_mode = model.vars.adc_clock_mode.var_enum.VCODIV
        else:
            # Full rate mode
            # Use the divided down VCO for the ADC clock
            adc_rate_mode = model.vars.adc_rate_mode.var_enum.FULLRATE
            adc_clock_mode = model.vars.adc_clock_mode.var_enum.VCODIV

        # Load local variables back into model variables
        model.vars.adc_clock_mode.value = adc_clock_mode
        model.vars.adc_rate_mode.value = adc_rate_mode

    def calc_sylodivrloadcclk_reg(self, model):
        adc_rate_mode = model.vars.adc_rate_mode.value

        if adc_rate_mode == model.vars.adc_rate_mode.var_enum.HALFRATE:
            reg = 1
        else:
            reg = 0

        self._reg_write(model.vars.RAC_SYLOEN_SYLODIVRLOADCCLKSEL, reg)

    def calc_sytrim0_sychpcurrtx_reg(self, model):
        pass

    def calc_rx_mode_reg(self, model):

        rx_mode = model.vars.synth_rx_mode.value
        ind = rx_mode.value

        # Synth settings https://jira.silabs.com/browse/MCUW_RADIO_CFG-1529
        # Settings copied over from Lynx Assert
        # {workspace}\shared_files\lynx\radio_validation\ASSERTS
        # BLK_SYNTH_RX_LP_BW_200KHZ.csv (BLE_LR mode)
        # BLK_SYNTH_RX_LP_BW_250KHZ.csv (NORMAL mode)

        rx_mode_settings = {
            'SYNTH.LPFCTRL2RX.CASELRX':         [1,   1],
            'SYNTH.LPFCTRL2RX.CAVALRX':         [22,  16],
            'SYNTH.LPFCTRL2RX.CZSELRX':         [1,   1],
            'SYNTH.LPFCTRL2RX.CZVALRX':         [254, 229],
            'SYNTH.LPFCTRL2RX.CFBSELRX':        [0,   0],
            'SYNTH.LPFCTRL2RX.LPFGNDSWENRX':    [0,   0],
            'SYNTH.LPFCTRL2RX.MODESELRX':       [0,   0],
            'SYNTH.LPFCTRL1RX.OP1BWRX':         [0,   0],
            'SYNTH.LPFCTRL1RX.OP1COMPRX':       [7,   7],
            'SYNTH.LPFCTRL1RX.RFBVALRX':        [0,   0],
            'SYNTH.LPFCTRL1RX.RPVALRX':         [7,   7],
            'SYNTH.LPFCTRL1RX.RZVALRX':         [12,  13],
            'SYNTH.LPFCTRL2RX.LPFSWENRX':       [1,   1],
            'SYNTH.LPFCTRL2RX.LPFINCAPRX':      [2,   2]}

        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_CASELRX,          rx_mode_settings['SYNTH.LPFCTRL2RX.CASELRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_CAVALRX,          rx_mode_settings['SYNTH.LPFCTRL2RX.CAVALRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_CZSELRX,          rx_mode_settings['SYNTH.LPFCTRL2RX.CZSELRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_CZVALRX,          rx_mode_settings['SYNTH.LPFCTRL2RX.CZVALRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_CFBSELRX,         rx_mode_settings['SYNTH.LPFCTRL2RX.CFBSELRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_LPFGNDSWENRX,     rx_mode_settings['SYNTH.LPFCTRL2RX.LPFGNDSWENRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_MODESELRX,        rx_mode_settings['SYNTH.LPFCTRL2RX.MODESELRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL1RX_OP1BWRX,          rx_mode_settings['SYNTH.LPFCTRL1RX.OP1BWRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL1RX_OP1COMPRX,        rx_mode_settings['SYNTH.LPFCTRL1RX.OP1COMPRX'][ind] )
        self._reg_write(model.vars.SYNTH_LPFCTRL1RX_RFBVALRX,         rx_mode_settings['SYNTH.LPFCTRL1RX.RFBVALRX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1RX_RPVALRX,          rx_mode_settings['SYNTH.LPFCTRL1RX.RPVALRX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1RX_RZVALRX,          rx_mode_settings['SYNTH.LPFCTRL1RX.RZVALRX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_LPFSWENRX,        rx_mode_settings['SYNTH.LPFCTRL2RX.LPFSWENRX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2RX_LPFINCAPRX,       rx_mode_settings['SYNTH.LPFCTRL2RX.LPFINCAPRX'][ind])

    def calc_tx_mode_reg(self, model):

        tx_mode = model.vars.synth_tx_mode.value
        ind = tx_mode.value

        # Synth settings https://jira.silabs.com/browse/MCUW_RADIO_CFG-1529
        # Settings copied over from Lynx Assert
        # {workspace}\shared_files\lynx\radio_validation\ASSERTS
        # BLK_SYNTH_TX_BW_1000KHZ.csv (MODE 1)
        # BLK_SYNTH_TX_BW_1500KHZ.csv (MODE 2)
        # BLK_SYNTH_TX_BW_2500KHZ.csv (MODE 3)
        # BLK_SYNTh_TX_BW_3000KHZ.csv (MODE 4)

        tx_mode_settings = {
            'SYNTH.LPFCTRL2TX.CASELTX':         [1,   1,   1,   1],
            'SYNTH.LPFCTRL2TX.CAVALTX':         [15,  8,   4,   2],
            'SYNTH.LPFCTRL2TX.CZSELTX':         [1,   1,   1,   1],
            'SYNTH.LPFCTRL2TX.CZVALTX':         [126, 70,  22,  6],
            'SYNTH.LPFCTRL2TX.CFBSELTX':        [0,   0,   0,   0],
            'SYNTH.LPFCTRL2TX.LPFGNDSWENTX':    [0,   0,   0,   0],
            'SYNTH.LPFCTRL2TX.MODESELTX':       [0,   0,   0,   0],
            'SYNTH.LPFCTRL1TX.OP1BWTX':         [0,   5,   11,  15],
            'SYNTH.LPFCTRL1TX.OP1COMPTX':       [13,  13,  14,  15],
            'SYNTH.LPFCTR1TX.RFBVALTX':         [0,   0,   0,   0],
            'SYNTH.LPFCTRL1TX.RPVALTX':         [0,   0,   0,   0],
            'SYNTH.LPFCTRL1TX.RZVALTX':         [0,   3,   9,   11],
            'SYNTH.LPFCTRL2TX.LPFSWENTX':       [1,   1,   1,   1],
            'SYNTH.LPFCTRL2TX.LPFINCAPTX':      [2,   2,   2,   2]}

        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_CASELTX,            tx_mode_settings['SYNTH.LPFCTRL2TX.CASELTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_CAVALTX,            tx_mode_settings['SYNTH.LPFCTRL2TX.CAVALTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_CZSELTX,            tx_mode_settings['SYNTH.LPFCTRL2TX.CZSELTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_CZVALTX,            tx_mode_settings['SYNTH.LPFCTRL2TX.CZVALTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_CFBSELTX,           tx_mode_settings['SYNTH.LPFCTRL2TX.CFBSELTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_LPFGNDSWENTX,       tx_mode_settings['SYNTH.LPFCTRL2TX.LPFGNDSWENTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_MODESELTX,          tx_mode_settings['SYNTH.LPFCTRL2TX.MODESELTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1TX_OP1BWTX,            tx_mode_settings['SYNTH.LPFCTRL1TX.OP1BWTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1TX_OP1COMPTX,          tx_mode_settings['SYNTH.LPFCTRL1TX.OP1COMPTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1TX_RFBVALTX,           tx_mode_settings['SYNTH.LPFCTR1TX.RFBVALTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1TX_RPVALTX,            tx_mode_settings['SYNTH.LPFCTRL1TX.RPVALTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL1TX_RZVALTX,            tx_mode_settings['SYNTH.LPFCTRL1TX.RZVALTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_LPFSWENTX,          tx_mode_settings['SYNTH.LPFCTRL2TX.LPFSWENTX'][ind])
        self._reg_write(model.vars.SYNTH_LPFCTRL2TX_LPFINCAPTX,         tx_mode_settings['SYNTH.LPFCTRL2TX.LPFINCAPTX'][ind])

    def calc_boostlna_reg(self, model):

        #Read in model vars
        lo_injection_side = model.vars.lo_injection_side.value

        # Calculating the boostlna value
        if lo_injection_side == model.vars.lo_injection_side.var_enum.HIGH_SIDE:
            boostlna = 1
        else:
            boostlna = 0

        # Write the register
        self._reg_write(model.vars.AGC_LNABOOST_BOOSTLNA, boostlna)
        
    def calc_hfxo_retiming_table(self, model):
        # Inherit Ocelot retiming
        super().calc_hfxo_retiming_table(model)

        #setting for 2x HFXO frequency
        self.retime_print("calculating 2x HFXO freq")
        model.vars.lut_table_index.value.append(0)
        self.retime_main(model, model.vars.xtal_frequency_hz.value * 2, 1, model.vars.lut_table_index.value[0])

