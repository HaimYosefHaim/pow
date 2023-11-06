
# -*- coding: utf-8 -*-

from . static import Base_RM_Field


class RM_Field_LEGOQPSK_LEGOQPSKCFG_MODULATION(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_LEGOQPSK_LEGOQPSKCFG_MODULATION, self).__init__(register,
            'MODULATION', 'LEGOQPSK.LEGOQPSKCFG.MODULATION', 'read-write',
            u"",
            0, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_LEGOQPSK_LEGOQPSKCFG_CHIPRATE(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_LEGOQPSK_LEGOQPSKCFG_CHIPRATE, self).__init__(register,
            'CHIPRATE', 'LEGOQPSK.LEGOQPSKCFG.CHIPRATE', 'read-write',
            u"",
            8, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_LEGOQPSK_LEGOQPSKCFG_BANDFREQMHZ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_LEGOQPSK_LEGOQPSKCFG_BANDFREQMHZ, self).__init__(register,
            'BANDFREQMHZ', 'LEGOQPSK.LEGOQPSKCFG.BANDFREQMHZ', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


