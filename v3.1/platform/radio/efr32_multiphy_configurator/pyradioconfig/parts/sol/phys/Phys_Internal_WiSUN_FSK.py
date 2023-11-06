from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.parts.sol.phys.Phys_Studio_WiSUN_FSK import PHYS_IEEE802154_WiSUN_FSK_Sol
from py_2_and_3_compatibility import *

class PHYS_Internal_WiSUN_FSK_Ocelot(IPhy):

    # Reference \\silabs.com\mcuandwireless\026 Shared Docs\0260_Standards\std_body\IEEE_802_15_4\IEEE Std 802.15.4-2015.pdf
    # Ch 20. SUN FSK PHY

    # Owner: Created by Mark Gorday for use in creating a concurrent co-channel PHY where
    # FEFILT0 is configured for WiSUN using Sol AGC settings, and
    # FEFILT1 is configured for OFDM OPT1
    # JIRA Link:
    def PHY_Internal_WISUN_868MHz_2GFSK_50kbps_1a_EU(self, model, phy_name=None):
        # modify Studio PHY
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_868MHz_2GFSK_50kbps_1a_EU(model,phy_name='PHY_Internal_WISUN_868MHz_2GFSK_50kbps_1a_EU')

        # Match OFDM OPT1 settings
        phy.profile_inputs.xtal_frequency_hz.value = 39000000
        phy.profile_inputs.base_frequency_hz.value = 867800000
        model.vars.if_frequency_hz.value_forced = 200000
        model.vars.adc_rate_mode.value_forced = model.vars.adc_rate_mode.var_enum.FULLRATE

        # AGC from OFDM OPT1 PHY
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 16 # Ocelot PostSi JIRA 1253
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2   # 25usec dispngainup period
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 36
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 240      # STF cycle = 6 usec
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION0.override = 29  # PERIODHI-SETTLETIMEIF-1
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
        phy.profile_outputs.AGC_CTRL0_PWRTARGET.override = 254
        phy.profile_outputs.AGC_CTRL1_PWRPERIOD.override = 3
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 4
        # Override calculated settings to match OFDM OPT1
        phy.profile_outputs.AGC_LNABOOST_LNABWADJ.override = 3
        phy.profile_outputs.AGC_LNABOOST_LNABWADJBOOST.override = 3
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPDEL.override = 44
        
        # Use OFDM OPT1 FRC override here, since this phy is for concurrent mode
        phy.profile_outputs.FRC_CTRL_LPMODEDIS.override         = 1
        phy.profile_outputs.FRC_FECCTRL_BLOCKWHITEMODE.override = 0
 
        phy.profile_outputs.AGC_AGCPERIOD0_MAXHICNTTHD.override = 100                                             
        phy.profile_outputs.AGC_AGCPERIOD0_PERIODHI.override = 44                                                 
        phy.profile_outputs.AGC_AGCPERIOD0_SETTLETIMEIF.override = 6                                              
        phy.profile_outputs.AGC_AGCPERIOD0_SETTLETIMERF.override = 14                                             
        phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 960                                               
        phy.profile_outputs.AGC_CTRL0_ADCATTENCODE.override = 0                                                   
        phy.profile_outputs.AGC_CTRL0_ADCATTENMODE.override = 0                                                   
        phy.profile_outputs.AGC_CTRL0_AGCRST.override = 0                                                         
        phy.profile_outputs.AGC_CTRL0_CFLOOPNFADJ.override = 0                                                    
        phy.profile_outputs.AGC_CTRL0_DISCFLOOPADJ.override = 1                                                   
        phy.profile_outputs.AGC_CTRL0_DISPNDWNCOMP.override = 0                                                   
        phy.profile_outputs.AGC_CTRL0_DISPNGAINUP.override = 0                                                    
        phy.profile_outputs.AGC_CTRL0_DISRESETCHPWR.override = 0                                                  
        phy.profile_outputs.AGC_CTRL0_DSADISCFLOOP.override = 0                                                   
        phy.profile_outputs.AGC_CTRL0_ENRSSIRESET.override = 0                                                    
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1                                                           
        phy.profile_outputs.AGC_CTRL0_PWRTARGET.override = 5                                                      
        phy.profile_outputs.AGC_CTRL0_RSSISHIFT.override = 78                                                     
        phy.profile_outputs.AGC_CTRL1_CCATHRSH.override = 100                                                     
        phy.profile_outputs.AGC_CTRL1_PWRPERIOD.override = 2                                                      
        phy.profile_outputs.AGC_CTRL1_RSSIPERIOD.override = 3                                                     
        phy.profile_outputs.AGC_CTRL2_DISRFPKD.override = 0                                                       
        phy.profile_outputs.AGC_CTRL2_DMASEL.override = 0                                                         
        phy.profile_outputs.AGC_CTRL2_PRSDEBUGEN.override = 0                                                     
        phy.profile_outputs.AGC_CTRL2_REHICNTTHD.override = 7                                                     
        phy.profile_outputs.AGC_CTRL2_RELBYCHPWR.override = 3                                                     
        phy.profile_outputs.AGC_CTRL2_RELOTHD.override = 4                                                        
        phy.profile_outputs.AGC_CTRL2_RELTARGETPWR.override = 236                                                 
        phy.profile_outputs.AGC_CTRL2_SAFEMODE.override = 0                                                       
        phy.profile_outputs.AGC_CTRL2_SAFEMODETHD.override = 3                                                    
        phy.profile_outputs.AGC_CTRL3_IFPKDDEB.override = 1                                                       
        phy.profile_outputs.AGC_CTRL3_IFPKDDEBPRD.override = 40                                                   
        phy.profile_outputs.AGC_CTRL3_IFPKDDEBRST.override = 10                                                   
        phy.profile_outputs.AGC_CTRL3_IFPKDDEBTHD.override = 1                                                    
        phy.profile_outputs.AGC_CTRL3_RFPKDDEB.override = 1                                                       
        phy.profile_outputs.AGC_CTRL3_RFPKDDEBPRD.override = 40                                                   
        phy.profile_outputs.AGC_CTRL3_RFPKDDEBRST.override = 10                                                   
        phy.profile_outputs.AGC_CTRL3_RFPKDDEBTHD.override = 1                                                    
        phy.profile_outputs.AGC_CTRL4_FRZPKDEN.override = 1                                                       
        phy.profile_outputs.AGC_CTRL4_PERIODRFPKD.override = 4000                                                 
        phy.profile_outputs.AGC_CTRL4_RFPKDCNTEN.override = 1                                                     
        phy.profile_outputs.AGC_CTRL4_RFPKDPRDGEAR.override = 2                                                   
        phy.profile_outputs.AGC_CTRL4_RFPKDSEL.override = 1                                                       
        phy.profile_outputs.AGC_CTRL4_RFPKDSYNCSEL.override = 1                                                   
        phy.profile_outputs.AGC_CTRL5_PNUPDISTHD.override = 48                                                    
        phy.profile_outputs.AGC_CTRL5_PNUPRELTHD.override = 4                                                     
        phy.profile_outputs.AGC_CTRL5_SEQPNUPALLOW.override = 0                                                   
        phy.profile_outputs.AGC_CTRL5_SEQRFPKDEN.override = 0                                                     
        phy.profile_outputs.AGC_CTRL6_DUALRFPKDDEC.override = 240296                                              
        phy.profile_outputs.AGC_CTRL6_ENDUALRFPKD.override = 1                                                    
        phy.profile_outputs.AGC_CTRL7_SUBDEN.override = 1                                                         
        phy.profile_outputs.AGC_CTRL7_SUBINT.override = 4                                                         
        phy.profile_outputs.AGC_CTRL7_SUBNUM.override = 0                                                         
        phy.profile_outputs.AGC_CTRL7_SUBPERIOD.override = 1                                                      
        phy.profile_outputs.AGC_DUALRFPKDTHD0_RFPKDLOWTHD0.override = 1                                           
        phy.profile_outputs.AGC_DUALRFPKDTHD0_RFPKDLOWTHD1.override = 10                                          
        phy.profile_outputs.AGC_DUALRFPKDTHD1_RFPKDHITHD0.override = 1                                            
        phy.profile_outputs.AGC_DUALRFPKDTHD1_RFPKDHITHD1.override = 40                                           
        phy.profile_outputs.AGC_GAINRANGE_GAININCSTEP.override = 1                                                
        phy.profile_outputs.AGC_GAINRANGE_HIPWRTHD.override = 3                                                   
        phy.profile_outputs.AGC_GAINRANGE_LATCHEDHISTEP.override = 0                                              
        phy.profile_outputs.AGC_GAINRANGE_LNAINDEXBORDER.override = 7                                             
        phy.profile_outputs.AGC_GAINRANGE_PGAINDEXBORDER.override = 8                                             
        phy.profile_outputs.AGC_GAINRANGE_PNGAINSTEP.override = 3                                                 
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPDEL.override = 45                                              
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 10                                          
        phy.profile_outputs.AGC_GAINSTEPLIM0_HYST.override = 5                                                    
        phy.profile_outputs.AGC_GAINSTEPLIM0_MAXPWRVAR.override = 0                                               
        phy.profile_outputs.AGC_GAINSTEPLIM0_TRANRSTAGC.override = 0                                              
        phy.profile_outputs.AGC_GAINSTEPLIM1_PNINDEXMAX.override = 17                                             
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION0.override = 37                                           
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION1.override = 100                                          
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION2.override = 100                                          
        phy.profile_outputs.AGC_HICNTREGION0_HICNTREGION3.override = 100                                          
        phy.profile_outputs.AGC_HICNTREGION1_HICNTREGION4.override = 100                                          
        phy.profile_outputs.AGC_LBT_CCARSSIPERIOD.override = 0                                                    
        phy.profile_outputs.AGC_LBT_ENCCAGAINREDUCED.override = 0                                                 
        phy.profile_outputs.AGC_LBT_ENCCARSSIMAX.override = 0                                                     
        phy.profile_outputs.AGC_LBT_ENCCARSSIPERIOD.override = 0                                                  
        phy.profile_outputs.AGC_LNABOOST_BOOSTLNA.override = 1                                                    
        phy.profile_outputs.AGC_LNABOOST_LNABWADJ.override = 3                                                    
        phy.profile_outputs.AGC_LNABOOST_LNABWADJBOOST.override = 3                                               
        phy.profile_outputs.AGC_LNAMIXCODE0_LNAMIXSLICE1.override = 61                                            
        phy.profile_outputs.AGC_LNAMIXCODE0_LNAMIXSLICE2.override = 46                                            
        phy.profile_outputs.AGC_LNAMIXCODE0_LNAMIXSLICE3.override = 36                                            
        phy.profile_outputs.AGC_LNAMIXCODE0_LNAMIXSLICE4.override = 28                                            
        phy.profile_outputs.AGC_LNAMIXCODE0_LNAMIXSLICE5.override = 21                                            
        phy.profile_outputs.AGC_LNAMIXCODE1_LNAMIXSLICE10.override = 5                                            
        phy.profile_outputs.AGC_LNAMIXCODE1_LNAMIXSLICE6.override = 17                                            
        phy.profile_outputs.AGC_LNAMIXCODE1_LNAMIXSLICE7.override = 12                                            
        phy.profile_outputs.AGC_LNAMIXCODE1_LNAMIXSLICE8.override = 10                                            
        phy.profile_outputs.AGC_LNAMIXCODE1_LNAMIXSLICE9.override = 6                                             
        phy.profile_outputs.AGC_MANGAIN_MANGAINEN.override = 0                                                    
        phy.profile_outputs.AGC_MANGAIN_MANGAINIFPGA.override = 0                                                 
        phy.profile_outputs.AGC_MANGAIN_MANGAINLNA.override = 0                                                   
        phy.profile_outputs.AGC_MANGAIN_MANGAINPN.override = 0                                                    
        phy.profile_outputs.AGC_MANGAIN_MANIFHILATRST.override = 0                                                
        phy.profile_outputs.AGC_MANGAIN_MANIFLOLATRST.override = 0                                                
        phy.profile_outputs.AGC_MANGAIN_MANRFLATRST.override = 0                                                  
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN1.override = 0                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN2.override = 1                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN3.override = 2                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN4.override = 3                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN5.override = 4                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN6.override = 5                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN7.override = 6                                                    
        phy.profile_outputs.AGC_PGACODE0_PGAGAIN8.override = 7                                                    
        phy.profile_outputs.AGC_PGACODE1_PGAGAIN10.override = 9                                                   
        phy.profile_outputs.AGC_PGACODE1_PGAGAIN11.override = 10                                                  
        phy.profile_outputs.AGC_PGACODE1_PGAGAIN9.override = 8                                                    
        phy.profile_outputs.AGC_PNRFATT0_LNAMIXRFATT1.override = 0                                                
        phy.profile_outputs.AGC_PNRFATT0_LNAMIXRFATT2.override = 63                                               
        phy.profile_outputs.AGC_PNRFATT1_LNAMIXRFATT3.override = 141                                              
        phy.profile_outputs.AGC_PNRFATT1_LNAMIXRFATT4.override = 238                                              
        phy.profile_outputs.AGC_PNRFATT10_LNAMIXRFATT21.override = 14800                                          
        phy.profile_outputs.AGC_PNRFATT10_LNAMIXRFATT22.override = 16383                                          
        phy.profile_outputs.AGC_PNRFATT11_LNAMIXRFATT23.override = 16383                                          
        phy.profile_outputs.AGC_PNRFATT2_LNAMIXRFATT5.override = 502                                              
        phy.profile_outputs.AGC_PNRFATT2_LNAMIXRFATT6.override = 940                                              
        phy.profile_outputs.AGC_PNRFATT3_LNAMIXRFATT7.override = 1269                                             
        phy.profile_outputs.AGC_PNRFATT3_LNAMIXRFATT8.override = 1942                                             
        phy.profile_outputs.AGC_PNRFATT4_LNAMIXRFATT10.override = 3484                                            
        phy.profile_outputs.AGC_PNRFATT4_LNAMIXRFATT9.override = 2526                                             
        phy.profile_outputs.AGC_PNRFATT5_LNAMIXRFATT11.override = 4547                                            
        phy.profile_outputs.AGC_PNRFATT5_LNAMIXRFATT12.override = 6035                                            
        phy.profile_outputs.AGC_PNRFATT6_LNAMIXRFATT13.override = 7678                                            
        phy.profile_outputs.AGC_PNRFATT6_LNAMIXRFATT14.override = 9973                                            
        phy.profile_outputs.AGC_PNRFATT7_LNAMIXRFATT15.override = 12989                                           
        phy.profile_outputs.AGC_PNRFATT7_LNAMIXRFATT16.override = 16383                                           
        phy.profile_outputs.AGC_PNRFATT8_LNAMIXRFATT17.override = 5630                                            
        phy.profile_outputs.AGC_PNRFATT8_LNAMIXRFATT18.override = 7160                                            
        phy.profile_outputs.AGC_PNRFATT9_LNAMIXRFATT19.override = 9180                                            
        phy.profile_outputs.AGC_PNRFATT9_LNAMIXRFATT20.override = 11700                                           
        phy.profile_outputs.AGC_RSSISTEPTHR_DEMODRESTARTPER.override = 0                                          
        phy.profile_outputs.AGC_RSSISTEPTHR_DEMODRESTARTTHR.override = 0                                          
        phy.profile_outputs.AGC_RSSISTEPTHR_NEGSTEPTHR.override = 0                                               
        phy.profile_outputs.AGC_RSSISTEPTHR_POSSTEPTHR.override = 0                                               
        phy.profile_outputs.AGC_RSSISTEPTHR_RSSIFAST.override = 0                                                 
        phy.profile_outputs.AGC_RSSISTEPTHR_STEPPER.override = 0                                                  
        phy.profile_outputs.AGC_SETTLINGINDCTRL_EN.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_NEGTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDCTRL_POSTHD.override = 1
        phy.profile_outputs.AGC_SETTLINGINDPER_DELAYPERIOD.override = 330
        phy.profile_outputs.AGC_SETTLINGINDPER_SETTLEDPERIOD.override = 200
        phy.profile_outputs.AGC_STEPDWN_STEPDWN0.override = 1                                                     
        phy.profile_outputs.AGC_STEPDWN_STEPDWN1.override = 2                                                     
        phy.profile_outputs.AGC_STEPDWN_STEPDWN2.override = 2                                                     
        phy.profile_outputs.AGC_STEPDWN_STEPDWN3.override = 2                                                     
        phy.profile_outputs.AGC_STEPDWN_STEPDWN4.override = 2                                                     
        phy.profile_outputs.AGC_STEPDWN_STEPDWN5.override = 2                                                     
        phy.profile_outputs.FEFILT1_CF_ADCBITORDERI.override = 0                                                  
        phy.profile_outputs.FEFILT1_CF_ADCBITORDERQ.override = 0                                                  
        phy.profile_outputs.FEFILT1_CF_DEC0.override = 5                                                          
        phy.profile_outputs.FEFILT1_CF_DEC1.override = 0                                                          
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF0.override = 21                                             
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF1.override = 80                                             
        phy.profile_outputs.FEFILT1_CHFCOE00_SET0COEFF2.override = 173                                            
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF3.override = 256                                            
        phy.profile_outputs.FEFILT1_CHFCOE01_SET0COEFF4.override = 230                                            
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF5.override = 7                                              
        phy.profile_outputs.FEFILT1_CHFCOE02_SET0COEFF6.override = 3676                                           
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF7.override = 3206                                           
        phy.profile_outputs.FEFILT1_CHFCOE03_SET0COEFF8.override = 3014                                           
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF10.override = 675                                           
        phy.profile_outputs.FEFILT1_CHFCOE04_SET0COEFF9.override = 15755                                          
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF11.override = 2704                                          
        phy.profile_outputs.FEFILT1_CHFCOE05_SET0COEFF12.override = 4961                                          
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF13.override = 6736                                          
        phy.profile_outputs.FEFILT1_CHFCOE06_SET0COEFF14.override = 7409                                          
        phy.profile_outputs.FEFILT1_CHFCOE10_SET1COEFF0.override = 22                                             
        phy.profile_outputs.FEFILT1_CHFCOE10_SET1COEFF1.override = 45                                             
        phy.profile_outputs.FEFILT1_CHFCOE10_SET1COEFF2.override = 48                                             
        phy.profile_outputs.FEFILT1_CHFCOE11_SET1COEFF3.override = 2030                                           
        phy.profile_outputs.FEFILT1_CHFCOE11_SET1COEFF4.override = 1848                                           
        phy.profile_outputs.FEFILT1_CHFCOE12_SET1COEFF5.override = 1553                                           
        phy.profile_outputs.FEFILT1_CHFCOE12_SET1COEFF6.override = 3282                                           
        phy.profile_outputs.FEFILT1_CHFCOE13_SET1COEFF7.override = 3120                                           
        phy.profile_outputs.FEFILT1_CHFCOE13_SET1COEFF8.override = 3346                                           
        phy.profile_outputs.FEFILT1_CHFCOE14_SET1COEFF10.override = 1433                                          
        phy.profile_outputs.FEFILT1_CHFCOE14_SET1COEFF9.override = 44                                             
        phy.profile_outputs.FEFILT1_CHFCOE15_SET1COEFF11.override = 3224                                          
        phy.profile_outputs.FEFILT1_CHFCOE15_SET1COEFF12.override = 5025                                          
        phy.profile_outputs.FEFILT1_CHFCOE16_SET1COEFF13.override = 6365                                          
        phy.profile_outputs.FEFILT1_CHFCOE16_SET1COEFF14.override = 6861                                          
        phy.profile_outputs.FEFILT1_CHFCTRL_CHFLATENCY.override = 0                                               
        phy.profile_outputs.FEFILT1_CHFCTRL_FWSELCOEFF.override = 0                                               
        phy.profile_outputs.FEFILT1_CHFCTRL_FWSWCOEFFEN.override = 0                                              
        phy.profile_outputs.FEFILT1_CHFCTRL_SWCOEFFEN.override = 0                                                
        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPEN.override = 1                                                  
        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPFREEZE.override = 0                                              
        phy.profile_outputs.FEFILT1_DCCOMP_DCCOMPGEAR.override = 4                                                
        phy.profile_outputs.FEFILT1_DCCOMP_DCESTIEN.override = 1                                                  
        phy.profile_outputs.FEFILT1_DCCOMP_DCGAINGEAR.override = 10                                               
        phy.profile_outputs.FEFILT1_DCCOMP_DCGAINGEAREN.override = 1                                              
        phy.profile_outputs.FEFILT1_DCCOMP_DCGAINGEARSMPS.override = 40                                           
        phy.profile_outputs.FEFILT1_DCCOMP_DCLIMIT.override = 0                                                   
        phy.profile_outputs.FEFILT1_DCCOMP_DCRSTEN.override = 0                                                   
        phy.profile_outputs.FEFILT1_DCCOMPFILTINIT_DCCOMPINIT.override = 0                                        
        phy.profile_outputs.FEFILT1_DCCOMPFILTINIT_DCCOMPINITVALI.override = 0                                    
        phy.profile_outputs.FEFILT1_DCCOMPFILTINIT_DCCOMPINITVALQ.override = 0                                    
        phy.profile_outputs.FEFILT1_DIGIGAINCTRL_DEC0GAIN.override = 0                                            
        phy.profile_outputs.FEFILT1_DIGIGAINCTRL_DEC1GAIN.override = 0                                            
        phy.profile_outputs.FEFILT1_DIGIGAINCTRL_DIGIGAIN.override = 0                                            
        phy.profile_outputs.FEFILT1_DIGIGAINCTRL_DIGIGAINEN.override = 0                                          
        phy.profile_outputs.FEFILT1_DIGMIXCTRL_DIGIQSWAPEN.override = 1                                           
        phy.profile_outputs.FEFILT1_DIGMIXCTRL_DIGMIXFBENABLE.override = 1                                        
        phy.profile_outputs.FEFILT1_DIGMIXCTRL_DIGMIXFREQ.override = 0                                            
        phy.profile_outputs.FEFILT1_DIGMIXCTRL_MIXERCONJ.override = 0                                             
        phy.profile_outputs.FEFILT1_SRC_SRCENABLE.override = 1                                                    
        phy.profile_outputs.FEFILT1_SRC_SRCRATIO.override = 782746                                                
        phy.profile_outputs.FEFILT1_SRC_SRCSRD.override = 1                                                       
        phy.profile_outputs.RAC_CLKMULTEN0_CLKMULTENBYPASS40MHZ.override = 0                                      
        phy.profile_outputs.RAC_CLKMULTEN0_CLKMULTENDRVN.override = 0                                             
        phy.profile_outputs.RAC_CLKMULTEN0_CLKMULTENDRVP.override = 0                                             
        phy.profile_outputs.RAC_CLKMULTEN0_CLKMULTENREG3.override = 0                                             
        phy.profile_outputs.RAC_CLKMULTEN0_CLKMULTREG3ADJV.override = 2                                           
        phy.profile_outputs.RAC_CLKMULTEN1_CLKMULTDRVAMPSEL.override = 0                                          
        phy.profile_outputs.RAC_IFADCTRIM0_IFADCCLKSEL.override = 1                                               
        phy.profile_outputs.RAC_IFADCTRIM0_IFADCENHALFMODE.override = 0                                           
        phy.profile_outputs.RAC_IFADCTRIM0_IFADCSIDETONEAMP.override = 1                                          
        phy.profile_outputs.RAC_IFADCTRIM1_IFADCENNEGRES.override = 1                                             
        phy.profile_outputs.RAC_IFADCTRIM1_IFADCENSUBGMODE.override = 0                                           
        phy.profile_outputs.RAC_IFADCTRIM1_IFADCENXOBYPASS.override = 0                                           
        phy.profile_outputs.RAC_IFADCTRIM1_IFADCTZ.override = 1                                                   
        phy.profile_outputs.RAC_LNAMIXTRIM0_LNAMIXLNA0CAPSEL.override = 0                                         
        phy.profile_outputs.RAC_LNAMIXTRIM1_LNAMIXLNA1CAPSEL.override = 0                                         
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELHI.override = 5                                   
        phy.profile_outputs.RAC_LNAMIXTRIM4_LNAMIXRFPKDTHRESHSELLO.override = 2                                   
        phy.profile_outputs.RAC_PATRIM3_TXTRIMDREGBLEED.override = 1                                              
        phy.profile_outputs.RAC_PGACTRL_PGABWMODE.override = 1                                                    
        phy.profile_outputs.RAC_PGACTRL_PGAENLATCHI.override = 1                                                  
        phy.profile_outputs.RAC_PGACTRL_PGAENLATCHQ.override = 1                                                  
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDHISEL.override = 4                                               
        phy.profile_outputs.RAC_PGACTRL_PGATHRPKDLOSEL.override = 0                                               
        phy.profile_outputs.RAC_RX_FEFILTOUTPUTSEL.override = 1
        phy.profile_outputs.RAC_RX_LNAMIXENRFPKDLOTHRESH.override = 1                                             
        phy.profile_outputs.RAC_RX_LNAMIXLDOLOWCUR.override = 0                                                   
        phy.profile_outputs.RAC_RX_SYCHPBIASTRIMBUFRX.override = 0                                                
        phy.profile_outputs.RAC_RX_SYPFDCHPLPENRX.override = 1                                                    
        phy.profile_outputs.RAC_RX_SYPFDFPWENRX.override = 1                                                      
        phy.profile_outputs.RAC_SYDIVCTRL_SYLODIVRADCDIV.override = 0                                             
        phy.profile_outputs.RAC_SYEN_SYCHPLPENRX.override = 1                                                     
        phy.profile_outputs.RAC_SYMMDCTRL_SYMMDMODERX.override = 4                                                
        phy.profile_outputs.RAC_SYNTHENCTRL_MMDPOWERBALANCEDISABLE.override = 0                                   
        phy.profile_outputs.RAC_SYNTHREGCTRL_MMDLDOVREFTRIM.override = 3                                          
        phy.profile_outputs.RAC_SYTRIM0_SYCHPCURRRX.override = 5                                                  
        phy.profile_outputs.RAC_SYTRIM0_SYCHPCURRTX.override = 5                                                  
        phy.profile_outputs.RAC_SYTRIM0_SYCHPLEVPSRCRX.override = 0                                               
        phy.profile_outputs.RAC_SYTRIM0_SYCHPREPLICACURRADJ.override = 1                                          
        phy.profile_outputs.RAC_SYTRIM0_SYCHPSRCENRX.override = 0                                                 
        phy.profile_outputs.RAC_SYTRIM0_SYTRIMCHPREGAMPBIAS.override = 0                                          
        phy.profile_outputs.RAC_SYTRIM0_SYTRIMCHPREGAMPBW.override = 3                                            
        phy.profile_outputs.RAC_SYTRIM1_SYLODIVLDOTRIMCORERX.override = 0                                         
        phy.profile_outputs.RAC_SYTRIM1_SYLODIVLDOTRIMCORETX.override = 0                                         
        phy.profile_outputs.RAC_SYTRIM1_SYLODIVLDOTRIMNDIORX.override = 4                                         
        phy.profile_outputs.RAC_SYTRIM1_SYLODIVLDOTRIMNDIOTX.override = 4                                         
        phy.profile_outputs.RAC_SYTRIM1_SYTRIMMMDREGAMPBIAS.override = 1                                          
        phy.profile_outputs.RAC_SYTRIM1_SYTRIMMMDREGAMPBW.override = 3                                            
        phy.profile_outputs.RAC_TXRAMP_TXMODEPHASEFLIP.override = 0                                               
        phy.profile_outputs.RAC_VCOCTRL_VCODETAMPLITUDERX.override = 4                                            
        phy.profile_outputs.RAC_VCOCTRL_VCODETAMPLITUDETX.override = 4                                            
        phy.profile_outputs.SYNTH_DSMCTRLRX_DEMMODERX.override = 0                                                
        phy.profile_outputs.SYNTH_DSMCTRLRX_DITHERDACRX.override = 0                                              
        phy.profile_outputs.SYNTH_DSMCTRLRX_DITHERDSMINPUTRX.override = 0                                         
        phy.profile_outputs.SYNTH_DSMCTRLRX_DITHERDSMOUTPUTRX.override = 0                                        
        phy.profile_outputs.SYNTH_DSMCTRLRX_DSMMODERX.override = 1                                                
        phy.profile_outputs.SYNTH_DSMCTRLRX_LSBFORCERX.override = 1                                               
        phy.profile_outputs.SYNTH_DSMCTRLRX_MASHORDERRX.override = 1                                              
        phy.profile_outputs.SYNTH_DSMCTRLRX_REQORDERRX.override = 0                                               
        phy.profile_outputs.SYNTH_LPFCTRL1RX_OP1BWRX.override = 0                                                 
        phy.profile_outputs.SYNTH_LPFCTRL1RX_OP1COMPRX.override = 7                                               
        phy.profile_outputs.SYNTH_LPFCTRL1RX_RFBVALRX.override = 0                                                
        phy.profile_outputs.SYNTH_LPFCTRL1RX_RPVALRX.override = 7                                                 
        phy.profile_outputs.SYNTH_LPFCTRL1RX_RZVALRX.override = 14                                                
        phy.profile_outputs.SYNTH_LPFCTRL2RX_CASELRX.override = 1                                                 
        phy.profile_outputs.SYNTH_LPFCTRL2RX_CAVALRX.override = 16                                                
        phy.profile_outputs.SYNTH_LPFCTRL2RX_CFBSELRX.override = 0                                                
        phy.profile_outputs.SYNTH_LPFCTRL2RX_CZSELRX.override = 1                                                 
        phy.profile_outputs.SYNTH_LPFCTRL2RX_CZVALRX.override = 128                                               
        phy.profile_outputs.SYNTH_LPFCTRL2RX_LPFGNDSWENRX.override = 0                                            
        phy.profile_outputs.SYNTH_LPFCTRL2RX_LPFSWENRX.override = 1                                               
        phy.profile_outputs.SYNTH_LPFCTRL2RX_MODESELRX.override = 0                                               
        phy.profile_outputs.SYNTH_LPFCTRL2RX_VCMLVLRX.override = 0                                                
        phy.profile_outputs.TXFRONT_INT1CFG_GAINSHIFT.override = 12
        phy.profile_outputs.TXFRONT_INT1CFG_RATIO.override = 6
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF0.override = 32761
        phy.profile_outputs.TXFRONT_INT1COEF01_COEFF1.override = 32694
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF10.override = 609
        phy.profile_outputs.TXFRONT_INT1COEF1011_COEFF11.override = 983
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF12.override = 1374
        phy.profile_outputs.TXFRONT_INT1COEF1213_COEFF13.override = 1734
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF14.override = 2001
        phy.profile_outputs.TXFRONT_INT1COEF1415_COEFF15.override = 2076
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF2.override = 32655
        phy.profile_outputs.TXFRONT_INT1COEF23_COEFF3.override = 32619
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF4.override = 32574
        phy.profile_outputs.TXFRONT_INT1COEF45_COEFF5.override = 32545
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF6.override = 32549
        phy.profile_outputs.TXFRONT_INT1COEF67_COEFF7.override = 32624
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF8.override = 82
        phy.profile_outputs.TXFRONT_INT1COEF89_COEFF9.override = 329
        phy.profile_outputs.TXFRONT_INT2CFG_GAINSHIFT.override = 2
        phy.profile_outputs.TXFRONT_INT2CFG_RATIO.override = 1
        phy.profile_outputs.TXFRONT_SRCCFG_RATIO.override = 250941      

        phy.profile_outputs.MODEM_TRECSCFG_TRECSOSR.override = 5
        phy.profile_outputs.MODEM_AFC_AFCDEL.override = 6
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEE.override = 1                                                 
        phy.profile_outputs.MODEM_AFCADJRX_AFCSCALEM.override = 13                                                
        phy.profile_outputs.MODEM_AFCADJTX_AFCSCALEE.override = 14                                                
        phy.profile_outputs.MODEM_AFCADJTX_AFCSCALEM.override = 31                                                
        phy.profile_outputs.MODEM_CTRL2_DATAFILTER.override = 0                                                   
        phy.profile_outputs.MODEM_PHDMODCTRL_REMODEN.override = 0                                                 
        phy.profile_outputs.MODEM_PHDMODCTRL_REMODOSR.override = 4   
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64                                          
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 56                                          
        phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 48                                          
        phy.profile_outputs.MODEM_VTCORRCFG1_VITERBIKSI3WB.override = 53           
        phy.profile_outputs.SYNTH_FREQ_FREQ.override = 33546500  

        return phy

    #  WiSUN PHYs with FEC enabled
    def PHY_IEEE802154_WISUN_868MHz_2GFSK_50kbps_1a_EU_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                      readable_name='PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU_FEC',
                      phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_50kbps_1b_JP_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_920MHz_2GFSK_50kbps_1b_JP_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_50kbps_1b_JP(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_200kbps_4b_JP_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_920MHz_2GFSK_200kbps_4b_JP_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_200kbps_4b_JP(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA_FEC(self, model, phy_name=None):
        self._makePhy(model, model.profiles.WiSUN_FSK,
                            readable_name='PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA_FEC',
                            phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA(model)
        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.ENABLED

        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP_ANTDIV(self, model, phy_name=None):
        # phy = self._makePhy(model, model.profiles.WiSUN,
        #                     readable_name='PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP_ANTDIV',
        #                     phy_name=phy_name, tags='-IC')
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP(model)

        phy.profile_inputs.fec_tx_enable.value = model.vars.fec_tx_enable.var_enum.DISABLED

        #phy.profile_inputs.antdivmode.value = model.vars.antdivmode.var_enum.PHDEMODANTDIV
        phy.profile_outputs.MODEM_CTRL3_ANTDIVMODE.override = 5
        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIP2ANT.override = 1
        phy.profile_outputs.MODEM_PHDMODANTDIV_ANTWAIT.override = 24

        phy.profile_outputs.MODEM_REALTIMCFE_TRACKINGWIN.override = 2

        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIPRSSITHD.override = 10

        phy.profile_outputs.MODEM_AFC_AFCONESHOT.override = 0

        phy.profile_outputs.MODEM_REALTIMCFE_RTSCHWIN.override = 3
        phy.profile_outputs.MODEM_TRECPMDET_PMCOSTVALTHD.override = 2

        phy.profile_outputs.MODEM_PHDMODANTDIV_ANTDECRSTBYP.override = 0
        phy.profile_outputs.MODEM_PHDMODANTDIV_RECHKCORREN.override = 1

        return phy

    #  WiSUN PHYs for Soft Demod
    def PHY_IEEE802154_WISUN_868MHz_2GFSK_50kbps_1a_EU_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_868MHz_2GFSK_50kbps_1a_EU(model)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True

        return phy

    def PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True
        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_50kbps_1b_JP_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_50kbps_1b_JP(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True
        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_100kbps_2b_JP(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True
        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_200kbps_4a_NA(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True
        return phy

    def PHY_IEEE802154_WISUN_920MHz_2GFSK_200kbps_4b_JP_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_920MHz_2GFSK_200kbps_4b_JP(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True
        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA_Soft(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_FSK_Sol().PHY_IEEE802154_WISUN_915MHz_2GFSK_300kbps_5_NA(model, phy_name=phy_name)

        phy.profile_inputs.demod_select.value = model.vars.demod_select.var_enum.SOFT_DEMOD
        phy.profile_inputs.afc_run_mode.value = model.vars.afc_run_mode.var_enum.ONE_SHOT
        phy.profile_inputs.trecs_enabled.value = True
        return phy
