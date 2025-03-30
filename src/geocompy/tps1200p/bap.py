from __future__ import annotations

from enum import Enum

from .. import (
    GeoComSubsystem,
    GeoComResponse
)
from ..data import (
    Angle,
    toenum,
    parsestr
)


class TPS1200PBAP(GeoComSubsystem):
    class MEASUREPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.MEASUREPRG:
            return cls(int(value))

        NOMEAS = 0
        NODIST = 1
        DEFDIST = 2
        CLEARDIST = 5
        STOPTRK = 6

    class USERMEASPRG(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.USERMEASPRG:
            return cls(int(value))

        SINGLE_REF_STANDARD = 0
        SINGLE_REF_FAST = 1
        SINGLE_REF_VISIBLE = 2
        SINGLE_RLESS_VISIBLE = 3
        CONT_REF_STANDARD = 4
        CONT_REF_FAST = 5
        CONT_RLESS_VISIBLE = 6
        AVG_REF_STANDARD = 7
        AVG_REF_VISIBLE = 8
        AVG_RLESS_VISIBLE = 9
        CONT_REF_SYNCHRO = 10
        SINGLE_REF_PRECISE = 11

    class PRISMTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.PRISMTYPE:
            return cls(int(value))

        ROUND = 0
        MINI = 1
        TAPE = 2
        THREESIXTY = 3
        USER1 = 4
        USER2 = 5
        USER3 = 6
        MINI360 = 7
        MINIZERO = 8
        USER = 9
        NDSTAPE = 10
        GRZ121 = 11
        MAMPR122 = 12

    class REFLTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.REFLTYPE:
            return cls(int(value))

        UNDEF = 0
        PRISM = 1
        TAPE = 2

    class TARGETTYPE(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.TARGETTYPE:
            return cls(int(value))

        REFL_USE = 0
        REFL_LESS = 1

    class ATRSETTING(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.ATRSETTING:
            return cls(int(value))

        NORMAL = 0
        LOWVISON = 1
        LOWVISAON = 2
        SRANGEON = 3
        SRANGEAON = 4

    class ONOFF(Enum):
        @classmethod
        def parse(cls, value: str) -> TPS1200PBAP.ONOFF:
            return cls(int(value))

        OFF = 0
        ON = 1

    def get_target_type(self) -> GeoComResponse:
        return self._request(
            17022,
            parsers={
                "targettype": self.TARGETTYPE.parse
            }
        )

    def set_target_type(
        self,
        targettype: TARGETTYPE | str
    ) -> GeoComResponse:
        _targettype = toenum(self.TARGETTYPE, targettype)
        return self._request(
            17021,
            [_targettype.value]
        )

    def get_prism_type(self) -> GeoComResponse:
        return self._request(
            17009,
            parsers={
                "prismtype": self.PRISMTYPE.parse
            }
        )

    def set_prism_type(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17008,
            [_prismtype.value]
        )

    def get_prism_type2(self) -> GeoComResponse:
        return self._request(
            17031,
            parsers={
                "prismtype": self.PRISMTYPE.parse,
                "name": parsestr
            }
        )

    def set_prism_type2(
        self,
        prismtype: PRISMTYPE | str,
        name: str
    ) -> GeoComResponse:
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17030,
            [_prismtype.value, name]
        )

    def get_prism_def(
        self,
        prismtype: PRISMTYPE | str
    ) -> GeoComResponse:
        _prismtype = toenum(self.PRISMTYPE, prismtype)
        return self._request(
            17023,
            [_prismtype.value],
            {
                "name": parsestr,
                "const": float,
                "refltype": self.REFLTYPE.parse
            }
        )

    def get_user_prism_def(
        self,
        name: str
    ) -> GeoComResponse:
        return self._request(
            17033,
            [name],
            {
                "const": float,
                "refltype": self.REFLTYPE.parse,
                "creator": parsestr
            }
        )

    def set_user_prism_def(
        self,
        name: str,
        const: float,
        refltype: REFLTYPE | str,
        creator: str
    ) -> GeoComResponse:
        _refltype = toenum(self.REFLTYPE, refltype)
        return self._request(
            17032,
            [name, const, _refltype.value, creator]
        )

    def get_meas_prg(self) -> GeoComResponse:
        return self._request(
            17018,
            parsers={
                "measprg": self.MEASUREPRG.parse
            }
        )

    def set_meas_prog(
        self,
        measprg: MEASUREPRG | str
    ) -> GeoComResponse:
        _measprg = toenum(self.MEASUREPRG, measprg)
        return self._request(
            17019,
            [_measprg.value]
        )

    def meas_distance_angle(
        self,
        distmode: MEASUREPRG | str = MEASUREPRG.DEFDIST
    ) -> GeoComResponse:
        _distmode = toenum(self.MEASUREPRG, distmode)
        return self._request(
            17017,
            [_distmode.value],
            {
                "hz": Angle.parse,
                "v": Angle.parse,
                "dist": float,
                "distmode": self.MEASUREPRG.parse
            }
        )

    def search_target(self) -> GeoComResponse:
        return self._request(17020, [0])

    def get_atr_setting(self) -> GeoComResponse:
        return self._request(
            17034,
            parsers={
                "atrsetting": self.ATRSETTING.parse
            }
        )

    def set_atr_setting(
        self,
        atrsetting: ATRSETTING | str
    ) -> GeoComResponse:
        _atrsetting = toenum(self.ATRSETTING, atrsetting)
        return self._request(
            17035,
            [_atrsetting.value]
        )

    def get_red_atr_fov(self) -> GeoComResponse:
        return self._request(
            17036,
            parsers={
                "redfov": self.ONOFF.parse
            }
        )

    def set_red_atr_fov(
        self,
        redfov: TPS1200PBAP.ONOFF | str
    ) -> GeoComResponse:
        _redfov = toenum(self.ONOFF, redfov)
        return self._request(
            17037,
            [_redfov.value]
        )
