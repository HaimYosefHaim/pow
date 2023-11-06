
# -*- coding: utf-8 -*-

from . static import Base_RM_Register
from . LEGOQPSK_field import *


class RM_Register_LEGOQPSK_LEGOQPSKCFG(Base_RM_Register):
    def __init__(self, rmio, label):
        self.__dict__['zz_frozen'] = False
        super(RM_Register_LEGOQPSK_LEGOQPSKCFG, self).__init__(rmio, label,
            0xb500fc00, 0x000,
            'LEGOQPSKCFG', 'LEGOQPSK.LEGOQPSKCFG', 'read-write',
            u"",
            0x00000000, 0x00000000,
            0x00001000, 0x00002000,
            0x00003000)

        self.MODULATION = RM_Field_LEGOQPSK_LEGOQPSKCFG_MODULATION(self)
        self.zz_fdict['MODULATION'] = self.MODULATION
        self.CHIPRATE = RM_Field_LEGOQPSK_LEGOQPSKCFG_CHIPRATE(self)
        self.zz_fdict['CHIPRATE'] = self.CHIPRATE
        self.BANDFREQMHZ = RM_Field_LEGOQPSK_LEGOQPSKCFG_BANDFREQMHZ(self)
        self.zz_fdict['BANDFREQMHZ'] = self.BANDFREQMHZ
        self.__dict__['zz_frozen'] = True


