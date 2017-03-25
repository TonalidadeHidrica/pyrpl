from ..attributes import BoolRegister, FloatRegister, SelectRegister, PhaseRegister, LongRegister
from . import FilterModule
from ..pyrpl_utils import sorted_dict

class Trig(FilterModule):
    _setup_attributes = ["input",
                         "output_direct",
                         "output_signal",
                         "trigger_source",
                         "threshold",
                         "hysteresis",
                         "phase_offset",
                         "auto_rearm",
                         "phase_abs"]#,
                         #"trigger_armed"]
    _gui_attributes = _setup_attributes

    armed = BoolRegister(0x100, 0, doc="Set to True to arm trigger")

    auto_rearm = BoolRegister(0x104, 0, doc="Automatically re-arm trigger?")

    phase_abs = BoolRegister(0x104, 1, doc="Output the absolute value of the phase")

    _trigger_sources = {"off": 0,
                        "pos_edge": 1,
                        "neg_edge": 2,
                        "both_edge": 3}
    trigger_sources = sorted(_trigger_sources.keys())  # help for the user
    trigger_source = SelectRegister(0x108, doc="Trigger source",
                                     options=_trigger_sources)

    _output_signals = sorted_dict(
        TTL = 0,
        asg0_phase = 1)
    output_signals = _output_signals.keys()
    output_signal = SelectRegister(0x10C, options=_output_signals,
                                   doc="Signal to use as module output")
    phase_offset = PhaseRegister(0x110, bits=14,
                                 doc="offset to add to the output phase (before taking absolute value)")

    threshold = FloatRegister(0x118, bits=14, norm=2 ** 13,
                              doc="trigger threshold [volts]")
    hysteresis = FloatRegister(0x11C, bits=14, norm=2 ** 13,
                              doc="hysteresis for ch1 trigger [volts]")


    current_timestamp = LongRegister(0x15C,
                                     bits=64,
                                     doc="An absolute counter "
                                         + "for the time [cycles]")
    trigger_timestamp = LongRegister(0x164,
                                     bits=64,
                                     doc="An absolute counter "
                                         + "for the trigger time [cycles]")

    def _setup(self):
        """ sets up the module (just setting the attributes is OK). """
        self.armed = True

    def output_signal_to_phase(self, v):
        # output signal is a voltage. 0 == 0 deg
        # -1 == 180 deg, 1 == 180 deg - epsilon
        return (v * 180.0) % 360.0