from pyradioconfig.parts.common.phys.phy_common import PHY_COMMON_FRAME_INTERNAL
from pyradioconfig.parts.ocelot.phys.Phys_Internal_Base_Experimental import PHYS_Internal_Base_Experimental_Ocelot
from pyradioconfig.parts.sol.phys.Phys_Studio_WiSUN_FSK import PHYS_IEEE802154_WiSUN_FSK_Sol
from pyradioconfig.parts.sol.phys.Phys_RAIL_Base_Standard_IEEE802154 import Phys_IEEE802154_Sol
class Phys_Internal_Base_Experimental_Sol(PHYS_Internal_Base_Experimental_Ocelot):

    def PHY_Internal_868MHz_ASK_100kbps(self, model, phy_name=None):
        pass

    def PHY_Internal_928M_2GFSK_250Kbps_125K(self, model, phy_name=None):
        pass

    def PHY_Internal_OQPSK_915M_1p2K_coh_FEC(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Longer Range Phy', phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.COHERENT
        phy.profile_inputs.agc_power_target.value = -11
        phy.profile_inputs.agc_scheme.value = model.vars.agc_scheme.var_enum.SCHEME_3
        phy.profile_inputs.asynchronous_rx_enable.value = False
        phy.profile_inputs.base_frequency_hz.value = 915000000
        phy.profile_inputs.baudrate_tol_ppm.value = 0
        phy.profile_inputs.bitrate.value = 1200 #Net bitrate(data only)
        phy.profile_inputs.channel_spacing_hz.value = 5000000
        phy.profile_inputs.crc_bit_endian.value = model.vars.crc_bit_endian.var_enum.MSB_FIRST
        phy.profile_inputs.crc_byte_endian.value = model.vars.crc_byte_endian.var_enum.MSB_FIRST
        phy.profile_inputs.crc_input_order.value = model.vars.crc_input_order.var_enum.LSB_FIRST
        phy.profile_inputs.crc_invert.value = False
        phy.profile_inputs.crc_pad_input.value = False
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.CCITT_16
        phy.profile_inputs.crc_seed.value = 0
        phy.profile_inputs.deviation.value = 4800
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = 226
        phy.profile_inputs.dsss_len.value = 8
        phy.profile_inputs.dsss_spreading_factor.value = 8
        phy.profile_inputs.fec_en.value = model.vars.fec_en.var_enum.FEC_154G_NRNSC_INTERLEAVING
        phy.profile_inputs.fixed_length_size.value = 1
        phy.profile_inputs.frame_bitendian.value = model.vars.frame_bitendian.var_enum.LSB_FIRST
        phy.profile_inputs.frame_coding.value = model.vars.frame_coding.var_enum.NONE
        phy.profile_inputs.frame_length_type.value = model.vars.frame_length_type.var_enum.VARIABLE_LENGTH
        phy.profile_inputs.frame_type_0_filter.value = True
        phy.profile_inputs.frame_type_0_length.value = 0
        phy.profile_inputs.frame_type_0_valid.value = False
        phy.profile_inputs.frame_type_1_filter.value = True
        phy.profile_inputs.frame_type_1_length.value = 0
        phy.profile_inputs.frame_type_1_valid.value = False
        phy.profile_inputs.frame_type_2_filter.value = True
        phy.profile_inputs.frame_type_2_length.value = 0
        phy.profile_inputs.frame_type_2_valid.value = False
        phy.profile_inputs.frame_type_3_filter.value = True
        phy.profile_inputs.frame_type_3_length.value = 0
        phy.profile_inputs.frame_type_3_valid.value = False
        phy.profile_inputs.frame_type_4_filter.value = True
        phy.profile_inputs.frame_type_4_length.value = 0
        phy.profile_inputs.frame_type_4_valid.value = False
        phy.profile_inputs.frame_type_5_filter.value = True
        phy.profile_inputs.frame_type_5_length.value = 0
        phy.profile_inputs.frame_type_5_valid.value = False
        phy.profile_inputs.frame_type_6_filter.value = True
        phy.profile_inputs.frame_type_6_length.value = 0
        phy.profile_inputs.frame_type_6_valid.value = False
        phy.profile_inputs.frame_type_7_filter.value = True
        phy.profile_inputs.frame_type_7_length.value = 0
        phy.profile_inputs.frame_type_7_valid.value = False
        phy.profile_inputs.frame_type_bits.value = 0
        phy.profile_inputs.frame_type_loc.value = 0
        phy.profile_inputs.frame_type_lsbit.value = 0
        phy.profile_inputs.frequency_comp_mode.value = model.vars.frequency_comp_mode.var_enum.DISABLED
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0
        phy.profile_inputs.header_calc_crc.value = False
        phy.profile_inputs.header_en.value = True
        phy.profile_inputs.header_size.value = 1
        phy.profile_inputs.header_white_en.value = False
        phy.profile_inputs.manchester_mapping.value = model.vars.manchester_mapping.var_enum.Default
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.OQPSK
        phy.profile_inputs.number_of_timing_windows.value = 8
        phy.profile_inputs.payload_crc_en.value = True
        phy.profile_inputs.payload_white_en.value = False
        phy.profile_inputs.preamble_length.value = 72
        phy.profile_inputs.preamble_pattern.value = 0
        phy.profile_inputs.preamble_pattern_len.value = 1
        phy.profile_inputs.rssi_period.value = 8
        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Custom_OQPSK
        phy.profile_inputs.shaping_filter_param.value = 0.0
        phy.profile_inputs.symbol_encoding.value = model.vars.symbol_encoding.var_enum.DSSS
        phy.profile_inputs.symbols_in_timing_window.value = 12
        phy.profile_inputs.syncword_0.value = 229
        phy.profile_inputs.syncword_1.value = 0
        phy.profile_inputs.syncword_length.value = 12
        phy.profile_inputs.syncword_tx_skip.value = False
        phy.profile_inputs.target_osr.value = 5
        phy.profile_inputs.test_ber.value = False
        phy.profile_inputs.timing_detection_threshold.value = 98
        phy.profile_inputs.timing_sample_threshold.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0
        phy.profile_inputs.var_length_adjust.value = 0
        phy.profile_inputs.var_length_bitendian.value = model.vars.var_length_bitendian.var_enum.LSB_FIRST
        phy.profile_inputs.var_length_byteendian.value = model.vars.var_length_byteendian.var_enum.LSB_FIRST
        phy.profile_inputs.var_length_includecrc.value = True
        phy.profile_inputs.var_length_maxlength.value = 127
        phy.profile_inputs.var_length_minlength.value = 5
        phy.profile_inputs.var_length_numbits.value = 8
        phy.profile_inputs.var_length_shift.value = 0
        phy.profile_inputs.white_output_bit.value = 0
        phy.profile_inputs.white_poly.value = model.vars.white_poly.var_enum.NONE
        phy.profile_inputs.white_seed.value = 0
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 4
        phy.profile_outputs.AGC_RSSISTEPTHR_DEMODRESTARTPER.override = 5
        phy.profile_outputs.AGC_RSSISTEPTHR_DEMODRESTARTTHR.override = 171
        phy.profile_outputs.AGC_RSSISTEPTHR_POSSTEPTHR.override = 3
        phy.profile_outputs.FRC_CONVGENERATOR_GENERATOR0.override = 109
        phy.profile_outputs.FRC_CONVGENERATOR_GENERATOR1.override = 79
        phy.profile_outputs.FRC_FECCTRL_CONVDECODEMODE.override = 1
        phy.profile_outputs.FRC_FECCTRL_CONVMODE.override = 1
        phy.profile_outputs.MODEM_AFC_AFCRXCLR_override = 1
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 2750
        phy.profile_outputs.MODEM_CGCLKSTOP_FORCEOFF.override = 7680
        phy.profile_outputs.MODEM_CTRL0_DUALCORROPTDIS.override = 0
        phy.profile_outputs.MODEM_CTRL1_PHASEDEMOD.override = 2
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 7
        phy.profile_outputs.MODEM_CTRL3_TSAMPDEL.override = 2
        phy.profile_outputs.MODEM_CTRL5_LINCORR.override = 1
        phy.profile_outputs.MODEM_CTRL6_ARW.override = 0
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT0.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT1.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT2.override = 1
        phy.profile_outputs.MODEM_CTRL6_RXBRCALCDIS.override = 1
        phy.profile_outputs.MODEM_TIMING_OFFSUBDEN.override = 5
        phy.profile_outputs.MODEM_TIMING_OFFSUBNUM.override = 12
        phy.profile_outputs.MODEM_TIMING_TIMSEQSYNC.override = 1
        phy.profile_outputs.MODEM_COH3_COHDSAEN.override = 0

        # Need to disable PREERRORS check for long timing windows (calculator sets it to half of symbol lenght)
        phy.profile_outputs.MODEM_PRE_PREERRORS.override = 15


        # Imported from .m file:

        # Need DSSCTD for all coherent setups
        phy.profile_outputs.MODEM_CTRL5_DSSSCTD.override = 1

        # Allow high frequency offset
        phy.profile_outputs.MODEM_CTRL6_CPLXCORREN.override = 1
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 0

        # Soft symbol FEC
        phy.profile_outputs.FRC_FECCTRL_CONVMODE.override = 1
        phy.profile_outputs.MODEM_CTRL0_DSSSDOUBLE.override = 1

        # Allowing errors in preamble/sync as payload uses FEC
        phy.profile_outputs.MODEM_CTRL1_SYNCERRORS.override = 2
        phy.profile_outputs.MODEM_PRE_PREWNDERRORS.override = 2

        # Configuring coherent operation
        phy.profile_outputs.MODEM_CTRL6_TDREW.override = 64
        phy.profile_outputs.MODEM_TIMING_TIMINGBASES.override = 12
        phy.profile_outputs.MODEM_CTRL3_TIMINGBASESGAIN.override = 1
        phy.profile_outputs.MODEM_TIMING_TIMTHRESH.override = 25
        phy.profile_outputs.MODEM_CTRL6_TIMTHRESHGAIN.override = 1
        phy.profile_outputs.MODEM_TIMING_ADDTIMSEQ.override = 14
        phy.profile_outputs.MODEM_CTRL5_FOEPREAVG.override = 7
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG0.override = 0
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG1.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG2.override = 2
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG3.override = 3
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG4.override = 4
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG5.override = 5
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG6.override = 6
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG7.override = 6
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_BBSS.override = 2
        phy.profile_outputs.MODEM_CTRL5_POEPER.override = 4
        phy.profile_outputs.MODEM_COH0_COHCHPWRRESTART.override = 1

        # Dynamic BBSS:
        phy.profile_outputs.MODEM_COH0_COHDYNAMICBBSSEN.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_AVGWIN.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_CHPWRACCUDEL.override = 3
        phy.profile_outputs.MODEM_LONGRANGE1_HYSVAL.override = 3
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH1.override = 3
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH2.override = 9
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH3.override = 15
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH4.override = 21
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH5.override = 27
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH6.override = 33
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH7.override = 39
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH8.override = 45
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH9.override = 51
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH10.override = 57
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH1.override = 0
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH2.override = 1
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH3.override = 2
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH4.override = 3
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH5.override = 4
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH6.override = 5
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH7.override = 6
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH8.override = 7
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH9.override = 8
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH10.override = 9
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH11.override = 10

        # Dynamic timing threshold
        phy.profile_outputs.MODEM_COH0_COHDYNAMICSYNCTHRESH.override = 0
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESHEN.override = 1
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESH.override = 0
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESH.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESHSEL.override = 0
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH0.override = 0
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = 3
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 63
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = 0
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = 73
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = 73
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH3.override = 144
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA0.override = 0
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA1.override = 0
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA2.override = 14
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA3.override = 0

        return phy

    def PHY_Internal_OQPSK_915Mhz_50kbps(self, model, phy_name=None):
        pass

    def PHY_Internal_2450M_CW_BW2520KHz_0K(self, model, phy_name=None):
        pass

    def PHY_RFSENSE_2450M_OOK_1kbps(self, model):
        pass

    def PHY_Internal_Test_Max_Sampling(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Internal Test Max Sampling', phy_name=phy_name)

        phy.profile_inputs.base_frequency_hz.value = 915000000
        phy.profile_inputs.if_frequency_hz.value = 1100000
        phy.profile_inputs.baudrate_tol_ppm.value = 0
        phy.profile_inputs.bitrate.value = 2000000
        phy.profile_inputs.bandwidth_hz.value = 2500000
        phy.profile_inputs.channel_spacing_hz.value = 1000000
        phy.profile_inputs.deviation.value = 500000
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = 0
        phy.profile_inputs.dsss_len.value = 0
        phy.profile_inputs.dsss_spreading_factor.value = 0
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.FSK2
        phy.profile_inputs.preamble_pattern.value = 1
        phy.profile_inputs.preamble_pattern_len.value = 2
        phy.profile_inputs.preamble_length.value = 40
        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Gaussian
        phy.profile_inputs.shaping_filter_param.value = 0.5
        phy.profile_inputs.syncword_0.value = 0xf68d
        phy.profile_inputs.syncword_1.value = 0x0
        phy.profile_inputs.syncword_length.value = 16
        phy.profile_inputs.tx_xtal_error_ppm.value = 0
        phy.profile_inputs.xtal_frequency_hz.value = 38400000
        phy.profile_inputs.symbols_in_timing_window.value = 14
        phy.profile_inputs.agc_period.value = 0
        phy.profile_inputs.agc_speed.value = model.vars.agc_speed.var_enum.FAST
        phy.profile_outputs.FEFILT0_SRC_SRCRATIO.override = 381981
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVX.override = 5
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVY.override = 17
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVN.override = 85
        model.vars.dec0.value_forced = 4
        model.vars.dec1.value_forced = 1
        model.vars.min_src2.value_forced = 0.6
        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.TRECS_VITERBI
        PHY_COMMON_FRAME_INTERNAL(phy, model)
        return phy

    # This is the 5 NA WiSUN PHY but with frequency planning enabled for the sim target
    # all other PHYs have frequency planning disabled to avoid changing PHYs that are already part of regression tests
    def PHY_Internal_Freq_Plan_Test(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_Internal_Freq_Plan_Test',
                            phy_name=phy_name, tags='-IC')
        # run the following PHY without
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA(model)

        return phy

    # This is the 5 NA WiSUN PHY but with frequency planning enabled for the sim target and fxo at 38 MHz to
    # get the maximum ratio for TXBR to verify interpolator implemenation on the FPGA
    def PHY_Internal_Freq_Plan_Test_Max_Interp(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_Internal_Freq_Plan_Test_Max_Interp',
                            phy_name=phy_name, tags='-IC')
        # run the following PHY without
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA(model)
        phy.profile_inputs.xtal_frequency_hz.value = 38000000

        return phy

    def PHY_Dual_Frontend_Test(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN OFDM OPTION 1',
                            phy_name=phy_name, tags='-IC')

        # updated for OFDM
        model.vars.ofdm_option.value_forced = model.vars.ofdm_option.var_enum.OPT1
        phy.profile_inputs.bitrate.value = 2400000  # set to the highest rate for given option # up to 2400 with MCS6
        phy.profile_inputs.channel_spacing_hz.value = 1200000
        phy.profile_inputs.bandwidth_hz.value = 1376000
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.OFDM
        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.adc_rate_mode.value = model.vars.adc_rate_mode.var_enum.FULLRATE
        phy.profile_inputs.xtal_frequency_hz.value = 39000000
        phy.profile_inputs.base_frequency_hz.value = 868000000

        # place holders for now
        phy.profile_inputs.baudrate_tol_ppm.value = 0
        phy.profile_inputs.deviation.value = 0
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = 0
        phy.profile_inputs.dsss_len.value = 0
        phy.profile_inputs.dsss_spreading_factor.value = 0
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0
        phy.profile_inputs.pll_bandwidth_tx.value = model.vars.pll_bandwidth_tx.var_enum.BW_2500KHz
        phy.profile_inputs.preamble_length.value = 2
        phy.profile_inputs.preamble_pattern.value = 1
        phy.profile_inputs.preamble_pattern_len.value = 2
        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Gaussian
        phy.profile_inputs.shaping_filter_param.value = 0.5
        phy.profile_inputs.symbol_encoding.value = model.vars.symbol_encoding.var_enum.NRZ
        phy.profile_inputs.syncword_0.value = 0
        phy.profile_inputs.syncword_1.value = 0
        phy.profile_inputs.syncword_length.value = 16
        phy.profile_inputs.tx_xtal_error_ppm.value = 0
        phy.profile_inputs.if_frequency_hz.value = 0

        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPGEAR.override = 4
        phy.profile_outputs.FEFILT1_DCCOMP_DCGAINGEAR.override = 10
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF0.override = 21
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF1.override = 80
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF2.override = 173
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF3.override = 256
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF4.override = 230
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF5.override = 7
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF6.override = -420
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF7.override = -890
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF8.override = -1082
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF9.override = -629
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF10.override = 675
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF11.override = 2704
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF12.override = 4961
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF13.override = 6736
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF14.override = 7409

        phy.profile_outputs.FEFILT0_CF_ADCBITORDERI.override = 0
        phy.profile_outputs.FEFILT0_CF_ADCBITORDERQ.override = 0
        phy.profile_outputs.FEFILT0_CF_DEC0.override = 5
        phy.profile_outputs.FEFILT0_CF_DEC1.override = 0
        phy.profile_outputs.FEFILT0_CHFCOE00_SET0COEFF0.override = 21
        phy.profile_outputs.FEFILT0_CHFCOE00_SET0COEFF1.override = 80
        phy.profile_outputs.FEFILT0_CHFCOE00_SET0COEFF2.override = 173
        phy.profile_outputs.FEFILT0_CHFCOE01_SET0COEFF3.override = 256
        phy.profile_outputs.FEFILT0_CHFCOE01_SET0COEFF4.override = 230
        phy.profile_outputs.FEFILT0_CHFCOE02_SET0COEFF5.override = 7
        phy.profile_outputs.FEFILT0_CHFCOE02_SET0COEFF6.override = 3676
        phy.profile_outputs.FEFILT0_CHFCOE03_SET0COEFF7.override = 3206
        phy.profile_outputs.FEFILT0_CHFCOE03_SET0COEFF8.override = 3014
        phy.profile_outputs.FEFILT0_CHFCOE04_SET0COEFF10.override = 675
        phy.profile_outputs.FEFILT0_CHFCOE04_SET0COEFF9.override = 15755
        phy.profile_outputs.FEFILT0_CHFCOE05_SET0COEFF11.override = 2704
        phy.profile_outputs.FEFILT0_CHFCOE05_SET0COEFF12.override = 4961
        phy.profile_outputs.FEFILT0_CHFCOE06_SET0COEFF13.override = 6736
        phy.profile_outputs.FEFILT0_CHFCOE06_SET0COEFF14.override = 7409
        phy.profile_outputs.FEFILT0_CHFCOE10_SET1COEFF0.override = 26
        phy.profile_outputs.FEFILT0_CHFCOE10_SET1COEFF1.override = 66
        phy.profile_outputs.FEFILT0_CHFCOE10_SET1COEFF2.override = 102
        phy.profile_outputs.FEFILT0_CHFCOE11_SET1COEFF3.override = 77
        phy.profile_outputs.FEFILT0_CHFCOE11_SET1COEFF4.override = 1973
        phy.profile_outputs.FEFILT0_CHFCOE12_SET1COEFF5.override = 1669
        phy.profile_outputs.FEFILT0_CHFCOE12_SET1COEFF6.override = 3331
        phy.profile_outputs.FEFILT0_CHFCOE13_SET1COEFF7.override = 3053
        phy.profile_outputs.FEFILT0_CHFCOE13_SET1COEFF8.override = 3154
        phy.profile_outputs.FEFILT0_CHFCOE14_SET1COEFF10.override = 1189
        phy.profile_outputs.FEFILT0_CHFCOE14_SET1COEFF9.override = 16162
        phy.profile_outputs.FEFILT0_CHFCOE15_SET1COEFF11.override = 3104
        phy.profile_outputs.FEFILT0_CHFCOE15_SET1COEFF12.override = 5087
        phy.profile_outputs.FEFILT0_CHFCOE16_SET1COEFF13.override = 6586
        phy.profile_outputs.FEFILT0_CHFCOE16_SET1COEFF14.override = 7145
        phy.profile_outputs.FEFILT0_CHFCTRL_CHFLATENCY.override = 0
        phy.profile_outputs.FEFILT0_CHFCTRL_FWSELCOEFF.override = 0
        phy.profile_outputs.FEFILT0_CHFCTRL_FWSWCOEFFEN.override = 0
        phy.profile_outputs.FEFILT0_CHFCTRL_SWCOEFFEN.override = 0
        phy.profile_outputs.FEFILT0_DCCOMP_DCCOMPEN.override = 1
        phy.profile_outputs.FEFILT0_DCCOMP_DCCOMPFREEZE.override = 0
        phy.profile_outputs.FEFILT0_DCCOMP_DCCOMPGEAR.override = 4
        phy.profile_outputs.FEFILT0_DCCOMP_DCESTIEN.override = 1
        phy.profile_outputs.FEFILT0_DCCOMP_DCGAINGEAR.override = 10
        phy.profile_outputs.FEFILT0_DCCOMP_DCGAINGEAREN.override = 1
        phy.profile_outputs.FEFILT0_DCCOMP_DCGAINGEARSMPS.override = 40
        phy.profile_outputs.FEFILT0_DCCOMP_DCLIMIT.override = 0
        phy.profile_outputs.FEFILT0_DCCOMP_DCRSTEN.override = 0
        phy.profile_outputs.FEFILT0_DCCOMPFILTINIT_DCCOMPINIT.override = 0
        phy.profile_outputs.FEFILT0_DCCOMPFILTINIT_DCCOMPINITVALI.override = 0
        phy.profile_outputs.FEFILT0_DCCOMPFILTINIT_DCCOMPINITVALQ.override = 0
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_DEC0GAIN.override = 0
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_DEC1GAIN.override = 0
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_DIGIGAIN.override = 0
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_DIGIGAINEN.override = 0
        phy.profile_outputs.FEFILT0_DIGMIXCTRL_DIGIQSWAPEN.override = 1
        phy.profile_outputs.FEFILT0_DIGMIXCTRL_DIGMIXFBENABLE.override = 1
        phy.profile_outputs.FEFILT0_DIGMIXCTRL_DIGMIXFREQ.override = 0
        phy.profile_outputs.FEFILT0_DIGMIXCTRL_MIXERCONJ.override = 0
        phy.profile_outputs.FEFILT0_SRC_SRCENABLE.override = 1
        phy.profile_outputs.FEFILT0_SRC_SRCRATIO.override = 766771
        phy.profile_outputs.FEFILT0_SRC_SRCSRD.override = 1

        phy.profile_outputs.FRC_FCD2_CALCCRC.override = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override = 0
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override = 1
        phy.profile_outputs.RAC_SCRATCH6_SCRATCH6.override = 1

        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override = -7
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override = -74
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override = -113
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override = -149
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override = -194
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override = -223
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override = -219
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override = -144
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override = 329
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override = 6
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override = 12

        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override = 1
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override = 2
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override = 250941

        phy.profile_outputs.RAC_TXOFDM_TXENBBREG.override = 1
        phy.profile_outputs.RAC_TXOFDM_TXENMIX.override = 1
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override = 1

        # AGC
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17  # Per Yang Gao 10/1/20
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2  # 25usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 960  # 960 STF cycle = 24 usec
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION0.override = 37  # PERIODHI-SETTLETIMEIF-1
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION1.override = 100
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION2.override = 100
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION3.override = 100
        phy.profile_outputs.AGC_HICNTREGION1_HICNTREGION4.override = 100
        phy.profile_outputs.AGC_AGCPERIOD0_MAXHICNTTHD.override = 100  # > PERIODHI means disabled
        phy.profile_outputs.AGC_STEPDWN_STEPDWN0.override = 1
        phy.profile_outputs.AGC_STEPDWN_STEPDWN1.override = 2
        phy.profile_outputs.AGC_STEPDWN_STEPDWN2.override = 2
        phy.profile_outputs.AGC_STEPDWN_STEPDWN3.override = 2
        phy.profile_outputs.AGC_STEPDWN_STEPDWN4.override = 2
        phy.profile_outputs.AGC_STEPDWN_STEPDWN5.override = 2
        # slow loop and RSSI
        phy.profile_outputs.AGC_CTRL0_DISCFLOOPADJ.override = 1
        phy.profile_outputs.AGC_CTRL0_CFLOOPNFADJ.override = 0
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 10
        phy.profile_outputs.AGC_GAINSTEPLIM0_HYST.override = 5
        phy.profile_outputs.AGC_CTRL0_PWRTARGET.override = 5
        phy.profile_outputs.AGC_CTRL1_PWRPERIOD.override = 2
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 3
        phy.profile_outputs.AGC_CTRL7_SUBDEN.override = 1
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 10
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1
        # AGC Settling Indicator
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200  # fast loop
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 330  # fast loop

        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVXDACSEL.override = 7

        return phy

    def PHY_Internal_PSMTest_2GFSK_PMDET_PMTIMLOSEN(self, model, phy_name=None):
        pass

    def PHY_Internal_PSMTest_2GFSK_PMDET_BCRDETECT(self, model, phy_name=None):
        pass

    def PHY_Internal_PSMTest_2GFSK_PHDSA(self, model, phy_name=None):
        pass

    def PHY_Internal_PSMTest_4GFSK_Legacy_PHDSA(self, model, phy_name=None):
        pass

    def PHY_Internal_Freq_Plan_Test_OFDM(self, model, phy_name=None):

        phy = Phys_IEEE802154_Sol.PHY_IEEE802154_SUN_OFDM_OPT1(self, model)
        return phy
