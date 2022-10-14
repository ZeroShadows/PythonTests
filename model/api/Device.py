from dataclasses import dataclass


@dataclass
class Device:
    address: str
    name: str
    pin_1_pwm_d: int
    pin_1_pwm_f: int
    pin_2_pwm_d: int
    pin_2_pwm_f: int
    type: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            address=data["address"],
            pin_1_pwm_d=data["pin_1_pwm_d"],
            pin_1_pwm_f=data["pin_1_pwm_f"],
            pin_2_pwm_d=data["pin_1_pwm_d"],
            pin_2_pwm_f=data["pin_2_pwm_f"],
            type=data["type"]
        )
