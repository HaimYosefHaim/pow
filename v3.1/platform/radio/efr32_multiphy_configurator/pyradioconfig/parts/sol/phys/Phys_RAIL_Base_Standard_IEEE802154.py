from pyradioconfig.parts.ocelot.phys.Phys_RAIL_Base_Standard_IEEE802154 import PHYS_IEEE802154_Ocelot
from pyradioconfig.parts.common.phys.phy_common import PHY_COMMON_FRAME_154
from pyradioconfig.parts.lynx.phys.Phys_IEEE802154 import PHYS_IEEE802154_Lynx
from pyradioconfig.parts.common.phys.phy_common import PHY_COMMON_FRAME_INTERNAL
from pyradioconfig.parts.panther.phys.PHY_internal_base import Phy_Internal_Base

from py_2_and_3_compatibility import *

class Phys_IEEE802154_Sol(PHYS_IEEE802154_Ocelot):

    def PHY_IEEE802154_780MHz_OQPSK(self, model):
        pass

    def PHY_IEEE802154_868MHz_BPSK(self, model):
        pass

    def PHY_IEEE802154_868MHz_BPSK_coh(self, model):
        pass

    def PHY_IEEE802154_868MHz_OQPSK(self, model):
        pass

    def PHY_IEEE802154_868MHz_OQPSK_coh(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 868MHz OQPSK Coherent Demod',
                            phy_name=phy_name)

        self.IEEE802154_915MHz_OQPSK(phy, model)
        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.COHERENT
        phy.profile_inputs.base_frequency_hz.value = long(868300000)
        phy.profile_inputs.bitrate.value = 100000
        # phy.profile_inputs.if_frequency_hz.value = 500000
        phy.profile_inputs.deviation.value = 100000
        phy.profile_inputs.dsss_spreading_factor.value = 4
        phy.profile_inputs.dsss_len.value = 16
        phy.profile_inputs.bandwidth_hz.value = 504960

        phy.profile_inputs.target_osr.value = 5  # Calc SRC

        # : AFC (Automatic Frequency Control) compensation limit
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 1536  # : 15.36 kHz

        # : Controls frequency/amplitude offset compensation.
        phy.profile_outputs.MODEM_CTRL1_COMPMODE.override = 0  # Disable compensation
        # : Defines modulation method for OQPSK
        phy.profile_outputs.MODEM_CTRL1_PHASEDEMOD.override = 2  # : 2 - COH
        phy.profile_outputs.MODEM_CTRL1_RESYNCPER.override = 1  #### has input var for resyncper
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 7  #### remove if you can - related to xo freq chnage # TODO: remove
        # : Baseband signal selection - determines number of LSB discarded before signal is used for detection.
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_BBSS.override = 4  # : TODO Investigation original 5 - NO EFFECT
        phy.profile_outputs.MODEM_CTRL5_DSSSCTD.override = 1
        phy.profile_outputs.MODEM_CTRL5_FOEPREAVG.override = 7  # : TODO potential investigation original 7
        phy.profile_outputs.MODEM_CTRL5_POEPER.override = 1
        phy.profile_outputs.MODEM_CTRL6_ARW.override = 1
        # : Controls number of bauds to rewind after fixed window timing detection.
        phy.profile_outputs.MODEM_CTRL6_TDREW.override = 32  #### look up - probably not related
        # : Disable RX baudrate calculation used by AGC. Instead assume OSR = 2 * RXBRFRAC
        phy.profile_outputs.MODEM_CTRL6_RXBRCALCDIS.override = 1

        # phy.profile_outputs.MODEM.DIGMIXCTRL.DIGMIXFBENABLE.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG0.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG1.override = 2
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG2.override = 4
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG3.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_AVGWIN.override = 3 # : improves sensitivity
        phy.profile_outputs.MODEM_LONGRANGE1_CHPWRACCUDEL.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_HYSVAL.override = 3
        phy.profile_outputs.MODEM_LONGRANGE1_LRTIMEOUTTHD.override = 160

        phy.profile_outputs.MODEM_PRE_PREERRORS.override = 15
        phy.profile_outputs.MODEM_DSACTRL_ARRTHD.override = 4  # Was missed

        phy.profile_outputs.MODEM_LONGRANGE1_PREFILTLEN.override = 3
        phy.profile_outputs.MODEM_PREFILTCOEFF_PREFILTCOEFF.override = 2736235287

        # : trim bits after the freq discriminator
        phy.profile_outputs.MODEM_COH3_CDSS.override = 4

        """ Channel Power Lock Settings """
        # : 0 - Channel power is locked when timing is detected
        # : 1 - Channel power is locked when DSA is detected
        phy.profile_outputs.MODEM_COH0_COHCHPWRLOCK.override = 0
        # : Set to enable automatic restart of channel power - needed to make sure channel power is not dependent on
        # : power of received frames
        phy.profile_outputs.MODEM_COH0_COHCHPWRRESTART.override = 1

        """ Complex Correlation """
        phy.profile_outputs.MODEM_CTRL6_CPLXCORREN.override = 1
        phy.profile_outputs.MODEM_COH3_COHDSACMPLX.override = 1

        # : Check to ensure that correlation grows linearly - better performance if complex correlation is enabled
        phy.profile_outputs.MODEM_CTRL5_LINCORR.override = 1

        """ Coherent DSA Settings """
        # : Enable coherent demodulator DSA
        phy.profile_outputs.MODEM_COH3_COHDSAEN.override = 1

        # : This threshold determines whether to use fixed or dynamic threshold based on channel power.
        # : > 128, FIXED DSA THRESHOLD ALWAYS
        # : = 0  , DYNAMIC DSA THRESHOLD ALWAYS
        # : 0 < x < 128, hybrid - for low channel power, use fixed threshold. For high channel power, use dynamic.
        # : LRCHPWRSPIKETHD : DUT Power [dBm]
        # : 23 : -52
        # : 25 : -46
        # : 30 : -40
        # : 32 : -38
        # : 35 : -35
        # : 37 : -33
        # : 40 : -31
        # : 60 : -10
        # : 70 : -1
        # : 80 : 3
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSPIKETH.override = 70  # : TODO original 127

        # : For FIXED DSA mode, this is the correlation threshold
        phy.profile_outputs.MODEM_LONGRANGE6_LRSPIKETHD.override = 25  # : Above 25 - sensitivity degradation

        # : For dynamic DSA threshold, this is the baseline threshold. Threshold will increase in addition to this
        # : baseline value dependent on the channel power.
        phy.profile_outputs.MODEM_COH2_FIXEDCDTHFORIIR.override = 70  #

        # : Coefficients for IIR, 0 -> 2^-3, 1 -> 2^-4, 2 -> 2^-5 , 3 -> 2^-6, Higher the value slower is the averaging.
        phy.profile_outputs.MODEM_COH3_DYNIIRCOEFOPTION.override = 3

        # : Tolerance of minimum distance between peaks
        phy.profile_outputs.MODEM_COH3_DSAPEAKINDLEN.override = 4  # : TODO Investigation Original no override (0)

        """ Timing Detection Settings """
        # : Offset between DSA and timing windows
        # : Calculate as OSR*no_of_chips_per_sym*m
        phy.profile_outputs.MODEM_COH3_COHDSAADDWNDSIZE.override = 80  ###-160 ( 864 = 2^10 - 160 ) # : TODO Investigation original 864

        # : Controls additional offset averaging state for timing search and AFC.
        # : Additional windows averages over OFFSUBNUM/OFFSUBDEN samples to avoid DC balance issue
        # : MUST BE SET MANUALLY! NO CALCULATOR SUPPORT AVAILABLE FOR COH PHY
        phy.profile_outputs.MODEM_TIMING_OFFSUBNUM.override = 7
        phy.profile_outputs.MODEM_TIMING_OFFSUBDEN.override = 5

        # : Timing correlation threshold
        # : Note that if COHDYNAMICPRETHRESH = 1, then this is not the timing correlation value used. Dynamic threshold
        # : based on channel power (SYNCTHRESHx and LRCHPWRSHx).
        phy.profile_outputs.MODEM_CTRL6_TIMTHRESHGAIN.override = 1
        phy.profile_outputs.MODEM_TIMING_TIMTHRESH.override = 31

        # : Timing window is controlled via timingbases
        # : Preamble search window is controlled via ADDTIMESEQ
        phy.profile_outputs.MODEM_TIMING_TIMINGBASES.override = 3  # : TODO Potential investigation original 3  - NO EFFECT
        phy.profile_outputs.MODEM_TIMING_ADDTIMSEQ.override = 6  # : TODO : Potential investigation original 6  - NO EFFECT

        # : Preamble Search Timing Criteria
        # : Abort timing based on additional criteria
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT0.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT1.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT2.override = 1

        """ Dynamic Preamble / Sync """
        # : 0 = 1x sync coeff
        # : 1 = 0.94x sync coeff
        # : 2 = 0.88x sync coeff
        # : 3 = 0.74x sync coeff
        # : 4 = 0.5x sync coeff
        # : NOTE CANNOT BE SET IF COHDYNAMICSYNCTHRESH is SET
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESH.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESHSEL.override = 0

        # : Select dynamic sync threshold
        # : NOTE CANNOT BE SET IF COHDYNAMICPRETHRESH is SET
        phy.profile_outputs.MODEM_COH0_COHDYNAMICSYNCTHRESH.override = 0  # TODO: Remove per override killer # Investigation original 0

        # : Enable/Disable and select static sync threshold
        # : IF COHDYNAMICSYNCTHRESH = 0, then this sync threshold is used.
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESHEN.override = 1
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESH.override = 25

        """ Dynamic Channel Power Thresholds """
        # : Set LRCHPWRTHx to 6 dB increment starting from starting_LRCHPWRTH value
        starting_LRCHPWRTH = 16
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH1.override = starting_LRCHPWRTH
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH2.override = starting_LRCHPWRTH + 6 * 1
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH3.override = starting_LRCHPWRTH + 6 * 2  # + 1 # : 29 = -41 dBm and up
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH4.override = starting_LRCHPWRTH + 6 * 3  # + 2
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH5.override = starting_LRCHPWRTH + 6 * 4  # + 2
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH6.override = starting_LRCHPWRTH + 6 * 5  # + 2
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH7.override = starting_LRCHPWRTH + 6 * 6  # + 3 # : 55 = -15 dBm and up
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH8.override = starting_LRCHPWRTH + 6 * 7  # + 4
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH9.override = starting_LRCHPWRTH + 6 * 8  # + 4
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH10.override = starting_LRCHPWRTH + 6 * 9  # + 4
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRTH11.override = starting_LRCHPWRTH + 6 * 10  # + 5

        """ Dynamic BBSS Adjustment Enable """
        phy.profile_outputs.MODEM_COH0_COHDYNAMICBBSSEN.override = 1

        """ Assign BBSS shift values in bits for each channel power threshold """
        # : Set LRCHPWRSHx to 1 bit increment starting from starting_LRCHPWRSH value
        starting_LRCHPWRSH = 3
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH1.override = starting_LRCHPWRSH # no effect on sensitivity
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH2.override = starting_LRCHPWRSH + 1 # no effect on sensitivity
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH3.override = starting_LRCHPWRSH + 2
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH4.override = starting_LRCHPWRSH + 3
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH5.override = starting_LRCHPWRSH + 4
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH6.override = starting_LRCHPWRSH + 5
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH7.override = starting_LRCHPWRSH + 6
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH8.override = starting_LRCHPWRSH + 7
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH9.override = starting_LRCHPWRSH + 8
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH10.override = starting_LRCHPWRSH + 9
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH11.override = starting_LRCHPWRSH + 10
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSH12.override = starting_LRCHPWRSH + 10 # : removes floor issue at high power

        """ ===== Select various slope region based on power level ========================================== """
        """ ===== SEE ALSO BBSS SHIFT BASED ON POWER LEVELS SECTION ========================================= """
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH0.override = starting_LRCHPWRTH  # : TODO Investigation original no override
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = starting_LRCHPWRTH + 6  # : TODO Investigation original 19
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 81

        # : PER's settings
        # phy.profile_outputs.MODEM_COH0_COHCHPWRTH0.override = 0 # : channel power boundary between SYNCTHRESH 0 and 1
        # phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = 21 # : channel power boundary between SYNCTHRESH 1 and 2
        # phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 81 # : channel power boundary between SYNCTHRESH 2 and 3

        """ ===== Select various slope region based on channel power level ================================== """
        # : using this setting reduces premble error rate (PER's setting -5% while this setting -0.3%)
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = starting_LRCHPWRTH - 6  # : TODO Investigation original 37
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = starting_LRCHPWRTH  # : TODO Investigation original 19
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = starting_LRCHPWRTH + 6  # : TODO Investigation original 19
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH3.override = 59  # : TODO Investigation original 59

        # : PER's settings
        # phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = 0
        # phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = 19
        # phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = 19

        # : DELTA 0,1,2,3, available for override
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA0.override = 0  # : TODO Investigation original no override
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA1.override = 0  # 2  # : TODO Investigation original no override
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA2.override = 8  # 4  # : TODO Investigation original 8
        return phy

    #def PHY_IEEE802154_915MHz_OQPSK(self, model):
        #pass

    def PHY_IEEE802154_915MHz_OQPSK_coh(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 915MHz OQPSK Coherent Demod', phy_name=phy_name, tags="-FPGA")

        self.IEEE802154_915MHz_OQPSK(phy, model)
        phy.profile_inputs.deviation.value = 250000
        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.COHERENT
        #phy.profile_outputs.AGC_AGCPERIOD0_MAXHICNTTHD.override = 13
        #phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 14
        #phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 42
        #phy.profile_outputs.AGC_AGCPERIOD0_SETTLETIMERF.override = 14
        # phy.profile_outputs.AGC_CTRL0_DISPNGAINUP.override = 0
        # phy.profile_outputs.AGC_CTRL0_MODE.override = 2
        phy.profile_outputs.AGC_CTRL0_PWRTARGET.override = 20
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 3
        # phy.profile_outputs.AGC_CTRL2_REHICNTTHD.override = 7
        # phy.profile_outputs.AGC_CTRL2_SAFEMODE.override = 0
        # phy.profile_outputs.AGC_CTRL2_SAFEMODETHD.override = 3
        # phy.profile_outputs.AGC_CTRL3_IFPKDDEB.override = 1
        # phy.profile_outputs.AGC_CTRL3_IFPKDDEBPRD.override = 40
        # phy.profile_outputs.AGC_CTRL3_IFPKDDEBRST.override = 10
        # phy.profile_outputs.AGC_CTRL3_IFPKDDEBTHD.override = 1
        # phy.profile_outputs.AGC_CTRL3_RFPKDDEB.override = 0
        # phy.profile_outputs.AGC_CTRL3_RFPKDDEBTHD.override = 1
        # phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        # phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 4
        # phy.profile_outputs.AGC_CTRL4_RFPKDSEL.override = 1
        # phy.profile_outputs.AGC_CTRL4_RFPKDSYNCSEL.override = 1
        # phy.profile_outputs.AGC_CTRL5_PNUPDISTHD.override = 32
        # phy.profile_outputs.AGC_CTRL5_PNUPRELTHD.override = 4
        # phy.profile_outputs.AGC_CTRL6_SEQRFPKDEN.override = 0
        # phy.profile_outputs.AGC_GAINRANGE_BOOSTLNA.override = 1
        # phy.profile_outputs.AGC_GAINRANGE_HIPWRTHD.override = 3
        # phy.profile_outputs.AGC_GAINRANGE_LATCHEDHISTEP.override = 0
        # phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 4
        # phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPDEL.override = 50
        # phy.profile_outputs.AGC_GAINSTEPLIM0_HYST.override = 3
        # phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION0.override = 8
        # phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION1.override = 10
        # phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION2.override = 12
        # phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION3.override = 12
        # phy.profile_outputs.AGC_HICNTREGION1_HICNTREGION4.override = 13
        # phy.profile_outputs.AGC_MANGAIN_MANGAINIFPGA.override = 7
        # phy.profile_outputs.AGC_MANGAIN_MANGAINLNA.override = 1
        # phy.profile_outputs.AGC_MANGAIN_MANGAINPN.override = 1
        # phy.profile_outputs.AGC_STEPDWN_STEPDWN2.override = 3
        # phy.profile_outputs.AGC_STEPDWN_STEPDWN4.override = 3
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 658
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = 19
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 79
        phy.profile_outputs.MODEM_COH0_COHDYNAMICBBSSEN.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESH.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICSYNCTHRESH.override = 0
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = 31
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = 21
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = 21
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH3.override = 46
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA2.override = 5
        phy.profile_outputs.MODEM_COH3_CDSS.override = 4
        phy.profile_outputs.MODEM_COH3_COHDSAADDWNDSIZE.override = -160
        phy.profile_outputs.MODEM_COH3_COHDSAEN.override = 1
        phy.profile_outputs.MODEM_COH3_DYNIIRCOEFOPTION.override = 3
        phy.profile_outputs.MODEM_CTRL1_COMPMODE.override = 0
        phy.profile_outputs.MODEM_CTRL1_PHASEDEMOD.override = 2
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 7
        phy.profile_outputs.FEFILT0_DIGIGAINCTRL_BBSS.override = 5
        phy.profile_outputs.MODEM_CTRL5_DSSSCTD.override = 1
        phy.profile_outputs.MODEM_CTRL5_FOEPREAVG.override = 7
        phy.profile_outputs.MODEM_CTRL5_POEPER.override = 1
        phy.profile_outputs.MODEM_CTRL6_ARW.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT1.override = 1
        phy.profile_outputs.MODEM_CTRL6_RXBRCALCDIS.override = 1
        phy.profile_outputs.MODEM_CTRL6_TDREW.override = 32
        phy.profile_outputs.MODEM_CTRL6_TIMTHRESHGAIN.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG0.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG1.override = 2
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG2.override = 4
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG3.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_AVGWIN.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_CHPWRACCUDEL.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_HYSVAL.override = 3
        phy.profile_outputs.MODEM_LONGRANGE1_LRTIMEOUTTHD.override = 160
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH1.override = 19
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH2.override = 25
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH3.override = 31
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH4.override = 37
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH5.override = 43
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH6.override = 49
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH7.override = 55
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH8.override = 61
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH1.override = 3
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH2.override = 4
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH3.override = 5
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH4.override = 6
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH10.override = 73
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH9.override = 67
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH10.override = 12
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH11.override = 13
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH5.override = 7
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH6.override = 8
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH7.override = 9
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH8.override = 10
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH9.override = 11
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSPIKETH.override = 127
        phy.profile_outputs.MODEM_LONGRANGE6_LRSPIKETHD.override = 50
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINE.override = 7
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINM.override = 1
        phy.profile_outputs.MODEM_PRE_PREERRORS.override = 15
        #phy.profile_outputs.MODEM_REALTIMCFE_MINCOSTTHD.override = 800
        #phy.profile_outputs.MODEM_REALTIMCFE_RTCFEEN.override = 1
        #phy.profile_outputs.MODEM_REALTIMCFE_RTSCHWIN.override = 10
        #phy.profile_outputs.MODEM_REALTIMCFE_VTAFCFRAME.override = 1
        phy.profile_outputs.MODEM_TIMING_ADDTIMSEQ.override = 6
        phy.profile_outputs.MODEM_TIMING_OFFSUBDEN.override = 5
        phy.profile_outputs.MODEM_TIMING_OFFSUBNUM.override = 7
        phy.profile_outputs.MODEM_TIMING_TIMINGBASES.override = 3
        phy.profile_outputs.MODEM_TIMING_TIMTHRESH.override = 25
        #phy.profile_outputs.MODEM_TRECPMDET_PMACQUINGWIN.override = 1
        #phy.profile_outputs.MODEM_TRECPMDET_PMMINCOSTTHD.override = 120
        #phy.profile_outputs.MODEM_TRECPMDET_PMTIMEOUTSEL.override = 2
        phy.profile_outputs.MODEM_CTRL1_RESYNCPER.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_PREFILTLEN.override = 1
        phy.profile_outputs.MODEM_PREFILTCOEFF_PREFILTCOEFF.override = 2736235287
        phy.profile_outputs.MODEM_COH3_COHDSACMPLX.override = 0
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESHEN.override = 1
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESH.override = 50
        phy.profile_outputs.MODEM_COH0_COHCHPWRLOCK.override = 0
        phy.profile_outputs.MODEM_COH0_COHCHPWRRESTART.override = 1


        return phy

    def PHY_IEEE802154_RSGFSK_868MHz_500kbps_mi0p76(self, model):
        pass

    def PHY_IEEE802154_2p4GHz_cohdsa(self, model, phy_name=None):
        pass

    def PHY_IEEE802154_2p4GHz_cohdsa_diversity(self, model, phy_name=None):
        pass

    def PHY_IEEE802154_2p4GHz_diversity(self, model,phy_name=None):
        pass

    def PHY_IEEE802154_2p4GHz(self, model,phy_name=None):
        pass

    def PHY_IEEE802154_2p4GHz_prod(self, model,phy_name=None):
        pass

    def PHY_IEEE802154_SUN_OFDM_OPT1(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN OFDM OPTION 1', phy_name=phy_name)

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
        phy.profile_inputs.target_osr.value = 2
        phy.profile_inputs.if_frequency_hz.value = 0

        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPGEAR.override = 4
        phy.profile_outputs.FEFILT1_DCCOMP_DCGAINGEAR.override = 10
        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPEN.override   = 0
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

        phy.profile_outputs.FRC_FCD0_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override          = 0 
        phy.profile_outputs.FRC_FCD2_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override           = 1
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3

        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override    = -7
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override    = -74
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override    = -113
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override    = -149
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override    = -194
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override    = -223
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override    = -219
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override    = -144
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override    = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override    = 329
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override        = 6
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override    = 12

        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override        = 1
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override    = 2
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override         = 250941
                
        # AGC
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELHI.override = 5 #60mVrms
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 4  # 300mV
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 0  # 100mV
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17 # Per Yang Gao 10/1/20
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2   # 25usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 960       #960 STF cycle = 24 usec
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
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 4
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1
        # AGC Settling Indicator
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200  #fast loop
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 330  #fast loop

        phy.profile_outputs.RAC_TXOFDM_TXENBBREG.override         = 1
        phy.profile_outputs.RAC_TXOFDM_TXENMIX.override           = 1
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override       = 1
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVXDACSEL.override = 7

        return phy
    
    def PHY_IEEE802154_SUN_OFDM_OPT2(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN OFDM OPTION 2', phy_name=phy_name)

        # updated for OFDM
        model.vars.ofdm_option.value_forced = model.vars.ofdm_option.var_enum.OPT2
        phy.profile_inputs.bitrate.value = 1200000
        phy.profile_inputs.channel_spacing_hz.value = 800000
        phy.profile_inputs.bandwidth_hz.value = 688000
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
        phy.profile_inputs.target_osr.value = 2
        phy.profile_inputs.if_frequency_hz.value = 0

        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPEN.override     = 0
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

        phy.profile_outputs.FRC_FCD0_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_FCD2_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override           = 1
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3                

        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override    = -7
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override    = -74
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override    = -113
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override    = -149
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override    = -194
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override    = -223
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override    = -219
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override    = -144
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override    = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override    = 329
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override        = 6
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override    = 12

        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override        = 3
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override    = 4
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override         = 250941

        # AGC
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELHI.override = 5 #60mVrms
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 4  # 300mV
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 0  # 100mV
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17 # Per Yang Gao 10/1/20
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2   # 25usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 960      # STF cycle = 24usec
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
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 4
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1
        # AGC Settling Indicator
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200  #fast loop
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 615  #fast loop

        phy.profile_outputs.RAC_TXOFDM_TXENBBREG.override         = 1
        phy.profile_outputs.RAC_TXOFDM_TXENMIX.override           = 1
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override       = 1
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVXDACSEL.override = 7

        return phy

    def PHY_IEEE802154_SUN_OFDM_OPT3(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN OFDM OPTION 3', phy_name=phy_name)

        # updated for OFDM
        model.vars.ofdm_option.value_forced = model.vars.ofdm_option.var_enum.OPT3
        phy.profile_inputs.bitrate.value = 600000
        phy.profile_inputs.channel_spacing_hz.value = 400000
        phy.profile_inputs.bandwidth_hz.value = 400000
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
        phy.profile_inputs.target_osr.value = 2
        phy.profile_inputs.if_frequency_hz.value = 0

        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPEN.override   = 0
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF0.override = -11
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF1.override = -36
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF2.override = -48
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF3.override = 11
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF4.override = 175
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF5.override = 349
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF6.override = 302
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF7.override = -165
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF8.override = -925
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF9.override = -1375
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF10.override = -690
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF11.override = 1558
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF12.override = 4869
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF13.override = 7872
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF14.override = 9085

        phy.profile_outputs.FRC_FCD0_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_FCD2_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override           = 1
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3                

        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override    = -7
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override    = -74
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override    = -113
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override    = -149
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override    = -194
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override    = -223
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override    = -219
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override    = -144
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override    = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override    = 329
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override        = 6
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override    = 12

        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override        = 7
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override    = 6
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override         = 250941

        # AGC
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELHI.override = 5 #60mVrms
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 4  # 300mV
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 0  # 100mV
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17 # Per Yang Gao 10/1/20
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2  # 25usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 1920     # STF cycle = 48 usec
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
        phy.profile_outputs.AGC_CTRL1_PWRPERIOD.override = 1
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 2
        phy.profile_outputs.AGC_CTRL7_SUBDEN.override = 1
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 4
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1
        # AGC Settling Indicator
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200  #fast loop
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 1140  #fast loop

        phy.profile_outputs.RAC_TXOFDM_TXENBBREG.override         = 1
        phy.profile_outputs.RAC_TXOFDM_TXENMIX.override           = 1
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override       = 1
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVXDACSEL.override = 7

        return phy

    def PHY_IEEE802154_SUN_OFDM_OPT4(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN OFDM OPTION 4', phy_name=phy_name)

        # updated for OFDM
        model.vars.ofdm_option.value_forced = model.vars.ofdm_option.var_enum.OPT4
        phy.profile_inputs.bitrate.value = 300000
        phy.profile_inputs.channel_spacing_hz.value = 200000
        phy.profile_inputs.bandwidth_hz.value = 200000
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
        phy.profile_inputs.target_osr.value = 2
        phy.profile_inputs.if_frequency_hz.value = 0

        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPEN.override   = 0
        # overrides moved to Target_Sim.py for Sim target only
        # phy.profile_outputs.FEFILT1_CF_DEC0.override           = 2
        # phy.profile_outputs.FEFILT1_CF_DEC1.override           = 9
        # # phy.profile_outputs.MODEM_CTRL5_DEC2.override = 0
        # phy.profile_outputs.FEFILT1_SRC_SRCRATIO.override      = 766771
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF0.override = -11
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF1.override = -36
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF2.override = -48
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF3.override = 11
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF4.override = 175
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF5.override = 349
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF6.override = 302
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF7.override = -165
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF8.override = -925
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF9.override = -1375
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF10.override = -690
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF11.override = 1558
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF12.override = 4869
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF13.override = 7872
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF14.override = 9085

        phy.profile_outputs.FRC_FCD0_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_FCD2_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override           = 1
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3

        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override    = -7
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override    = -74
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override    = -113
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override    = -149
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override    = -194
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override    = -223
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override    = -219
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override    = -144
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override    = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override    = 329
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override        = 6
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override    = 12

        #FIXME: we should calculate these
        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override        = 15
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override    = 8
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override         = 250941

        # AGC
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELHI.override = 5 #60mVrms
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 4  # 300mV
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 0  # 100mV
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17 # Per Yang Gao 10/1/20
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 1  # 48usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 1920     # STF cycle = 48usec
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
        phy.profile_outputs.AGC_CTRL1_PWRPERIOD.override = 1
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 2
        phy.profile_outputs.AGC_CTRL7_SUBDEN.override = 1
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 4
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1
        # AGC Settling Indicator
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200  #fast loop
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 2220  #fast loop

        phy.profile_outputs.RAC_TXOFDM_TXENBBREG.override         = 1
        phy.profile_outputs.RAC_TXOFDM_TXENMIX.override           = 1
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override       = 1
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVXDACSEL.override = 7

        return phy

    def PHY_IEEE802154_SUN_OQPSK_1000kcps(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 915MHz SUN OQPSK Coherent Demod 1000kcps', phy_name=phy_name, tags="-FPGA")        
        self.IEEE802154_915MHz_OQPSK(phy, model)
        
        phy.profile_inputs.deviation.value = 250000
        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Custom_OQPSK
        phy.profile_inputs.shaping_filter_param.value = 0.0
        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.tx_xtal_error_ppm.value = 20

        #FIXME: remove overrides that we don't need for soft demod - most of these should go
        phy.profile_outputs.AGC_CTRL0_PWRTARGET.override = 20
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 3
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 658
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = 19
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 79
        phy.profile_outputs.MODEM_COH0_COHDYNAMICBBSSEN.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESH.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICSYNCTHRESH.override = 0
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = 31
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = 21
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = 21
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH3.override = 46
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA2.override = 5
        phy.profile_outputs.MODEM_COH3_CDSS.override = 4
        phy.profile_outputs.MODEM_COH3_COHDSAADDWNDSIZE.override = -160
        phy.profile_outputs.MODEM_COH3_COHDSAEN.override = 1
        phy.profile_outputs.MODEM_COH3_DYNIIRCOEFOPTION.override = 3
        phy.profile_outputs.MODEM_CTRL0_CODING.override = 0
        phy.profile_outputs.MODEM_CTRL0_DETDIS.override = 1
        phy.profile_outputs.MODEM_CTRL0_MODFORMAT.override = 5
        phy.profile_outputs.MODEM_CTRL1_COMPMODE.override = 0
        phy.profile_outputs.MODEM_CTRL1_PHASEDEMOD.override = 2
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 7
        phy.profile_outputs.FEFILT1_DIGIGAINCTRL_BBSS.override = 5
        phy.profile_outputs.MODEM_CTRL5_DSSSCTD.override = 1
        phy.profile_outputs.MODEM_CTRL5_FOEPREAVG.override = 7
        phy.profile_outputs.MODEM_CTRL5_POEPER.override = 1
        phy.profile_outputs.MODEM_CTRL6_ARW.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT1.override = 1
        phy.profile_outputs.MODEM_CTRL6_RXBRCALCDIS.override = 1
        phy.profile_outputs.MODEM_CTRL6_TDREW.override = 32
        phy.profile_outputs.MODEM_CTRL6_TIMTHRESHGAIN.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG0.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG1.override = 2
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG2.override = 4
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG3.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_AVGWIN.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_CHPWRACCUDEL.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_HYSVAL.override = 3
        phy.profile_outputs.MODEM_LONGRANGE1_LRTIMEOUTTHD.override = 160
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH1.override = 19
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH2.override = 25
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH3.override = 31
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH4.override = 37
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH5.override = 43
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH6.override = 49
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH7.override = 55
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH8.override = 61
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH1.override = 3
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH2.override = 4
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH3.override = 5
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH4.override = 6
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH10.override = 73
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH9.override = 67
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH10.override = 12
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH11.override = 13
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH5.override = 7
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH6.override = 8
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH7.override = 9
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH8.override = 10
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH9.override = 11
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSPIKETH.override = 127
        phy.profile_outputs.MODEM_LONGRANGE6_LRSPIKETHD.override = 50
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINE.override = 7
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINM.override = 1
        phy.profile_outputs.MODEM_PRE_PREERRORS.override = 15
        phy.profile_outputs.MODEM_PRE_TXBASES.override = 0
        phy.profile_outputs.MODEM_TIMING_ADDTIMSEQ.override = 6
        phy.profile_outputs.MODEM_TIMING_OFFSUBDEN.override = 5
        phy.profile_outputs.MODEM_TIMING_OFFSUBNUM.override = 7
        phy.profile_outputs.MODEM_TIMING_TIMINGBASES.override = 3
        phy.profile_outputs.MODEM_TIMING_TIMTHRESH.override = 25
        phy.profile_outputs.MODEM_CTRL1_RESYNCPER.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_PREFILTLEN.override = 1
        phy.profile_outputs.MODEM_PREFILTCOEFF_PREFILTCOEFF.override = 2736235287
        phy.profile_outputs.MODEM_COH3_COHDSACMPLX.override = 0
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESHEN.override = 1
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESH.override = 50
        phy.profile_outputs.MODEM_COH0_COHCHPWRLOCK.override = 0
        phy.profile_outputs.MODEM_COH0_COHCHPWRRESTART.override = 1

        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override    = 3

        # For SUN OQPSK only
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override         = 1

        phy.profile_outputs.FRC_FCD0_WORDS.override             = 255
        phy.profile_outputs.FRC_FCD2_WORDS.override             = 255

        return phy

    def PHY_IEEE802154_SUN_OQPSK_1000kcps_RC(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 915MHz SUN OQPSK Coherent Demod 1000kcps RC',
                            phy_name=phy_name, tags="-FPGA")
        self.IEEE802154_915MHz_OQPSK(phy, model)

        phy.profile_inputs.deviation.value = 250000
        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Raised_Cosine
        phy.profile_inputs.shaping_filter_param.value = 0.8
        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.tx_xtal_error_ppm.value = 20

        # FIXME: remove overrides that we don't need for soft demod - most of these should go
        phy.profile_outputs.AGC_CTRL0_PWRTARGET.override = 20
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 3
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 658
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = 19
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 79
        phy.profile_outputs.MODEM_COH0_COHDYNAMICBBSSEN.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESH.override = 1
        phy.profile_outputs.MODEM_COH0_COHDYNAMICSYNCTHRESH.override = 0
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = 31
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = 21
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = 21
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH3.override = 46
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA2.override = 5
        phy.profile_outputs.MODEM_COH3_CDSS.override = 4
        phy.profile_outputs.MODEM_COH3_COHDSAADDWNDSIZE.override = -160
        phy.profile_outputs.MODEM_COH3_COHDSAEN.override = 1
        phy.profile_outputs.MODEM_COH3_DYNIIRCOEFOPTION.override = 3
        phy.profile_outputs.MODEM_CTRL0_CODING.override = 0
        phy.profile_outputs.MODEM_CTRL0_DETDIS.override = 1
        phy.profile_outputs.MODEM_CTRL0_MODFORMAT.override = 5
        phy.profile_outputs.MODEM_CTRL1_COMPMODE.override = 0
        phy.profile_outputs.MODEM_CTRL1_PHASEDEMOD.override = 2
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 7
        phy.profile_outputs.FEFILT1_DIGIGAINCTRL_BBSS.override = 5
        phy.profile_outputs.MODEM_CTRL5_DSSSCTD.override = 1
        phy.profile_outputs.MODEM_CTRL5_FOEPREAVG.override = 7
        phy.profile_outputs.MODEM_CTRL5_POEPER.override = 1
        phy.profile_outputs.MODEM_CTRL6_ARW.override = 1
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT1.override = 1
        phy.profile_outputs.MODEM_CTRL6_RXBRCALCDIS.override = 1
        phy.profile_outputs.MODEM_CTRL6_TDREW.override = 32
        phy.profile_outputs.MODEM_CTRL6_TIMTHRESHGAIN.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG0.override = 1
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG1.override = 2
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG2.override = 4
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG3.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_AVGWIN.override = 4
        phy.profile_outputs.MODEM_LONGRANGE1_CHPWRACCUDEL.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_HYSVAL.override = 3
        phy.profile_outputs.MODEM_LONGRANGE1_LRTIMEOUTTHD.override = 160
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH1.override = 19
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH2.override = 25
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH3.override = 31
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH4.override = 37
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH5.override = 43
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH6.override = 49
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH7.override = 55
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH8.override = 61
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH1.override = 3
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH2.override = 4
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH3.override = 5
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH4.override = 6
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH10.override = 73
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH9.override = 67
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH10.override = 12
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH11.override = 13
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH5.override = 7
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH6.override = 8
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH7.override = 9
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH8.override = 10
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH9.override = 11
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSPIKETH.override = 127
        phy.profile_outputs.MODEM_LONGRANGE6_LRSPIKETHD.override = 50
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINE.override = 7
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINM.override = 1
        phy.profile_outputs.MODEM_PRE_PREERRORS.override = 15
        phy.profile_outputs.MODEM_PRE_TXBASES.override = 0
        phy.profile_outputs.MODEM_TIMING_ADDTIMSEQ.override = 6
        phy.profile_outputs.MODEM_TIMING_OFFSUBDEN.override = 5
        phy.profile_outputs.MODEM_TIMING_OFFSUBNUM.override = 7
        phy.profile_outputs.MODEM_TIMING_TIMINGBASES.override = 3
        phy.profile_outputs.MODEM_TIMING_TIMTHRESH.override = 25
        phy.profile_outputs.MODEM_CTRL1_RESYNCPER.override = 1
        phy.profile_outputs.MODEM_LONGRANGE1_PREFILTLEN.override = 1
        phy.profile_outputs.MODEM_PREFILTCOEFF_PREFILTCOEFF.override = 2736235287
        phy.profile_outputs.MODEM_COH3_COHDSACMPLX.override = 0
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESHEN.override = 1
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESH.override = 50
        phy.profile_outputs.MODEM_COH0_COHCHPWRLOCK.override = 0
        phy.profile_outputs.MODEM_COH0_COHCHPWRRESTART.override = 1

        # For SUN OQPSK only
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override = 3
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override = 1

        phy.profile_outputs.FRC_FCD0_WORDS.override = 255
        phy.profile_outputs.FRC_FCD2_WORDS.override = 255

        return phy

    def PHY_IEEE802154_SUN_OQPSK_100kcps(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 915MHz SUN OQPSK Coherent Demod 100kcps',
                            phy_name=phy_name, tags="-FPGA")

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.bandwidth_hz.value = 125000
        phy.profile_inputs.base_frequency_hz.value = long(906000000)
        phy.profile_inputs.baudrate_tol_ppm.value = 8000
        phy.profile_inputs.bitrate.value = 25000
        phy.profile_inputs.channel_spacing_hz.value = 200000
        phy.profile_inputs.deviation.value = 25000
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = long(0xA47C)
        phy.profile_inputs.dsss_len.value = 16
        phy.profile_inputs.dsss_spreading_factor.value = 4
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.OQPSK
        phy.profile_inputs.preamble_length.value = 32
        phy.profile_inputs.preamble_pattern.value = 0
        phy.profile_inputs.preamble_pattern_len.value = 4
        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Custom_OQPSK
        phy.profile_inputs.shaping_filter_param.value = 0.0
        phy.profile_inputs.symbol_encoding.value = model.vars.symbol_encoding.var_enum.DSSS
        phy.profile_inputs.syncword_0.value = long(0xe5)
        phy.profile_inputs.syncword_1.value = long(0x0)
        phy.profile_inputs.syncword_length.value = 8
        phy.profile_inputs.tx_xtal_error_ppm.value = 20
        phy.profile_inputs.xtal_frequency_hz.value = 39000000
        # phy.profile_inputs.adc_rate_mode.value = model.vars.adc_rate_mode.var_enum.FULLRATE

        # Add 15.4 Packet Configuration
        PHY_COMMON_FRAME_154(phy, model)

        #phy.profile_outputs.FEFILT1_DIGIGAINCTRL_BBSS.override = 5
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override        = 3

        # For SUN OQPSK only
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override = 1
        phy.profile_outputs.FRC_FCD0_WORDS.override = 255
        phy.profile_outputs.FRC_FCD2_WORDS.override = 255
        phy.profile_outputs.MODEM_CTRL0_DETDIS.override = 1
        phy.profile_outputs.MODEM_CTRL0_CODING.override = 0
        phy.profile_outputs.MODEM_CTRL0_MODFORMAT.override = 5
        phy.profile_outputs.MODEM_CTRL1_SYNCDATA.override = 0
        phy.profile_outputs.MODEM_PRE_TXBASES.override = 0

        return phy

    def PHY_IEEE802154_SUN_OQPSK_100kcps_RC(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 915MHz SUN OQPSK Coherent Demod 100kcps RC',
                            phy_name=phy_name, tags="-FPGA")

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.bandwidth_hz.value = 125000
        phy.profile_inputs.base_frequency_hz.value = long(906000000)
        phy.profile_inputs.baudrate_tol_ppm.value = 8000
        phy.profile_inputs.bitrate.value = 25000
        phy.profile_inputs.channel_spacing_hz.value = 200000
        phy.profile_inputs.deviation.value = 25000
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = long(0xA47C)
        phy.profile_inputs.dsss_len.value = 16
        phy.profile_inputs.dsss_spreading_factor.value = 4
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.OQPSK
        phy.profile_inputs.preamble_length.value = 32
        phy.profile_inputs.preamble_pattern.value = 0
        phy.profile_inputs.preamble_pattern_len.value = 4
        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Raised_Cosine
        phy.profile_inputs.shaping_filter_param.value = 0.8
        phy.profile_inputs.symbol_encoding.value = model.vars.symbol_encoding.var_enum.DSSS
        phy.profile_inputs.syncword_0.value = long(0xe5)
        phy.profile_inputs.syncword_1.value = long(0x0)
        phy.profile_inputs.syncword_length.value = 8
        phy.profile_inputs.tx_xtal_error_ppm.value = 20
        phy.profile_inputs.xtal_frequency_hz.value = 39000000
        # phy.profile_inputs.adc_rate_mode.value = model.vars.adc_rate_mode.var_enum.FULLRATE

        # Add 15.4 Packet Configuration
        PHY_COMMON_FRAME_154(phy, model)

        #phy.profile_outputs.FEFILT1_DIGIGAINCTRL_BBSS.override = 5
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3

        # For SUN OQPSK only
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override = 1
        phy.profile_outputs.FRC_FCD0_WORDS.override = 255
        phy.profile_outputs.FRC_FCD2_WORDS.override = 255
        phy.profile_outputs.MODEM_CTRL0_DETDIS.override = 1
        phy.profile_outputs.MODEM_CTRL0_CODING.override = 0
        phy.profile_outputs.MODEM_CTRL0_MODFORMAT.override = 5
        phy.profile_outputs.MODEM_CTRL1_SYNCDATA.override = 0
        phy.profile_outputs.MODEM_PRE_TXBASES.override = 0

        return phy


    def PHY_IEEE802154_SUN_OQPSK_2000kcps(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 2.4GHz SUN OQPSK Coherent Demod 2000kcps', phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.bandwidth_hz.value = 2524800
        phy.profile_inputs.base_frequency_hz.value = long(2450000000)
        phy.profile_inputs.baudrate_tol_ppm.value = 0
        phy.profile_inputs.bitrate.value = 250000
        phy.profile_inputs.channel_spacing_hz.value = 5000000
        phy.profile_inputs.deviation.value = 500000
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = long(0x744AC39B)
        phy.profile_inputs.dsss_len.value = 32
        phy.profile_inputs.dsss_spreading_factor.value = 8
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0
        phy.profile_inputs.if_frequency_hz.value = 1370000
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.OQPSK
        phy.profile_inputs.preamble_length.value = 32
        phy.profile_inputs.preamble_pattern.value = 0
        phy.profile_inputs.preamble_pattern_len.value = 4
        phy.profile_inputs.rx_xtal_error_ppm.value = 20
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Custom_OQPSK
        phy.profile_inputs.shaping_filter_param.value = 0.0
        phy.profile_inputs.symbol_encoding.value = model.vars.symbol_encoding.var_enum.DSSS
        phy.profile_inputs.syncword_0.value = long(0xe5)
        phy.profile_inputs.syncword_1.value = long(0x0)
        phy.profile_inputs.syncword_length.value = 8
        phy.profile_inputs.target_osr.value = 5
        phy.profile_inputs.tx_xtal_error_ppm.value = 20
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

        # Do we need these?
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 5
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 1
        phy.profile_outputs.RAC_SYNTHREGCTRL_MMDLDOVREFTRIM.override = 3
        phy.profile_outputs.RAC_PGACTRL_PGAENLATCHI.override = 1
        phy.profile_outputs.RAC_PGACTRL_PGAENLATCHQ.override = 1
        phy.profile_outputs.SYNTH_LPFCTRL1CAL_OP1BWCAL.override = 11
        phy.profile_outputs.SYNTH_LPFCTRL1CAL_OP1COMPCAL.override = 14
        phy.profile_outputs.SYNTH_LPFCTRL1CAL_RFBVALCAL.override = 0
        phy.profile_outputs.SYNTH_LPFCTRL1CAL_RPVALCAL.override = 0
        phy.profile_outputs.SYNTH_LPFCTRL1CAL_RZVALCAL.override = 9

        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3
        # For SUN OQPSK only
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override = 1
        phy.profile_outputs.FRC_FCD0_WORDS.override = 255
        phy.profile_outputs.FRC_FCD2_WORDS.override = 255
        phy.profile_outputs.MODEM_CTRL0_DETDIS.override = 1
        phy.profile_outputs.MODEM_CTRL0_CODING.override = 0
        phy.profile_outputs.MODEM_CTRL0_MODFORMAT.override = 5
        phy.profile_outputs.MODEM_CTRL1_SYNCDATA.override = 0
        phy.profile_outputs.MODEM_PRE_TXBASES.override = 0

        return phy

    def PHY_Internal_SUN_OFDM_FSK_Concurrent(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN OFDM OPTION concurrent', phy_name=phy_name)

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
        phy.profile_inputs.target_osr.value = 2
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
        phy.profile_outputs.FEFILT1_CHFCTRL_SWCOEFFEN.override    = 0 #Select set 0 since the values are forced

        phy.profile_outputs.FRC_FCD2_CALCCRC.override             = 0
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override          = 0
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override           = 1
        phy.profile_outputs.FRC_RXCTRL_IFINPUTWIDTH.override      = 3

        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override    = -7
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override    = -74
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override    = -113
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override    = -149
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override    = -194
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override    = -223
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override    = -219
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override    = -144
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override    = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override    = 329
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override        = 6
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override    = 12

        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override        = 1
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override    = 2
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override         = 250941
                
        # AGC
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELHI.override = 5 #60mVrms
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 4  # 300mV
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 0  # 100mV
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17 # Per Yang Gao 10/1/20
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2   # 25usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 960       #960 STF cycle = 24 usec
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
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 4
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1
        # AGC Settling Indicator
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200  #fast loop
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 330  #fast loop

        phy.profile_outputs.RAC_TXOFDM_TXENBBREG.override         = 1
        phy.profile_outputs.RAC_TXOFDM_TXENMIX.override           = 1
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override       = 1
        phy.profile_outputs.RFFPLL0_RFFPLLCTRL1_DIVXDACSEL.override = 7

        phy.profile_outputs.FEFILT0_CF_ADCBITORDERI.override = 0                     
        phy.profile_outputs.FEFILT0_CF_ADCBITORDERQ.override = 0                     
        phy.profile_outputs.FEFILT0_CF_DEC0.override = 5                             
        phy.profile_outputs.FEFILT0_CF_DEC1.override = 24                            
        phy.profile_outputs.FEFILT0_CHFCOE00_SET0COEFF0.override = 981               
        phy.profile_outputs.FEFILT0_CHFCOE00_SET0COEFF1.override = 944               
        phy.profile_outputs.FEFILT0_CHFCOE00_SET0COEFF2.override = 70                
        phy.profile_outputs.FEFILT0_CHFCOE01_SET0COEFF3.override = 410               
        phy.profile_outputs.FEFILT0_CHFCOE01_SET0COEFF4.override = 459               
        phy.profile_outputs.FEFILT0_CHFCOE02_SET0COEFF5.override = 1892              
        phy.profile_outputs.FEFILT0_CHFCOE02_SET0COEFF6.override = 3369              
        phy.profile_outputs.FEFILT0_CHFCOE03_SET0COEFF7.override = 3997              
        phy.profile_outputs.FEFILT0_CHFCOE03_SET0COEFF8.override = 1197              
        phy.profile_outputs.FEFILT0_CHFCOE04_SET0COEFF10.override = 14764            
        phy.profile_outputs.FEFILT0_CHFCOE04_SET0COEFF9.override = 860               
        phy.profile_outputs.FEFILT0_CHFCOE05_SET0COEFF11.override = 13811            
        phy.profile_outputs.FEFILT0_CHFCOE05_SET0COEFF12.override = 1931             
        phy.profile_outputs.FEFILT0_CHFCOE06_SET0COEFF13.override = 9832             
        phy.profile_outputs.FEFILT0_CHFCOE06_SET0COEFF14.override = 13847            
        phy.profile_outputs.FEFILT0_CHFCOE10_SET1COEFF0.override = 30                
        phy.profile_outputs.FEFILT0_CHFCOE10_SET1COEFF1.override = 100               
        phy.profile_outputs.FEFILT0_CHFCOE10_SET1COEFF2.override = 200               
        phy.profile_outputs.FEFILT0_CHFCOE11_SET1COEFF3.override = 268               
        phy.profile_outputs.FEFILT0_CHFCOE11_SET1COEFF4.override = 201               
        phy.profile_outputs.FEFILT0_CHFCOE12_SET1COEFF5.override = 1960              
        phy.profile_outputs.FEFILT0_CHFCOE12_SET1COEFF6.override = 3515              
        phy.profile_outputs.FEFILT0_CHFCOE13_SET1COEFF7.override = 3008              
        phy.profile_outputs.FEFILT0_CHFCOE13_SET1COEFF8.override = 2832              
        phy.profile_outputs.FEFILT0_CHFCOE14_SET1COEFF10.override = 660              
        phy.profile_outputs.FEFILT0_CHFCOE14_SET1COEFF9.override = 15640             
        phy.profile_outputs.FEFILT0_CHFCOE15_SET1COEFF11.override = 2792             
        phy.profile_outputs.FEFILT0_CHFCOE15_SET1COEFF12.override = 5128             
        phy.profile_outputs.FEFILT0_CHFCOE16_SET1COEFF13.override = 6951             
        phy.profile_outputs.FEFILT0_CHFCOE16_SET1COEFF14.override = 7639             
        phy.profile_outputs.FEFILT0_CHFCTRL_CHFLATENCY.override = 0                  
        phy.profile_outputs.FEFILT0_CHFCTRL_FWSELCOEFF.override = 0                  
        phy.profile_outputs.FEFILT0_CHFCTRL_FWSWCOEFFEN.override = 0                 
        phy.profile_outputs.FEFILT0_CHFCTRL_SWCOEFFEN.override = 1                   
        phy.profile_outputs.FEFILT0_DCCOMP_DCCOMPEN.override = 1                     
        phy.profile_outputs.FEFILT0_DCCOMP_DCCOMPFREEZE.override = 0                 
        phy.profile_outputs.FEFILT0_DCCOMP_DCCOMPGEAR.override = 6                   
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
        phy.profile_outputs.FEFILT0_DIGMIXCTRL_DIGMIXFREQ.override = 26883           
        phy.profile_outputs.FEFILT0_DIGMIXCTRL_MIXERCONJ.override = 0                
        phy.profile_outputs.FEFILT0_SRC_SRCENABLE.override = 1                       
        phy.profile_outputs.FEFILT0_SRC_SRCRATIO.override = 654311                   
        phy.profile_outputs.FEFILT0_SRC_SRCSRD.override = 0                          
        phy.profile_outputs.FRC_AUTOCG_AUTOCGEN.override = 7                         
        phy.profile_outputs.FRC_BOICTRL_BOIBITPOS.override = 0                       
        phy.profile_outputs.FRC_BOICTRL_BOIEN.override = 0                           
        phy.profile_outputs.FRC_BOICTRL_BOIFIELDLOC.override = 0                     
        phy.profile_outputs.FRC_BOICTRL_BOIMATCHVAL.override = 0                     
        phy.profile_outputs.FRC_CONVGENERATOR_GENERATOR0.override = 15               
        phy.profile_outputs.FRC_CONVGENERATOR_GENERATOR1.override = 13               
        phy.profile_outputs.FRC_CONVGENERATOR_NONSYSTEMATIC.override = 0             
        phy.profile_outputs.FRC_CONVGENERATOR_RECURSIVE.override = 0                 
        phy.profile_outputs.FRC_CTRL_BITORDER.override = 0                           
        phy.profile_outputs.FRC_CTRL_BITSPERWORD.override = 7                        
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override = 1                          
        phy.profile_outputs.FRC_CTRL_RATESELECT.override = 0                         
        phy.profile_outputs.FRC_CTRL_RXFCDMODE.override = 0                          
        phy.profile_outputs.FRC_CTRL_TXFCDMODE.override = 0                          
        phy.profile_outputs.FRC_CTRL_UARTMODE.override = 0                           
        phy.profile_outputs.FRC_CTRL_WAITEOFEN.override = 0                          
        phy.profile_outputs.FRC_DFLCTRL_DFLBITORDER.override = 0                     
        phy.profile_outputs.FRC_DFLCTRL_DFLBITS.override = 0                         
        phy.profile_outputs.FRC_DFLCTRL_DFLBOIOFFSET.override = 0                    
        phy.profile_outputs.FRC_DFLCTRL_DFLINCLUDECRC.override = 0                   
        phy.profile_outputs.FRC_DFLCTRL_DFLMODE.override = 0                         
        phy.profile_outputs.FRC_DFLCTRL_DFLOFFSET.override = 0                       
        phy.profile_outputs.FRC_DFLCTRL_DFLSHIFT.override = 0                        
        phy.profile_outputs.FRC_DFLCTRL_MINLENGTH.override = 0                       
        phy.profile_outputs.FRC_DSLCTRL_DSLBITORDER.override = 0                     
        phy.profile_outputs.FRC_DSLCTRL_DSLBITS.override = 0                         
        phy.profile_outputs.FRC_DSLCTRL_DSLMINLENGTH.override = 0                    
        phy.profile_outputs.FRC_DSLCTRL_DSLMODE.override = 0                         
        phy.profile_outputs.FRC_DSLCTRL_DSLOFFSET.override = 0                       
        phy.profile_outputs.FRC_DSLCTRL_DSLSHIFT.override = 0                        
        phy.profile_outputs.FRC_DSLCTRL_RXSUPRECEPMODE.override = 0                  
        phy.profile_outputs.FRC_DSLCTRL_STORESUP.override = 0                        
        phy.profile_outputs.FRC_DSLCTRL_SUPSHFFACTOR.override = 0                    
        phy.profile_outputs.FRC_FCD0_ADDTRAILTXDATA.override = 0                     
        phy.profile_outputs.FRC_FCD0_BUFFER.override = 0                             
        phy.profile_outputs.FRC_FCD0_CALCCRC.override = 0                            
        phy.profile_outputs.FRC_FCD0_EXCLUDESUBFRAMEWCNT.override = 0                
        phy.profile_outputs.FRC_FCD0_INCLUDECRC.override = 0                         
        phy.profile_outputs.FRC_FCD0_SKIPCRC.override = 0                            
        phy.profile_outputs.FRC_FCD0_SKIPWHITE.override = 0                          
        phy.profile_outputs.FRC_FCD0_WORDS.override = 255                            
        phy.profile_outputs.FRC_FCD1_ADDTRAILTXDATA.override = 0                     
        phy.profile_outputs.FRC_FCD1_BUFFER.override = 0                             
        phy.profile_outputs.FRC_FCD1_CALCCRC.override = 0                            
        phy.profile_outputs.FRC_FCD1_EXCLUDESUBFRAMEWCNT.override = 0                
        phy.profile_outputs.FRC_FCD1_INCLUDECRC.override = 0                         
        phy.profile_outputs.FRC_FCD1_SKIPCRC.override = 0                            
        phy.profile_outputs.FRC_FCD1_SKIPWHITE.override = 0                          
        phy.profile_outputs.FRC_FCD1_WORDS.override = 255                            
        phy.profile_outputs.FRC_FCD2_ADDTRAILTXDATA.override = 0                     
        phy.profile_outputs.FRC_FCD2_BUFFER.override = 1                             
        phy.profile_outputs.FRC_FCD2_CALCCRC.override = 0                            
        phy.profile_outputs.FRC_FCD2_EXCLUDESUBFRAMEWCNT.override = 0                
        phy.profile_outputs.FRC_FCD2_INCLUDECRC.override = 0                         
        phy.profile_outputs.FRC_FCD2_SKIPCRC.override = 0                            
        phy.profile_outputs.FRC_FCD2_SKIPWHITE.override = 0                          
        phy.profile_outputs.FRC_FCD2_WORDS.override = 255                            
        phy.profile_outputs.FRC_FCD3_ADDTRAILTXDATA.override = 0                     
        phy.profile_outputs.FRC_FCD3_BUFFER.override = 0                             
        phy.profile_outputs.FRC_FCD3_CALCCRC.override = 0                            
        phy.profile_outputs.FRC_FCD3_EXCLUDESUBFRAMEWCNT.override = 0                
        phy.profile_outputs.FRC_FCD3_INCLUDECRC.override = 0                         
        phy.profile_outputs.FRC_FCD3_SKIPCRC.override = 0                            
        phy.profile_outputs.FRC_FCD3_SKIPWHITE.override = 0                          
        phy.profile_outputs.FRC_FCD3_WORDS.override = 255                            
        phy.profile_outputs.FRC_FECCTRL_BLOCKWHITEMODE.override = 0                  
        phy.profile_outputs.FRC_FECCTRL_CONVBUSLOCK.override = 0                     
        phy.profile_outputs.FRC_FECCTRL_CONVDECODEMODE.override = 1                  
        phy.profile_outputs.FRC_FECCTRL_CONVHARDERROR.override = 0                   
        phy.profile_outputs.FRC_FECCTRL_CONVINV.override = 3                         
        phy.profile_outputs.FRC_FECCTRL_CONVMODE.override = 0                        
        phy.profile_outputs.FRC_FECCTRL_CONVSUBFRAMETERMINATE.override = 0           
        phy.profile_outputs.FRC_FECCTRL_CONVTRACEBACKDISABLE.override = 0            
        phy.profile_outputs.FRC_FECCTRL_FORCE2FSK.override = 0                       
        phy.profile_outputs.FRC_FECCTRL_INTERLEAVEFIRSTINDEX.override = 0            
        phy.profile_outputs.FRC_FECCTRL_INTERLEAVEMODE.override = 2                  
        phy.profile_outputs.FRC_FECCTRL_INTERLEAVEWIDTH.override = 1                 
        phy.profile_outputs.FRC_FECCTRL_SINGLEBLOCK.override = 0                     
        phy.profile_outputs.FRC_MAXLENGTH_MAXLENGTH.override = 0                     
        phy.profile_outputs.FRC_PUNCTCTRL_PUNCT0.override = 1                        
        phy.profile_outputs.FRC_PUNCTCTRL_PUNCT1.override = 1                        
        phy.profile_outputs.FRC_TRAILTXDATACTRL_TRAILTXDATA.override = 11            
        phy.profile_outputs.FRC_TRAILTXDATACTRL_TRAILTXDATACNT.override = 0          
        phy.profile_outputs.FRC_TRAILTXDATACTRL_TRAILTXDATAFORCE.override = 0        
        phy.profile_outputs.FRC_TRAILTXDATACTRL_TRAILTXREPLEN.override = 0           
        phy.profile_outputs.FRC_TRAILTXDATACTRL_TXSUPPLENOVERIDE.override = 0        
        phy.profile_outputs.FRC_WCNTCMP0_FRAMELENGTH.override = 2                    
        phy.profile_outputs.FRC_WCNTCMP1_LENGTHFIELDLOC.override = 0                 
        phy.profile_outputs.FRC_WCNTCMP3_SUPPLENFIELDLOC.override = 0                
        phy.profile_outputs.FRC_WCNTCMP4_SUPPLENGTH.override = 0                     
        phy.profile_outputs.FRC_WHITECTRL_FEEDBACKSEL.override = 5                   
        phy.profile_outputs.FRC_WHITECTRL_SHROUTPUTSEL.override = 8                  
        phy.profile_outputs.FRC_WHITECTRL_XORFEEDBACK.override = 1                   
        phy.profile_outputs.FRC_WHITEINIT_WHITEINIT.override = 255                   
        phy.profile_outputs.FRC_WHITEPOLY_POLY.override = 256                        
        phy.profile_outputs.MODEM_AFC_AFCAVGPER.override = 0                         
        phy.profile_outputs.MODEM_AFC_AFCDEL.override = 6                            
        phy.profile_outputs.MODEM_AFC_AFCDELDET.override = 0                         
        phy.profile_outputs.MODEM_AFC_AFCDSAFREQOFFEST.override = 0                  
        phy.profile_outputs.MODEM_AFC_AFCENINTCOMP.override = 0                      
        phy.profile_outputs.MODEM_AFC_AFCGEAR.override = 3                           
        phy.profile_outputs.MODEM_AFC_AFCLIMRESET.override = 0                       
        phy.profile_outputs.MODEM_AFC_AFCONESHOT.override = 1                        
        phy.profile_outputs.MODEM_AFC_AFCRXCLR.override = 0                          
        phy.profile_outputs.MODEM_AFC_AFCRXMODE.override = 0                         
        phy.profile_outputs.MODEM_AFC_AFCTXMODE.override = 0                         
        phy.profile_outputs.MODEM_AFCADJLIM_AFCADJLIM.override = 0                   
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEE.override = 1                    
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEM.override = 13                   
        phy.profile_outputs.MODEM_AFCADJTX_AFCSCALEE.override = 14                   
        phy.profile_outputs.MODEM_AFCADJTX_AFCSCALEM.override = 31                   
        phy.profile_outputs.MODEM_ANARAMPCTRL_MUTEDLY.override = 0                   
        phy.profile_outputs.MODEM_ANARAMPCTRL_VMIDCTRL.override = 1                  
        phy.profile_outputs.MODEM_ANTDIVCTRL_ADPRETHRESH.override = 0                
        phy.profile_outputs.MODEM_ANTDIVCTRL_ENADPRETHRESH.override = 0              
        phy.profile_outputs.MODEM_ANTSWCTRL_ANTCOUNT.override = 0                    
        phy.profile_outputs.MODEM_ANTSWCTRL_ANTDFLTSEL.override = 0                  
        phy.profile_outputs.MODEM_ANTSWCTRL_ANTSWENABLE.override = 0                 
        phy.profile_outputs.MODEM_ANTSWCTRL_ANTSWTYPE.override = 0                   
        phy.profile_outputs.MODEM_ANTSWCTRL_CFGANTPATTEN.override = 0                
        phy.profile_outputs.MODEM_ANTSWCTRL_EXTDSTOPPULSECNT.override = 30           
        phy.profile_outputs.MODEM_ANTSWCTRL1_TIMEPERIOD.override = 436906            
        phy.profile_outputs.MODEM_ANTSWEND_ANTSWENDTIM.override = 0                  
        phy.profile_outputs.MODEM_ANTSWSTART_ANTSWSTARTTIM.override = 0              
        phy.profile_outputs.MODEM_AUTOCG_AUTOCGEN.override = 0                       
        phy.profile_outputs.MODEM_BCRCTRL0_BCRALIGN.override = 0                     
        phy.profile_outputs.MODEM_BCRCTRL0_BCRERRRSTEN.override = 0                  
        phy.profile_outputs.MODEM_BCRCTRL0_BCRFBBYP.override = 0                     
        phy.profile_outputs.MODEM_BCRCTRL0_BCRNCOFF.override = 0                     
        phy.profile_outputs.MODEM_BCRCTRL0_CRFAST.override = 0                       
        phy.profile_outputs.MODEM_BCRCTRL0_CRSLOW.override = 0                       
        phy.profile_outputs.MODEM_BCRCTRL0_DISTOGG.override = 0                      
        phy.profile_outputs.MODEM_BCRCTRL1_BCROSR.override = 0                       
        phy.profile_outputs.MODEM_BCRCTRL1_BCRSWSYCW.override = 0                    
        phy.profile_outputs.MODEM_BCRCTRL1_CGAINX2.override = 0                      
        phy.profile_outputs.MODEM_BCRCTRL1_CRGAIN.override = 0                       
        phy.profile_outputs.MODEM_BCRCTRL1_DISMIDPT.override = 0                     
        phy.profile_outputs.MODEM_BCRCTRL1_ESCMIDPT.override = 0                     
        phy.profile_outputs.MODEM_BCRCTRL1_ESTOSREN.override = 0                     
        phy.profile_outputs.MODEM_BCRCTRL1_PHCOMP2FSK.override = 0                   
        phy.profile_outputs.MODEM_BCRCTRL1_RXCOMPLAT.override = 0                    
        phy.profile_outputs.MODEM_BCRCTRL1_RXNCOCOMP.override = 0                    
        phy.profile_outputs.MODEM_BCRCTRL1_SLICEFBBYP.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMOD4FSK0_CODE4GFSK.override = 0               
        phy.profile_outputs.MODEM_BCRDEMOD4FSK0_EN4GFSK.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMOD4FSK0_PHCOMPBYP.override = 0               
        phy.profile_outputs.MODEM_BCRDEMOD4FSK0_THD4GFSK.override = 0                
        phy.profile_outputs.MODEM_BCRDEMOD4FSK1_FDEVCOMPEN.override = 0              
        phy.profile_outputs.MODEM_BCRDEMOD4FSK1_FDEVCOMPRATIO.override = 0           
        phy.profile_outputs.MODEM_BCRDEMOD4FSK1_PHCOMP4FSK0.override = 0             
        phy.profile_outputs.MODEM_BCRDEMOD4FSK1_PHCOMP4FSK1.override = 0             
        phy.profile_outputs.MODEM_BCRDEMOD4FSK1_S2PMAP.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODAFC0_AFCGAINOVRFLW.override = 0            
        phy.profile_outputs.MODEM_BCRDEMODAFC0_EN2TBEST.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODAFC0_ENAFCCLKSW.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODAFC0_LARGEFREQERR.override = 0             
        phy.profile_outputs.MODEM_BCRDEMODAFC1_AFCMAEN.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODAFC1_ENAFC.override = 0                    
        phy.profile_outputs.MODEM_BCRDEMODAFC1_ENAFCFRZ.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODAFC1_ENFBPLL.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODAFC1_ENFZPMEND.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODAFC1_GEARSW.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODAFC1_HALFPHCOMP.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODAFC1_LGWAIT.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODAFC1_NONFRZEN.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODAFC1_ONESHOTAFCEN.override = 0             
        phy.profile_outputs.MODEM_BCRDEMODAFC1_ONESHOTWAITCNT.override = 0           
        phy.profile_outputs.MODEM_BCRDEMODAFC1_PMRSTEN.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODAFC1_SHWAIT.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODAFC1_SKIPPMDET.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODANT_AGCGAINUPB.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODANT_ANT2PMTHD.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODANT_ANWAIT.override = 0                    
        phy.profile_outputs.MODEM_BCRDEMODANT_BCRDEMODANTDIV.override = 0            
        phy.profile_outputs.MODEM_BCRDEMODANT_BYP1P5.override = 0                    
        phy.profile_outputs.MODEM_BCRDEMODANT_SKIP2PH.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODANT_SKIP2PHTHD.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODANT_SWANTTIMER.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR0_ARRDETEN.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR0_ARRDETSRC.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR0_ARRDETTHD.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR0_ARRQPM.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODARR0_ARRRSTEN.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR0_ARRTOLER.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR0_DIFF0RSTEN.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODARR0_EYEQUALEN.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR0_EYEXESTEN.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR0_EYEXESTFAST.override = 0              
        phy.profile_outputs.MODEM_BCRDEMODARR0_PHSPIKETHD.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODARR0_SCHFRZEN.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR0_SCHPRDHI.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR0_SCHPRDLO.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR1_ARREYEQUAL.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODARR1_BCRCFESRC.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR1_ENCFEQUAL.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR1_EYEOPENTHD.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODARR1_KSICOMPEN.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODARR2_CONSYMOL.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODARR2_RAWDCHKALWAYON.override = 0           
        phy.profile_outputs.MODEM_BCRDEMODCTRL_BBPMDETEN.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODCTRL_BCRDEMODEN.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODCTRL_CONSCHKBYP.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODCTRL_DETECTORSEL.override = 0              
        phy.profile_outputs.MODEM_BCRDEMODCTRL_INVRXBIT.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODCTRL_LOCKUPBYP.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODCTRL_MANCHDLY.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODCTRL_MANCHPH.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODCTRL_NONSTDPK.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODCTRL_PH0SIZE.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODCTRL_PHSRCSEL.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODCTRL_PMPATTERN.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODCTRL_PREATH.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODCTRL_PULCORRBYP.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODCTRL_RAWFASTMA.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODCTRL_RAWFLTSEL.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODCTRL_RAWSYN.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODCTRL_SKIPSYN.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODCTRL_SLICERFAST.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODCTRL_SPIKEREMOV.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODKSI_BCRKSI1.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODKSI_BCRKSI2.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODKSI_BCRKSI3.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODOOK_ABPK.override = 0                      
        phy.profile_outputs.MODEM_BCRDEMODOOK_ATTACK.override = 0                    
        phy.profile_outputs.MODEM_BCRDEMODOOK_BCRDEMODOOK.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODOOK_BWPK.override = 0                      
        phy.profile_outputs.MODEM_BCRDEMODOOK_DECAY.override = 0                     
        phy.profile_outputs.MODEM_BCRDEMODOOK_DECAYSWAL.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODOOK_MAFREQDWN.override = 0                 
        phy.profile_outputs.MODEM_BCRDEMODOOK_NOISEFLEST.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODOOK_OOKFRZEN.override = 0                  
        phy.profile_outputs.MODEM_BCRDEMODOOK_PKTRUNK.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODOOK_RAWGAIN.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODOOK_RAWNDEC.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODOOK_SQUELCH.override = 0                   
        phy.profile_outputs.MODEM_BCRDEMODOOK_SQUELCLKEN.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODPMEXP_BCRPHSCALE.override = 0              
        phy.profile_outputs.MODEM_BCRDEMODPMEXP_BCRPMEXP.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODRSSI_MUTERSSICNT.override = 0              
        phy.profile_outputs.MODEM_BCRDEMODRSSI_PRWOFFSET.override = 0                
        phy.profile_outputs.MODEM_BCRDEMODRSSI_RSSIARRTHD.override = 0               
        phy.profile_outputs.MODEM_BCRDEMODRSSI_RSSIMATAP.override = 0                
        phy.profile_outputs.MODEM_CFGANTPATT_CFGANTPATTVAL.override = 0              
        phy.profile_outputs.MODEM_CGCLKSTOP_FORCEOFF.override = 65023                
        phy.profile_outputs.MODEM_COH0_COHCHPWRLOCK.override = 0                     
        phy.profile_outputs.MODEM_COH0_COHCHPWRRESTART.override = 0                  
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH0.override = 0                      
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH1.override = 0                      
        phy.profile_outputs.MODEM_COH0_COHCHPWRTH2.override = 0                      
        phy.profile_outputs.MODEM_COH0_COHDYNAMICBBSSEN.override = 0                 
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESH.override = 0              
        phy.profile_outputs.MODEM_COH0_COHDYNAMICPRETHRESHSEL.override = 0           
        phy.profile_outputs.MODEM_COH0_COHDYNAMICSYNCTHRESH.override = 0             
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH0.override = 0                      
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH1.override = 0                      
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH2.override = 0                      
        phy.profile_outputs.MODEM_COH1_SYNCTHRESH3.override = 0                      
        phy.profile_outputs.MODEM_COH2_DSAPEAKCHPWRTH.override = 0                   
        phy.profile_outputs.MODEM_COH2_FIXEDCDTHFORIIR.override = 0                  
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA0.override = 0                 
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA1.override = 0                 
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA2.override = 0                 
        phy.profile_outputs.MODEM_COH2_SYNCTHRESHDELTA3.override = 0                 
        phy.profile_outputs.MODEM_COH3_CDSS.override = 0                             
        phy.profile_outputs.MODEM_COH3_COHDSAADDWNDSIZE.override = 0                 
        phy.profile_outputs.MODEM_COH3_COHDSACMPLX.override = 0                      
        phy.profile_outputs.MODEM_COH3_COHDSADETDIS.override = 0                     
        phy.profile_outputs.MODEM_COH3_COHDSAEN.override = 0                         
        phy.profile_outputs.MODEM_COH3_DSAPEAKCHKEN.override = 0                     
        phy.profile_outputs.MODEM_COH3_DSAPEAKCHPWREN.override = 0                   
        phy.profile_outputs.MODEM_COH3_DSAPEAKINDLEN.override = 0                    
        phy.profile_outputs.MODEM_COH3_DYNIIRCOEFOPTION.override = 0                 
        phy.profile_outputs.MODEM_COH3_LOGICBASEDCOHDEMODGATE.override = 0           
        phy.profile_outputs.MODEM_COH3_ONEPEAKQUALEN.override = 0                    
        phy.profile_outputs.MODEM_COH3_PEAKCHKTIMOUT.override = 0                    
        phy.profile_outputs.MODEM_CTRL0_CODING.override = 0                          
        phy.profile_outputs.MODEM_CTRL0_DEMODRAWDATASEL.override = 0                 
        phy.profile_outputs.MODEM_CTRL0_DETDIS.override = 0                          
        phy.profile_outputs.MODEM_CTRL0_DIFFENCMODE.override = 0                     
        phy.profile_outputs.MODEM_CTRL0_DSSSDOUBLE.override = 0                      
        phy.profile_outputs.MODEM_CTRL0_DSSSLEN.override = 0                         
        phy.profile_outputs.MODEM_CTRL0_DSSSSHIFTS.override = 0                      
        phy.profile_outputs.MODEM_CTRL0_DUALCORROPTDIS.override = 0                  
        phy.profile_outputs.MODEM_CTRL0_FDM0DIFFDIS.override = 0                     
        phy.profile_outputs.MODEM_CTRL0_FRAMEDETDEL.override = 0                     
        phy.profile_outputs.MODEM_CTRL0_MAPFSK.override = 0                          
        phy.profile_outputs.MODEM_CTRL0_MODFORMAT.override = 0                       
        phy.profile_outputs.MODEM_CTRL0_OOKASYNCPIN.override = 0                     
        phy.profile_outputs.MODEM_CTRL0_SHAPING.override = 2                         
        phy.profile_outputs.MODEM_CTRL1_COMPMODE.override = 3                        
        phy.profile_outputs.MODEM_CTRL1_DUALSYNC.override = 1                        
        phy.profile_outputs.MODEM_CTRL1_FREQOFFESTLIM.override = 0                   
        phy.profile_outputs.MODEM_CTRL1_FREQOFFESTPER.override = 2                   
        phy.profile_outputs.MODEM_CTRL1_PHASEDEMOD.override = 0                      
        phy.profile_outputs.MODEM_CTRL1_RESYNCPER.override = 2                       
        phy.profile_outputs.MODEM_CTRL1_SYNC1INV.override = 0                        
        phy.profile_outputs.MODEM_CTRL1_SYNCBITS.override = 15                       
        phy.profile_outputs.MODEM_CTRL1_SYNCDATA.override = 0                        
        phy.profile_outputs.MODEM_CTRL1_SYNCERRORS.override = 1                      
        phy.profile_outputs.MODEM_CTRL1_TXSYNC.override = 0                          
        phy.profile_outputs.MODEM_CTRL2_BRDIVA.override = 0                          
        phy.profile_outputs.MODEM_CTRL2_BRDIVB.override = 0                          
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 0                      
        phy.profile_outputs.MODEM_CTRL2_DEVMULA.override = 0                         
        phy.profile_outputs.MODEM_CTRL2_DEVMULB.override = 0                         
        phy.profile_outputs.MODEM_CTRL2_DEVWEIGHTDIS.override = 1                    
        phy.profile_outputs.MODEM_CTRL2_DMASEL.override = 0                          
        phy.profile_outputs.MODEM_CTRL2_RATESELMODE.override = 0                     
        phy.profile_outputs.MODEM_CTRL2_RXFRCDIS.override = 0                        
        phy.profile_outputs.MODEM_CTRL2_RXPINMODE.override = 0                       
        phy.profile_outputs.MODEM_CTRL2_SQITHRESH.override = 0                       
        phy.profile_outputs.MODEM_CTRL2_TXPINMODE.override = 0                       
        phy.profile_outputs.MODEM_CTRL3_ANTDIVMODE.override = 0                      
        phy.profile_outputs.MODEM_CTRL3_ANTDIVREPEATDIS.override = 0                 
        phy.profile_outputs.MODEM_CTRL3_PRSDINEN.override = 0                        
        phy.profile_outputs.MODEM_CTRL3_RAMTESTEN.override = 0                       
        phy.profile_outputs.MODEM_CTRL3_TIMINGBASESGAIN.override = 0                 
        phy.profile_outputs.MODEM_CTRL3_TSAMPDEL.override = 0                        
        phy.profile_outputs.MODEM_CTRL3_TSAMPLIM.override = 0                        
        phy.profile_outputs.MODEM_CTRL3_TSAMPMODE.override = 0                       
        phy.profile_outputs.MODEM_CTRL4_ADCSATDENS.override = 0                      
        phy.profile_outputs.MODEM_CTRL4_ADCSATLEVEL.override = 6                     
        phy.profile_outputs.MODEM_CTRL4_CLKUNDIVREQ.override = 0                     
        phy.profile_outputs.MODEM_CTRL4_DEVOFFCOMP.override = 0                      
        phy.profile_outputs.MODEM_CTRL4_ISICOMP.override = 0                         
        phy.profile_outputs.MODEM_CTRL4_OFFSETPHASEMASKING.override = 0              
        phy.profile_outputs.MODEM_CTRL4_OFFSETPHASESCALING.override = 0              
        phy.profile_outputs.MODEM_CTRL4_PHASECLICKFILT.override = 0                  
        phy.profile_outputs.MODEM_CTRL4_PREDISTAVG.override = 0                      
        phy.profile_outputs.MODEM_CTRL4_PREDISTDEB.override = 0                      
        phy.profile_outputs.MODEM_CTRL4_PREDISTGAIN.override = 0                     
        phy.profile_outputs.MODEM_CTRL4_PREDISTRST.override = 0                      
        phy.profile_outputs.MODEM_CTRL4_SOFTDSSSMODE.override = 0                    
        phy.profile_outputs.MODEM_CTRL5_BRCALAVG.override = 0                        
        phy.profile_outputs.MODEM_CTRL5_BRCALEN.override = 0                         
        phy.profile_outputs.MODEM_CTRL5_BRCALMODE.override = 0                       
        phy.profile_outputs.MODEM_CTRL5_DEC2.override = 0                            
        phy.profile_outputs.MODEM_CTRL5_DEMODRAWDATASEL2.override = 0                
        phy.profile_outputs.MODEM_CTRL5_DETDEL.override = 0                          
        phy.profile_outputs.MODEM_CTRL5_DSSSCTD.override = 0                         
        phy.profile_outputs.MODEM_CTRL5_FOEPREAVG.override = 0                       
        phy.profile_outputs.MODEM_CTRL5_INTOSR.override = 1                          
        phy.profile_outputs.MODEM_CTRL5_LINCORR.override = 0                         
        phy.profile_outputs.MODEM_CTRL5_POEPER.override = 0                          
        phy.profile_outputs.MODEM_CTRL5_RESYNCBAUDTRANS.override = 1                 
        phy.profile_outputs.MODEM_CTRL5_RESYNCLIMIT.override = 0                     
        phy.profile_outputs.MODEM_CTRL5_TDEDGE.override = 0                          
        phy.profile_outputs.MODEM_CTRL5_TREDGE.override = 0                          
        phy.profile_outputs.MODEM_CTRL6_ARW.override = 0                             
        phy.profile_outputs.MODEM_CTRL6_CODINGB.override = 0                         
        phy.profile_outputs.MODEM_CTRL6_CPLXCORREN.override = 0                      
        phy.profile_outputs.MODEM_CTRL6_DEMODRESTARTALL.override = 0                 
        phy.profile_outputs.MODEM_CTRL6_DSSS3SYMBOLSYNCEN.override = 0               
        phy.profile_outputs.MODEM_CTRL6_PREBASES.override = 0                        
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT0.override = 0                     
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT1.override = 0                     
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT2.override = 0                     
        phy.profile_outputs.MODEM_CTRL6_PSTIMABORT3.override = 0                     
        phy.profile_outputs.MODEM_CTRL6_RXBRCALCDIS.override = 0                     
        phy.profile_outputs.MODEM_CTRL6_RXRESTARTUPONRSSI.override = 0               
        phy.profile_outputs.MODEM_CTRL6_RXRESTARTUPONSHORTRSSI.override = 0          
        phy.profile_outputs.MODEM_CTRL6_TDREW.override = 0                           
        phy.profile_outputs.MODEM_CTRL6_TIMTHRESHGAIN.override = 0                   
        phy.profile_outputs.MODEM_CTRL6_TXDBPSKINV.override = 0                      
        phy.profile_outputs.MODEM_CTRL6_TXDBPSKRAMPEN.override = 0                   
        phy.profile_outputs.MODEM_DIRECTMODE_CLKWIDTH.override = 1                   
        phy.profile_outputs.MODEM_DIRECTMODE_DMENABLE.override = 0                   
        phy.profile_outputs.MODEM_DIRECTMODE_SYNCASYNC.override = 0                  
        phy.profile_outputs.MODEM_DIRECTMODE_SYNCPREAM.override = 3                  
        phy.profile_outputs.MODEM_DSACTRL_AGCBAUDEN.override = 0                     
        phy.profile_outputs.MODEM_DSACTRL_AMPJUPTHD.override = 0                     
        phy.profile_outputs.MODEM_DSACTRL_ARRTHD.override = 7                        
        phy.profile_outputs.MODEM_DSACTRL_ARRTOLERTHD0.override = 2                  
        phy.profile_outputs.MODEM_DSACTRL_ARRTOLERTHD1.override = 4                  
        phy.profile_outputs.MODEM_DSACTRL_DSAMODE.override = 0                       
        phy.profile_outputs.MODEM_DSACTRL_DSARSTON.override = 1                      
        phy.profile_outputs.MODEM_DSACTRL_FREQAVGSYM.override = 1                    
        phy.profile_outputs.MODEM_DSACTRL_GAINREDUCDLY.override = 0                  
        phy.profile_outputs.MODEM_DSACTRL_LOWDUTY.override = 0                       
        phy.profile_outputs.MODEM_DSACTRL_RESTORE.override = 0                       
        phy.profile_outputs.MODEM_DSACTRL_SCHPRD.override = 0                        
        phy.profile_outputs.MODEM_DSACTRL_TRANRSTDSA.override = 0                    
        phy.profile_outputs.MODEM_DSATHD0_FDEVMAXTHD.override = 120                  
        phy.profile_outputs.MODEM_DSATHD0_FDEVMINTHD.override = 12                   
        phy.profile_outputs.MODEM_DSATHD0_SPIKETHD.override = 100                    
        phy.profile_outputs.MODEM_DSATHD0_UNMODTHD.override = 4                      
        phy.profile_outputs.MODEM_DSATHD1_AMPFLTBYP.override = 1                     
        phy.profile_outputs.MODEM_DSATHD1_DSARSTCNT.override = 2                     
        phy.profile_outputs.MODEM_DSATHD1_FREQLATDLY.override = 1                    
        phy.profile_outputs.MODEM_DSATHD1_FREQSCALE.override = 0                     
        phy.profile_outputs.MODEM_DSATHD1_POWABSTHD.override = 5000                  
        phy.profile_outputs.MODEM_DSATHD1_POWRELTHD.override = 0                     
        phy.profile_outputs.MODEM_DSATHD1_PWRDETDIS.override = 1                     
        phy.profile_outputs.MODEM_DSATHD1_PWRFLTBYP.override = 1                     
        phy.profile_outputs.MODEM_DSATHD1_RSSIJMPTHD.override = 6                    
        phy.profile_outputs.MODEM_DSATHD3_FDEVMAXTHDLO.override = 120                
        phy.profile_outputs.MODEM_DSATHD3_FDEVMINTHDLO.override = 12                 
        phy.profile_outputs.MODEM_DSATHD3_SPIKETHDLO.override = 100                  
        phy.profile_outputs.MODEM_DSATHD3_UNMODTHDLO.override = 4                    
        phy.profile_outputs.MODEM_DSATHD4_ARRTOLERTHD0LO.override = 2                
        phy.profile_outputs.MODEM_DSATHD4_ARRTOLERTHD1LO.override = 4                
        phy.profile_outputs.MODEM_DSATHD4_POWABSTHDLO.override = 5000                
        phy.profile_outputs.MODEM_DSATHD4_SWTHD.override = 0                         
        phy.profile_outputs.MODEM_DSSS0_DSSS0.override = 0                           
        phy.profile_outputs.MODEM_ETSCTRL_CAPTRIG.override = 0                       
        phy.profile_outputs.MODEM_ETSCTRL_ETSLOC.override = 0                        
        phy.profile_outputs.MODEM_ETSTIM_ETSCOUNTEREN.override = 0                   
        phy.profile_outputs.MODEM_ETSTIM_ETSTIMVAL.override = 0                      
        phy.profile_outputs.MODEM_FRMSCHTIME_DSARSTSYCNEN.override = 0               
        phy.profile_outputs.MODEM_FRMSCHTIME_FRMSCHTIME.override = 88                
        phy.profile_outputs.MODEM_FRMSCHTIME_PMRSTSYCNEN.override = 0                
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG0.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG1.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG2.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG3.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG4.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG5.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG6.override = 0                     
        phy.profile_outputs.MODEM_INTAFC_FOEPREAVG7.override = 0                     
        phy.profile_outputs.MODEM_LONGRANGE1_AVGWIN.override = 0                     
        phy.profile_outputs.MODEM_LONGRANGE1_CHPWRACCUDEL.override = 0               
        phy.profile_outputs.MODEM_LONGRANGE1_HYSVAL.override = 0                     
        phy.profile_outputs.MODEM_LONGRANGE1_LOGICBASEDLRDEMODGATE.override = 0      
        phy.profile_outputs.MODEM_LONGRANGE1_LOGICBASEDPUGATE.override = 0           
        phy.profile_outputs.MODEM_LONGRANGE1_LRSPIKETHADD.override = 0               
        phy.profile_outputs.MODEM_LONGRANGE1_LRSS.override = 0                       
        phy.profile_outputs.MODEM_LONGRANGE1_LRTIMEOUTTHD.override = 0               
        phy.profile_outputs.MODEM_LONGRANGE1_PREFILTLEN.override = 1                 
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH1.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH2.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH3.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE2_LRCHPWRTH4.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH5.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH6.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH7.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE3_LRCHPWRTH8.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH1.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH2.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH3.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRSH4.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH10.override = 0                
        phy.profile_outputs.MODEM_LONGRANGE4_LRCHPWRTH9.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH10.override = 0                
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH11.override = 0                
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH5.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH6.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH7.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH8.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE5_LRCHPWRSH9.override = 0                 
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSH12.override = 0                
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRSPIKETH.override = 0             
        phy.profile_outputs.MODEM_LONGRANGE6_LRCHPWRTH11.override = 0                
        phy.profile_outputs.MODEM_LONGRANGE6_LRSPIKETHD.override = 0                 
        phy.profile_outputs.MODEM_LRFRC_CI500.override = 1                           
        phy.profile_outputs.MODEM_LRFRC_FRCACKTIMETHD.override = 0                   
        phy.profile_outputs.MODEM_LRFRC_LRCORRMODE.override = 1                      
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINE.override = 3                    
        phy.profile_outputs.MODEM_MODINDEX_FREQGAINM.override = 5                    
        phy.profile_outputs.MODEM_MODINDEX_MODINDEXE.override = 27                   
        phy.profile_outputs.MODEM_MODINDEX_MODINDEXM.override = 16                   
        phy.profile_outputs.MODEM_OOKSHAPING_OOKSHAPINGEN.override = 0               
        phy.profile_outputs.MODEM_OOKSHAPING_OOKSHAPINGLUTSIZE.override = 0          
        phy.profile_outputs.MODEM_OOKSHAPING_OOKSHAPINGSTEP.override = 0             
        phy.profile_outputs.MODEM_PADEBUG_ENMANPACLKAMPCTRL.override = 0             
        phy.profile_outputs.MODEM_PADEBUG_ENMANPAPOWER.override = 0                  
        phy.profile_outputs.MODEM_PADEBUG_ENMANPASELSLICE.override = 0               
        phy.profile_outputs.MODEM_PADEBUG_MANPACLKAMPCTRL.override = 0               
        phy.profile_outputs.MODEM_PHANTDECSION_CORRANDDIVTHD.override = 100          
        phy.profile_outputs.MODEM_PHANTDECSION_RSSIANDDIVTHD.override = 20           
        phy.profile_outputs.MODEM_PHANTDECSION_RSSICORR0.override = 1                
        phy.profile_outputs.MODEM_PHANTDECSION_RSSICORR1.override = 1                
        phy.profile_outputs.MODEM_PHANTDECSION_RSSICORR2.override = 1                
        phy.profile_outputs.MODEM_PHANTDECSION_RSSICORR3.override = 1                
        phy.profile_outputs.MODEM_PHDMODANTDIV_ANTDECRSTBYP.override = 1             
        phy.profile_outputs.MODEM_PHDMODANTDIV_ANTWAIT.override = 20                 
        phy.profile_outputs.MODEM_PHDMODANTDIV_RECHKCORREN.override = 0              
        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIP2ANT.override = 1                 
        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIPCORRTHD.override = 100            
        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIPRSSITHD.override = 0              
        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIPTHDSEL.override = 1               
        phy.profile_outputs.MODEM_PHDMODCTRL_BCRDETECTOR.override = 0                
        phy.profile_outputs.MODEM_PHDMODCTRL_BCRLEGACYCONC.override = 0              
        phy.profile_outputs.MODEM_PHDMODCTRL_BCRTRECSCONC.override = 0               
        phy.profile_outputs.MODEM_PHDMODCTRL_PMDETEN.override = 0                    
        phy.profile_outputs.MODEM_PHDMODCTRL_PMDETTHD.override = 8                   
        phy.profile_outputs.MODEM_PHDMODCTRL_PMTIMLOSEN.override = 0                 
        phy.profile_outputs.MODEM_PHDMODCTRL_PMTIMLOSTHD.override = 0                
        phy.profile_outputs.MODEM_PHDMODCTRL_REMODDWN.override = 0                   
        phy.profile_outputs.MODEM_PHDMODCTRL_REMODEN.override = 0                    
        phy.profile_outputs.MODEM_PHDMODCTRL_REMODOSR.override = 4                   
        phy.profile_outputs.MODEM_PHDMODCTRL_REMODOUTSEL.override = 1                
        phy.profile_outputs.MODEM_PRE_BASE.override = 2                              
        phy.profile_outputs.MODEM_PRE_BASEBITS.override = 1                          
        phy.profile_outputs.MODEM_PRE_DSSSPRE.override = 0                           
        phy.profile_outputs.MODEM_PRE_PREERRORS.override = 0                         
        phy.profile_outputs.MODEM_PRE_PRESYMB4FSK.override = 0                       
        phy.profile_outputs.MODEM_PRE_PREWNDERRORS.override = 0                      
        phy.profile_outputs.MODEM_PRE_SYNCSYMB4FSK.override = 0                      
        phy.profile_outputs.MODEM_PRE_TXBASES.override = 32                          
        phy.profile_outputs.MODEM_PREFILTCOEFF_PREFILTCOEFF.override = 0             
        phy.profile_outputs.MODEM_REALTIMCFE_EXTENSCHBYP.override = 1                
        phy.profile_outputs.MODEM_REALTIMCFE_MINCOSTTHD.override = 360               
        phy.profile_outputs.MODEM_REALTIMCFE_RTCFEEN.override = 1                    
        phy.profile_outputs.MODEM_REALTIMCFE_RTSCHMODE.override = 1                  
        phy.profile_outputs.MODEM_REALTIMCFE_RTSCHWIN.override = 5                   
        phy.profile_outputs.MODEM_REALTIMCFE_SINEWEN.override = 0                    
        phy.profile_outputs.MODEM_REALTIMCFE_SYNCACQWIN.override = 3                 
        phy.profile_outputs.MODEM_REALTIMCFE_TRACKINGWIN.override = 7                
        phy.profile_outputs.MODEM_REALTIMCFE_VTAFCFRAME.override = 1                 
        phy.profile_outputs.MODEM_RXBR_RXBRDEN.override = 2                          
        phy.profile_outputs.MODEM_RXBR_RXBRINT.override = 2                          
        phy.profile_outputs.MODEM_RXBR_RXBRNUM.override = 1                          
        phy.profile_outputs.MODEM_SHAPING0_COEFF0.override = 0                       
        phy.profile_outputs.MODEM_SHAPING0_COEFF1.override = 0                       
        phy.profile_outputs.MODEM_SHAPING0_COEFF2.override = 0                       
        phy.profile_outputs.MODEM_SHAPING0_COEFF3.override = 10                      
        phy.profile_outputs.MODEM_SHAPING1_COEFF4.override = 74                      
        phy.profile_outputs.MODEM_SHAPING1_COEFF5.override = 84                      
        phy.profile_outputs.MODEM_SHAPING1_COEFF6.override = 84                      
        phy.profile_outputs.MODEM_SHAPING1_COEFF7.override = 84                      
        phy.profile_outputs.MODEM_SHAPING10_COEFF40.override = 0                     
        phy.profile_outputs.MODEM_SHAPING10_COEFF41.override = 0                     
        phy.profile_outputs.MODEM_SHAPING10_COEFF42.override = 0                     
        phy.profile_outputs.MODEM_SHAPING10_COEFF43.override = 0                     
        phy.profile_outputs.MODEM_SHAPING11_COEFF44.override = 0                     
        phy.profile_outputs.MODEM_SHAPING11_COEFF45.override = 0                     
        phy.profile_outputs.MODEM_SHAPING11_COEFF46.override = 0                     
        phy.profile_outputs.MODEM_SHAPING11_COEFF47.override = 0                     
        phy.profile_outputs.MODEM_SHAPING12_COEFF48.override = 0                     
        phy.profile_outputs.MODEM_SHAPING12_COEFF49.override = 0                     
        phy.profile_outputs.MODEM_SHAPING12_COEFF50.override = 0                     
        phy.profile_outputs.MODEM_SHAPING12_COEFF51.override = 0                     
        phy.profile_outputs.MODEM_SHAPING13_COEFF52.override = 0                     
        phy.profile_outputs.MODEM_SHAPING13_COEFF53.override = 0                     
        phy.profile_outputs.MODEM_SHAPING13_COEFF54.override = 0                     
        phy.profile_outputs.MODEM_SHAPING13_COEFF55.override = 0                     
        phy.profile_outputs.MODEM_SHAPING14_COEFF56.override = 0                     
        phy.profile_outputs.MODEM_SHAPING14_COEFF57.override = 0                     
        phy.profile_outputs.MODEM_SHAPING14_COEFF58.override = 0                     
        phy.profile_outputs.MODEM_SHAPING14_COEFF59.override = 0                     
        phy.profile_outputs.MODEM_SHAPING15_COEFF60.override = 0                     
        phy.profile_outputs.MODEM_SHAPING15_COEFF61.override = 0                     
        phy.profile_outputs.MODEM_SHAPING15_COEFF62.override = 0                     
        phy.profile_outputs.MODEM_SHAPING15_COEFF63.override = 0                     
        phy.profile_outputs.MODEM_SHAPING2_COEFF10.override = 0                      
        phy.profile_outputs.MODEM_SHAPING2_COEFF11.override = 0                      
        phy.profile_outputs.MODEM_SHAPING2_COEFF8.override = 0                       
        phy.profile_outputs.MODEM_SHAPING2_COEFF9.override = 0                       
        phy.profile_outputs.MODEM_SHAPING3_COEFF12.override = 0                      
        phy.profile_outputs.MODEM_SHAPING3_COEFF13.override = 0                      
        phy.profile_outputs.MODEM_SHAPING3_COEFF14.override = 0                      
        phy.profile_outputs.MODEM_SHAPING3_COEFF15.override = 0                      
        phy.profile_outputs.MODEM_SHAPING4_COEFF16.override = 0                      
        phy.profile_outputs.MODEM_SHAPING4_COEFF17.override = 0                      
        phy.profile_outputs.MODEM_SHAPING4_COEFF18.override = 0                      
        phy.profile_outputs.MODEM_SHAPING4_COEFF19.override = 0                      
        phy.profile_outputs.MODEM_SHAPING5_COEFF20.override = 0                      
        phy.profile_outputs.MODEM_SHAPING5_COEFF21.override = 0                      
        phy.profile_outputs.MODEM_SHAPING5_COEFF22.override = 0                      
        phy.profile_outputs.MODEM_SHAPING5_COEFF23.override = 0                      
        phy.profile_outputs.MODEM_SHAPING6_COEFF24.override = 0                      
        phy.profile_outputs.MODEM_SHAPING6_COEFF25.override = 0                      
        phy.profile_outputs.MODEM_SHAPING6_COEFF26.override = 0                      
        phy.profile_outputs.MODEM_SHAPING6_COEFF27.override = 0                      
        phy.profile_outputs.MODEM_SHAPING7_COEFF28.override = 0                      
        phy.profile_outputs.MODEM_SHAPING7_COEFF29.override = 0                      
        phy.profile_outputs.MODEM_SHAPING7_COEFF30.override = 0                      
        phy.profile_outputs.MODEM_SHAPING7_COEFF31.override = 0                      
        phy.profile_outputs.MODEM_SHAPING8_COEFF32.override = 0                      
        phy.profile_outputs.MODEM_SHAPING8_COEFF33.override = 0                      
        phy.profile_outputs.MODEM_SHAPING8_COEFF34.override = 0                      
        phy.profile_outputs.MODEM_SHAPING8_COEFF35.override = 0                      
        phy.profile_outputs.MODEM_SHAPING9_COEFF36.override = 0                      
        phy.profile_outputs.MODEM_SHAPING9_COEFF37.override = 0                      
        phy.profile_outputs.MODEM_SHAPING9_COEFF38.override = 0                      
        phy.profile_outputs.MODEM_SHAPING9_COEFF39.override = 0                      
        phy.profile_outputs.MODEM_SQ_SQEN.override = 0                               
        phy.profile_outputs.MODEM_SQ_SQTIMOUT.override = 0                           
        phy.profile_outputs.MODEM_SQEXT_SQSTG2TIMOUT.override = 0                    
        phy.profile_outputs.MODEM_SQEXT_SQSTG3TIMOUT.override = 0                    
        phy.profile_outputs.MODEM_SYNC0_SYNC0.override = 29193                       
        phy.profile_outputs.MODEM_SYNC1_SYNC1.override = 29430                       
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESH.override = 0       
        phy.profile_outputs.MODEM_SYNCPROPERTIES_STATICSYNCTHRESHEN.override = 0     
        phy.profile_outputs.MODEM_TIMING_ADDTIMSEQ.override = 0                      
        phy.profile_outputs.MODEM_TIMING_FASTRESYNC.override = 0                     
        phy.profile_outputs.MODEM_TIMING_FDM0THRESH.override = 0                     
        phy.profile_outputs.MODEM_TIMING_OFFSUBDEN.override = 0                      
        phy.profile_outputs.MODEM_TIMING_OFFSUBNUM.override = 0                      
        phy.profile_outputs.MODEM_TIMING_TIMINGBASES.override = 15                   
        phy.profile_outputs.MODEM_TIMING_TIMSEQINVEN.override = 0                    
        phy.profile_outputs.MODEM_TIMING_TIMSEQSYNC.override = 0                     
        phy.profile_outputs.MODEM_TIMING_TIMTHRESH.override = 40                     
        phy.profile_outputs.MODEM_TIMING_TSAGCDEL.override = 0                       
        phy.profile_outputs.MODEM_TRECPMDET_COSTHYST.override = 0                    
        phy.profile_outputs.MODEM_TRECPMDET_PHSCALE.override = 0                     
        phy.profile_outputs.MODEM_TRECPMDET_PMACQUINGWIN.override = 7                
        phy.profile_outputs.MODEM_TRECPMDET_PMCOSTVALTHD.override = 4                
        phy.profile_outputs.MODEM_TRECPMDET_PMMINCOSTTHD.override = 750              
        phy.profile_outputs.MODEM_TRECPMDET_PMTIMEOUTSEL.override = 3                
        phy.profile_outputs.MODEM_TRECPMDET_PREAMSCH.override = 1                    
        phy.profile_outputs.MODEM_TRECPMPATT_PMEXPECTPATT.override = 1431655765      
        phy.profile_outputs.MODEM_TRECSCFG_PMOFFSET.override = 162                   
        phy.profile_outputs.MODEM_TRECSCFG_TRECSOSR.override = 5       
        phy.profile_outputs.MODEM_TXBR_TXBRDEN.override = 254                        
        phy.profile_outputs.MODEM_TXBR_TXBRNUM.override = 24765                      
        phy.profile_outputs.MODEM_VITERBIDEMOD_CORRCYCLE.override = 0                
        phy.profile_outputs.MODEM_VITERBIDEMOD_CORRSTPSIZE.override = 4              
        phy.profile_outputs.MODEM_VITERBIDEMOD_HARDDECISION.override = 0             
        phy.profile_outputs.MODEM_VITERBIDEMOD_SYNTHAFC.override = 1                 
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64             
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 56             
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 48             
        phy.profile_outputs.MODEM_VITERBIDEMOD_VTDEMODEN.override = 1                
        phy.profile_outputs.MODEM_VTBLETIMING_DISDEMODOF.override = 1                
        phy.profile_outputs.MODEM_VTBLETIMING_FLENOFF.override = 0                   
        phy.profile_outputs.MODEM_VTBLETIMING_TIMINGDELAY.override = 60              
        phy.profile_outputs.MODEM_VTBLETIMING_VTBLETIMINGSEL.override = 1            
        phy.profile_outputs.MODEM_VTCORRCFG0_EXPECTPATT.override = 2421030912        
        phy.profile_outputs.MODEM_VTCORRCFG1_EXPECTHT.override = 4                   
        phy.profile_outputs.MODEM_VTCORRCFG1_EXPSYNCLEN.override = 102               
        phy.profile_outputs.MODEM_VTCORRCFG1_KSI3SWENABLE.override = 1               
        phy.profile_outputs.MODEM_VTCORRCFG1_VITERBIKSI3WB.override = 53             
        phy.profile_outputs.MODEM_VTCORRCFG1_VTFRQLIM.override = 428                 
        phy.profile_outputs.MODEM_VTTRACK_FREQBIAS.override = 0                      
        phy.profile_outputs.MODEM_VTTRACK_FREQTRACKMODE.override = 1                 
        phy.profile_outputs.MODEM_VTTRACK_HIPWRTHD.override = 1                      
        phy.profile_outputs.MODEM_VTTRACK_TIMEACQUTHD.override = 238                 
        phy.profile_outputs.MODEM_VTTRACK_TIMGEAR.override = 0                       
        phy.profile_outputs.MODEM_VTTRACK_TIMTRACKTHD.override = 2                   
    
        return phy
