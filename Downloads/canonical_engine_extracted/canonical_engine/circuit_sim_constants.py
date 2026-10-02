"""Circuit simulation engine — evaluates the full neuro-bio-geochemical state machine.

Parses circuitfile-rewritten.md, builds a gate-level netlist, and simulates
the toroidal discharge-accumulation cycle.

Gate types:
  - AND (multi-input)
  - OR (2-input, observer-wired)
  - XOR / XNOR (2-input, observer-wired)
  - NAND / NOR (2-input, observer-wired)
  - Tristate (2-channel: in0/ctrl0→out0, in1/ctrl1→out1)
  - MUX (in0/in1/ctrl0→out0, sometimes out1)
  - D flip-flop (d/clk/enable/preset/reset → q/q_bar)
  - T flip-flop (clk → toggle)
  - SR latch (set/reset/enable → q/q_bar)
  - 2-output decoder (in_main/in_sub/in_ctrl → out1/out2)
  - 3-output decoder (in_main/in_sub/in_ctrl → out1/out2/out3)
  - 4-input AND (special: actomyosin_ctrl)
"""
from __future__ import annotations

import re
import json
import math
import pathlib
import sys
from typing import Any, Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import absolute_constants as AC

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class GateType(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    XNOR = "XNOR"
    NAND = "NAND"
    NOR = "NOR"
    TRISTATE = "tristate"
    MUX = "MUX"
    DFF = "DFF"
    TFF = "TFF"
    SR_LATCH = "SR_LATCH"
    DECODER2 = "DECODER2"
    DECODER3 = "DECODER3"
    AND4 = "AND4"
    UNKNOWN = "UNKNOWN"


@dataclass
class CircuitNode:
    name: str
    gate_type: GateType
    # inputs: port_name → source endpoint string
    inputs: Dict[str, str] = field(default_factory=dict)
    # controls: ctrl_name → source endpoint string
    controls: Dict[str, str] = field(default_factory=dict)
    # outputs: port_name → list of target endpoint strings
    outputs: Dict[str, List[str]] = field(default_factory=dict)
    # sequential: clk, enable, preset, reset, set, r
    seq: Dict[str, str] = field(default_factory=dict)
    # internal logic expressions (for decoders)
    logic: Dict[str, str] = field(default_factory=dict)
    # physics
    element: str = ""
    particle: str = ""
    color: str = ""
    group: str = ""
    music_dims: List[str] = field(default_factory=list)
    location: str = ""
    # state (for sequential elements)
    state: Dict[str, float] = field(default_factory=dict)
    # output values (current)
    out_values: Dict[str, float] = field(default_factory=dict)


def _parse_endpoint(s: str) -> Tuple[str, str]:
    """"heme.out0" → ("heme", "out0")"""
    s = s.strip().split("#")[0].strip()
    if "." in s:
        node, port = s.rsplit(".", 1)
    else:
        node, port = s, "out"
    return node.strip(), port.strip()


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_circuit(md_path: pathlib.Path) -> Dict[str, CircuitNode]:
    """Parse circuitfile-rewritten.md into CircuitNode dict."""
    text = md_path.read_text(encoding="utf-8")
    nodes: Dict[str, CircuitNode] = {}
    current: Optional[CircuitNode] = None

    # regex patterns
    header_re = re.compile(r"^([A-Za-z0-9_]+)\s*\[([^\]]*)\]")
    input_re = re.compile(r"^\s+(in\d+|in_main|in_sub|in_ctrl|d|clk|enable|preset|reset|set|r|s)\s+<-\s+(.+)")
    ctrl_re = re.compile(r"^\s+(ctrl\d+)\s+<-\s+(.+)")
    output_re = re.compile(r"^\s+(out\d+|out_\w+|q|q_bar|out0|out1|out2|t_ff_out|r_out|set_out|reset_out)\s+->\s+(.+)")
    logic_re = re.compile(r"^\s+(logic_\w+)\s+<-\s+(AND|OR|NOT|XOR)\((.+)\)")
    physics_re = re.compile(r"#\s*PHYSICS:\s*(.+)")
    location_re = re.compile(r"#\s*LOCATION:\s*(.+)")
    music_re = re.compile(r"\*\*음악 차원\*\*:\s*(.+)")

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # header
        m = header_re.match(line)
        if m:
            name = m.group(1)
            desc = m.group(2)

            # determine gate type
            gt = GateType.UNKNOWN
            desc_lower = desc.lower()
            if "d flip-flop" in desc_lower or "d flip flop" in desc_lower:
                gt = GateType.DFF
            elif "t flip-flop" in desc_lower or "t flip flop" in desc_lower:
                gt = GateType.TFF
            elif "sr latch" in desc_lower or "gated sr" in desc_lower:
                gt = GateType.SR_LATCH
            elif "3-output decoder" in desc_lower or "3-output" in desc_lower:
                gt = GateType.DECODER3
            elif "2-output decoder" in desc_lower:
                gt = GateType.DECODER2
            elif "mux" in desc_lower:
                gt = GateType.MUX
            elif "4-input and" in desc_lower or "4-input AND" in desc:
                gt = GateType.AND4
            elif "xor" in desc_lower and "xnor" not in desc_lower:
                gt = GateType.XOR
            elif "xnor" in desc_lower:
                gt = GateType.XNOR
            elif "nand" in desc_lower:
                gt = GateType.NAND
            elif "nor" in desc_lower:
                gt = GateType.NOR
            elif "or:" in desc_lower or desc_lower.startswith("or "):
                gt = GateType.OR
            elif "and:" in desc_lower or desc_lower.startswith("and "):
                gt = GateType.AND
            elif "tristate" in desc_lower:
                gt = GateType.TRISTATE
            elif "and" in desc_lower and "mux" not in desc_lower:
                gt = GateType.AND

            current = CircuitNode(name=name, gate_type=gt)
            nodes[name] = current
            i += 1
            continue

        if current:
            # location
            m = location_re.search(line)
            if m and not current.location:
                current.location = m.group(1).strip()
                i += 1
                continue

            # physics
            m = physics_re.search(line)
            if m and not current.element:
                payload = m.group(1)
                for pair in payload.split("|"):
                    pair = pair.strip()
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        k = k.strip().lower()
                        v = v.strip()
                        if k == "element":
                            current.element = v
                        elif k == "particle":
                            current.particle = v
                        elif k == "color":
                            current.color = v
                        elif k == "group":
                            current.group = v
                i += 1
                continue

            # music dims
            m = music_re.search(line)
            if m and not current.music_dims:
                dims = []
                for token in ("r", "h", "d", "p", "s", "gamma", "g", "nu"):
                    if token in m.group(1):
                        dims.append(token)
                current.music_dims = dims
                i += 1
                continue

            # logic expressions (for decoders)
            m = logic_re.match(line)
            if m:
                current.logic[m.group(1)] = f"{m.group(2)}({m.group(3)})"
                i += 1
                continue

            # inputs
            m = input_re.match(line)
            if m:
                port = m.group(1)
                sources = m.group(2).split("#")[0].strip()
                # handle comma-separated + "selects" comments
                sources = re.sub(r"\(selects.*?\)", "", sources).strip()
                if port in ("d", "clk", "enable", "preset", "reset", "set", "r", "s"):
                    current.seq[port] = sources.split(",")[0].strip()
                else:
                    current.inputs[port] = sources.split(",")[0].strip()
                i += 1
                continue

            # controls
            m = ctrl_re.match(line)
            if m:
                port = m.group(1)
                sources = m.group(2).split("#")[0].strip()
                sources = re.sub(r"\(selects.*?\)", "", sources).strip()
                current.controls[port] = sources.split(",")[0].strip()
                i += 1
                continue

            # outputs
            m = output_re.match(line)
            if m:
                port = m.group(1)
                targets_raw = m.group(2).split("#")[0].strip()
                targets = [t.strip() for t in targets_raw.split(",") if t.strip()]
                current.outputs[port] = targets
                i += 1
                continue

        i += 1

    return nodes


# ---------------------------------------------------------------------------
# Simulator
# ---------------------------------------------------------------------------

class CircuitSimulator:
    """Evaluates the circuit netlist.

    Values are continuous [0, 1] floats, not binary.
    AND = min(inputs), OR = max(inputs), XOR = |a-b|, etc.
    Tristate: ctrl > 0.5 → output = input, else high-impedance (0.0)
    DFF: on clk rising edge, q = d (if enabled)
    """

    def __init__(self, nodes: Dict[str, CircuitNode]):
        self.nodes = nodes
        self.values: Dict[str, Dict[str, float]] = {}  # node → port → value
        self.prev_clk: Dict[str, float] = {}  # for edge detection
        self.iteration = 0
        self.current_hour: float = 0.0

        # initialize all outputs to baseline (NOR_DEFAULT) instead of 0
        BASELINE = AC.NOR_DEFAULT  # 5/32 ≈ 0.15625
        for name, node in nodes.items():
            self.values[name] = {}
            for port in node.outputs:
                self.values[name][port] = BASELINE
            if node.gate_type in (GateType.DFF, GateType.SR_LATCH, GateType.TFF):
                self.values[name]["q"] = BASELINE
                self.values[name]["q_bar"] = 1.0 - BASELINE
                node.state["q"] = BASELINE
                node.state["q_bar"] = 1.0 - BASELINE
            # special: t_ff inside autophagy
            if name == "autophagy":
                self.values[name]["t_ff_out"] = 0.0
                node.state["t_ff_out"] = 0.0
            if name == "autophagy":
                self.values[name]["r_out"] = 0.0
                node.state["r_out"] = 0.0

    def _get_value(self, endpoint: str) -> float:
        """Get value from a source endpoint string like 'heme.out0'."""
        node_name, port = _parse_endpoint(endpoint)
        if node_name not in self.values:
            return 0.0
        return self.values[node_name].get(port, 0.0)

    def _set_output(self, node_name: str, port: str, value: float, hard: bool = False):
        """Set output with relaxation dynamics.
        
        hard=True: direct set (for seeds/initialization)
        hard=False: relax toward target using M_RISK_GAIN tracking rate
        """
        if node_name not in self.values:
            self.values[node_name] = {}
        value = max(0.0, min(1.0, value))
        cur = self.values[node_name].get(port, None)
        if hard or cur is None:
            self.values[node_name][port] = value
        else:
            # Relaxation: new = cur + GAIN * (target - cur)
            GAIN = AC.M_RISK_GAIN  # 0.20
            self.values[node_name][port] = max(0.0, min(1.0, cur + GAIN * (value - cur)))

    def _eval_combinational(self, node: CircuitNode) -> None:
        """Evaluate a combinational gate node."""
        gt = node.gate_type

        if gt == GateType.AND or gt == GateType.AND4:
            vals = [self._get_value(src) for src in node.inputs.values()]
            if not vals:
                return
            result = min(vals) if vals else 0.0
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.OR:
            vals = [self._get_value(src) for src in node.inputs.values()]
            result = max(vals) if vals else 0.0
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.XOR:
            a = self._get_value(node.inputs.get("a", "0"))
            b = self._get_value(node.inputs.get("b", "0"))
            result = abs(a - b)
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.XNOR:
            a = self._get_value(node.inputs.get("a", "0"))
            b = self._get_value(node.inputs.get("b", "0"))
            result = 1.0 - abs(a - b)
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.NAND:
            a = self._get_value(node.inputs.get("a", "0"))
            b = self._get_value(node.inputs.get("b", "0"))
            result = 1.0 - min(a, b)
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.NOR:
            a = self._get_value(node.inputs.get("a", "0"))
            b = self._get_value(node.inputs.get("b", "0"))
            result = 1.0 - max(a, b)
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.TRISTATE:
            # 2-channel tristate: ch0 = (in0, ctrl0, out0), ch1 = (in1, ctrl1, out1)
            for ch in [("in0", "ctrl0", "out0"), ("in1", "ctrl1", "out1")]:
                inp = node.inputs.get(ch[0])
                ctrl = node.controls.get(ch[1])
                if inp and ctrl:
                    cv = self._get_value(ctrl)
                    iv = self._get_value(inp)
                    # In continuous mode: blend between input and baseline
                    # instead of hard 0/1 threshold
                    result = iv * cv + AC.NOR_DEFAULT * (1.0 - cv)
                    self._set_output(node.name, ch[2], result)

        elif gt == GateType.MUX:
            in0 = node.inputs.get("in0")
            in1 = node.inputs.get("in1")
            ctrl0 = node.controls.get("ctrl0")
            if ctrl0:
                cv = self._get_value(ctrl0)
                v0 = self._get_value(in0) if in0 else AC.NOR_DEFAULT
                v1 = self._get_value(in1) if in1 else AC.NOR_DEFAULT
                # Continuous blend instead of hard threshold
                result = v0 * (1.0 - cv) + v1 * cv
            else:
                result = self._get_value(in0) if in0 else AC.NOR_DEFAULT
            for port in node.outputs:
                self._set_output(node.name, port, result)

        elif gt == GateType.DECODER2:
            in_main = self._get_value(node.inputs.get("in_main", "0"))
            in_sub = self._get_value(node.inputs.get("in_sub", "0"))
            in_ctrl = self._get_value(node.inputs.get("in_ctrl", "0"))
            logic_hind = min(in_ctrl, in_main)
            logic_co2 = min(in_ctrl, 1.0 - in_main, in_sub)
            # map logic names to outputs
            for port in node.outputs:
                if "hind" in port or "out_1" in port or port == "out_hind_insula":
                    self._set_output(node.name, port, logic_hind)
                elif "co2" in port or "out_2" in port or port == "out_co2":
                    self._set_output(node.name, port, logic_co2)
                else:
                    self._set_output(node.name, port, logic_hind)

        elif gt == GateType.DECODER3:
            in_main = self._get_value(node.inputs.get("in_main", "0"))
            in_sub = self._get_value(node.inputs.get("in_sub", "0"))
            in_ctrl = self._get_value(node.inputs.get("in_ctrl", "0"))
            logic_1 = min(in_ctrl, in_main)
            logic_2 = min(in_ctrl, 1.0 - in_main, in_sub)
            logic_3 = min(in_ctrl, 1.0 - in_main, 1.0 - in_sub)
            for port in node.outputs:
                if "out_1" in port:
                    self._set_output(node.name, port, logic_1)
                elif "out_2" in port:
                    self._set_output(node.name, port, logic_2)
                elif "out_3" in port:
                    self._set_output(node.name, port, logic_3)

    def _eval_sequential(self, node: CircuitNode) -> None:
        """Evaluate sequential elements (DFF, SR latch, TFF)."""
        gt = node.gate_type

        if gt == GateType.DFF:
            d = self._get_value(node.seq.get("d", "0"))
            clk = self._get_value(node.seq.get("clk", "0"))
            enable = self._get_value(node.seq.get("enable", "0")) if "enable" in node.seq else 1.0
            preset = self._get_value(node.seq.get("preset", "0")) if "preset" in node.seq else 0.0
            reset = self._get_value(node.seq.get("reset", "0")) if "reset" in node.seq else 0.0

            prev_clk = self.prev_clk.get(node.name, 0.0)

            # Continuous DFF: blend toward d on rising clk, weighted by enable
            # preset/reset are continuous overrides
            if preset > 0.5:
                target_q = 1.0
            elif reset > 0.5:
                target_q = 0.0
            elif clk > prev_clk and enable > 0.5:
                target_q = d
            else:
                target_q = node.state.get("q", AC.NOR_DEFAULT)
            
            # Relax toward target
            old_q = node.state.get("q", AC.NOR_DEFAULT)
            node.state["q"] = old_q + AC.M_RISK_GAIN * (target_q - old_q)
            node.state["q_bar"] = 1.0 - node.state["q"]

            self.prev_clk[node.name] = clk
            self._set_output(node.name, "q", node.state["q"])
            self._set_output(node.name, "q_bar", node.state["q_bar"])

        elif gt == GateType.SR_LATCH:
            set_v = self._get_value(node.seq.get("set", "0"))
            reset_v = self._get_value(node.seq.get("reset", "0"))
            enable = self._get_value(node.seq.get("enable", "0")) if "enable" in node.seq else 1.0
            clk = self._get_value(node.seq.get("clk", "0")) if "clk" in node.seq else 1.0

            if enable > 0.5 and clk > 0.5:
                if set_v > 0.5 and reset_v <= 0.5:
                    node.state["q"] = 1.0
                    node.state["q_bar"] = 0.0
                elif reset_v > 0.5 and set_v <= 0.5:
                    node.state["q"] = 0.0
                    node.state["q_bar"] = 1.0

            self._set_output(node.name, "q", node.state["q"])
            self._set_output(node.name, "q_bar", node.state["q_bar"])
            # SR latch with tristate outputs
            for port in node.outputs:
                if port.startswith("set_out"):
                    self._set_output(node.name, port, node.state["q"])
                elif port.startswith("reset_out"):
                    self._set_output(node.name, port, node.state["q_bar"])
                elif port not in ("q", "q_bar"):
                    # tristate channel
                    inp = node.inputs.get("in0") or node.inputs.get("in1")
                    ctrl = node.controls.get("ctrl0") or node.controls.get("ctrl1")
                    if inp and ctrl:
                        cv = self._get_value(ctrl)
                        iv = self._get_value(inp)
                        self._set_output(node.name, port, iv if cv > 0.5 else 0.0)

        elif gt == GateType.TFF:
            clk = self._get_value(node.seq.get("clk", "0"))
            enable = self._get_value(node.seq.get("enable", "0")) if "enable" in node.seq else 1.0
            prev_clk = self.prev_clk.get(node.name, 0.0)

            if clk > 0.5 and prev_clk <= 0.5 and enable > 0.5:
                node.state["t_ff_out"] = 1.0 - node.state.get("t_ff_out", 0.0)

            self.prev_clk[node.name] = clk
            self._set_output(node.name, "t_ff_out", node.state.get("t_ff_out", 0.0))

        # Special: autophagy has both tristate + TFF + SR latch
        if node.name == "autophagy":
            # SR latch part
            s = self._get_value(node.seq.get("s", "0"))
            r = self._get_value(node.seq.get("r", "0"))
            enable = self._get_value(node.seq.get("enable", "0")) if "enable" in node.seq else 1.0
            if s > 0.5 and r <= 0.5:
                node.state["r_out"] = 1.0
            elif r > 0.5:
                node.state["r_out"] = 0.0
            self._set_output(node.name, "r_out", node.state.get("r_out", 0.0))
            self._set_output(node.name, "t_ff_out", node.state.get("t_ff_out", 0.0))

    # Sphere-phase constants for time-varying drive
    # From universe-prose.md: 5-sphere toroidal circulation
    SPHERE_HOURS = {
        "Sun": (0, 3),      # AB_spark
        "Earth": (3, 9),    # A_accumulate
        "Moon": (9, 15),    # O_accumulate
        "CoMag": (15, 21),  # B_accumulate
        "Barnard": (21, 24),# AB_integration
    }
    # Sphere → 8D dimension activity weights (from universe-prose.md 5-sphere ↔ 8D mapping)
    SPHERE_DIM_ACTIVITY = {
        "Sun":     {"r": 0.8, "s": 0.7, "h": 0.3, "d": 0.2, "p": 0.3, "gamma": 0.2, "g": 0.2, "nu": 0.3},
        "Earth":   {"r": 0.3, "s": 0.3, "h": 0.7, "d": 0.3, "p": 0.3, "gamma": 0.8, "g": 0.5, "nu": 0.3},
        "Moon":    {"r": 0.3, "s": 0.3, "h": 0.3, "d": 0.3, "p": 0.8, "gamma": 0.3, "g": 0.3, "nu": 0.7},
        "CoMag":   {"r": 0.3, "s": 0.3, "h": 0.3, "d": 0.3, "p": 0.3, "gamma": 0.5, "g": 0.8, "nu": 0.3},
        "Barnard": {"r": 0.3, "s": 0.3, "h": 0.3, "d": 0.8, "p": 0.3, "gamma": 0.3, "g": 0.7, "nu": 0.3},
    }

    def _get_active_sphere(self, hour: float) -> str:
        for sphere, (start, end) in self.SPHERE_HOURS.items():
            if start <= hour < end:
                return sphere
        return "Sun"

    def _sphere_drive(self, hour: float) -> None:
        """Inject sphere-phase-dependent stimulus into observer seed nodes.
        
        Instead of static 1.0, the observer bootstrap value varies with the
        active sphere's overall activity level, driving the toroidal cycle.
        """
        sphere = self._get_active_sphere(hour)
        dims = self.SPHERE_DIM_ACTIVITY[sphere]
        # Overall sphere activity = mean of all dimension weights
        activity = sum(dims.values()) / len(dims)
        
        # Seed observer nodes with sphere activity (not 1.0)
        # This drives the whole circuit differently per sphere phase
        seeds = {
            "co2": ("out1", activity * 0.8),  # time/adenosine drive
            "co2": ("out0", activity * 0.5),  # respiratory CO2
            "observer_leftd2": ("out0", activity),  # master bus
            "observer_left_endorphin_electron_antineutrino": ("out0", activity),
            "nonobserver_left_d2": ("out", activity),
            "left_endorphin_non_observer": ("out", activity),
            "left_genital_d2_out0_nand": ("out", activity),
        }
        for node_name, (port, val) in seeds.items():
            self._set_output(node_name, port, val, hard=True)

    def step(self, hour: float = None, max_iter: int = 50) -> None:
        """One simulation step: evaluate all nodes until stable.
        
        If hour is provided, inject sphere-phase-dependent stimulus first.
        """
        if hour is not None:
            self.current_hour = hour
            self._sphere_drive(hour)
        
        for iteration in range(max_iter):
            changed = False
            prev_values = {n: dict(v) for n, v in self.values.items()}

            for node in self.nodes.values():
                if node.gate_type in (GateType.DFF, GateType.SR_LATCH, GateType.TFF):
                    self._eval_sequential(node)
                elif node.name == "autophagy":
                    self._eval_sequential(node)
                else:
                    self._eval_combinational(node)

            # check convergence
            for n, ports in self.values.items():
                for p, v in ports.items():
                    if abs(v - prev_values.get(n, {}).get(p, 0.0)) > 0.001:
                        changed = True
                        break
                if changed:
                    break

            if not changed:
                break

        self.iteration += 1

    def get_node_output(self, node_name: str, port: str = "out0") -> float:
        return self.values.get(node_name, {}).get(port, 0.0)

    def get_all_outputs(self) -> Dict[str, Dict[str, float]]:
        return self.values


# ---------------------------------------------------------------------------
# 8D vector computation from circuit state
# ---------------------------------------------------------------------------

# Node → music dimension mapping (from circuit file header)
NODE_MUSIC_MAP = {
    "heme":                  {"dims": ["s", "d"],     "channels": {"out0": "s", "out1": "d"}},
    "cytochrome_c_oxidase":  {"dims": ["r", "d"],     "channels": {"out0": "r", "out1": "d"}},
    "water_vapour":          {"dims": ["g"],          "channels": {"out0": "g", "out1": "g"}},
    "steel":                 {"dims": ["s", "gamma"], "channels": {"out0": "s", "out1": "gamma"}},
    "clay_gouge":            {"dims": ["g"],          "channels": {"out0": "g"}},
    "quark_orogen_magma":    {"dims": ["nu"],         "channels": {"out0": "nu"}},
    "observer_leftd2":       {"dims": ["p"],          "channels": {"out0": "p"}},
    "histosol":              {"dims": ["h"],          "channels": {"out0": "h", "out1": "h"}},
    "sulforaphane":          {"dims": ["g", "nu"],    "channels": {"out0": "g", "out1": "nu"}},
    "aurora":                {"dims": ["s", "gamma"], "channels": {"out0": "s", "out0_gamma": "gamma"}},
    "glymphatic_system":     {"dims": ["g"],          "channels": {"out0": "g"}},
    "cysteine":              {"dims": ["s"],          "channels": {"out0": "s"}},
    "memory_entropy":        {"dims": ["r", "h", "nu"],"channels": {"out_hind_insula": "r", "out_co2": "nu"}},
    "hind_insula":           {"dims": ["d", "s"],     "channels": {"out0": "d"}},
    "carbon":                {"dims": ["p", "nu"],    "channels": {"q": "p", "q_bar": "nu"}},
    "fold_belt":             {"dims": ["r", "gamma"], "channels": {"out0": "r", "out1": "gamma"}},
    "succinate_dehydrogenase":{"dims": ["r", "d"],    "channels": {"out0": "r", "out1": "h", "out2": "s"}},
    "collagen":              {"dims": ["h"],          "channels": {"out0": "h"}},
    "cambisol":              {"dims": ["h", "g"],     "channels": {"out0": "h", "out1": "g"}},
    "NaCl":                  {"dims": ["r", "d"],     "channels": {"out0": "r", "out1": "d"}},
    "sodium":                {"dims": ["r", "s"],     "channels": {"out0": "r", "out1": "s"}},
    "nitrogenase":           {"dims": ["p", "nu"],    "channels": {"out_1": "p", "out_2": "nu"}},
    "chlorine_ion_pump":     {"dims": ["d"],          "channels": {"out0": "d"}},
    "podzol":                {"dims": ["h", "gamma"], "channels": {"out0": "h", "out1": "gamma"}},
    "lower_mantle":          {"dims": ["nu", "gamma"], "channels": {"q": "nu", "q_bar": "gamma"}},
    "basin":                 {"dims": ["g", "gamma"], "channels": {"q": "g", "q_bar": "gamma"}},
    "co2":                   {"dims": ["p", "r"],     "channels": {"out0": "p", "out1": "r"}},
    "glp1":                  {"dims": ["s"],          "channels": {"q": "s", "q_bar": "s"}},
    "laterite":              {"dims": ["s", "d"],     "channels": {"q": "s", "q_bar": "d"}},
    "male_right_oxytocin":   {"dims": ["h", "nu"],    "channels": {"q": "h", "q_bar": "nu"}},
    "gluon_orogen":          {"dims": ["h"],          "channels": {"q": "h", "q_bar": "h"}},
    "lactate_dehydrogenase": {"dims": ["nu", "r"],    "channels": {"out0": "nu", "out1": "r"}},
    "magnetite":             {"dims": ["s", "gamma"], "channels": {"out0": "s"}},
    "ferritin":              {"dims": ["s"],          "channels": {"out0": "s", "out1": "s"}},
    "methylation":           {"dims": ["p", "nu"],    "channels": {"out0": "p", "out1": "nu"}},
    "right_acetylcholine":   {"dims": ["r", "h"],     "channels": {"out0": "r"}},
    "peonidine":             {"dims": ["h", "gamma"], "channels": {"out0": "h", "out1": "gamma"}},
    "actomyosin":            {"dims": ["r", "d"],     "channels": {"out0": "r", "out1": "d"}},
    "sulfur_iron_complex":   {"dims": ["d", "s"],     "channels": {"out0": "d", "out1": "s"}},
    "pyrite":                {"dims": ["p"],          "channels": {"out0": "p", "out1": "p"}},
    "right_sole_dopamine":   {"dims": ["p"],          "channels": {"q": "p", "q_bar": "p"}},
    "plume":                 {"dims": ["nu", "gamma"], "channels": {"out0": "nu"}},
    "subduction_zone":       {"dims": ["nu", "gamma"], "channels": {"out0": "nu", "out1": "gamma"}},
    "craton":                {"dims": ["g", "nu"],    "channels": {"out0": "g", "out1": "nu"}},
    "oxidised_manganese":    {"dims": ["d", "s"],     "channels": {"out1": "s", "set_out": "s", "reset_out": "d"}},
    "manganese_oxygen_complex": {"dims": ["nu", "gamma"], "channels": {"out0": "nu", "out1": "gamma"}},
    "pi_electron_cloud":     {"dims": ["nu"],         "channels": {"out0": "nu"}},
    "large_igneous_province": {"dims": ["s", "d"],    "channels": {"out0": "s", "out1": "d"}},
    "autophagy":             {"dims": ["d", "p"],     "channels": {"out0": "d", "r_out": "d", "t_ff_out": "p"}},
    "adapter_protein":       {"dims": ["p"],          "channels": {"q": "p", "q_bar": "p"}},
    "mc1r":                  {"dims": ["p"],          "channels": {"q": "p", "q_bar": "p"}},
    "manganese_nodule":      {"dims": ["g"],          "channels": {"q": "g", "q_bar": "g"}},
    "pentose_phosphate":     {"dims": ["p", "nu"],    "channels": {"out_1": "p", "out_2": "nu"}},
    "water":                 {"dims": ["g"],          "channels": {"out0": "g"}},
    "caco3_final_and":       {"dims": ["r", "h"],     "channels": {"out": "r"}},
    "left_genital_d2":       {"dims": ["p"],          "channels": {"out0": "p"}},
    "observer_left_endorphin_electron_antineutrino": {"dims": ["nu"], "channels": {"out0": "nu"}},
}


def compute_8d(sim: CircuitSimulator) -> Dict[str, float]:
    """Compute 8D music vector from current circuit state.

    8D = {r, h, d, p, s, gamma, g, nu}
    Each dimension takes the max active node output mapped to that dimension.
    """
    vec = {d: 0.0 for d in ("r", "h", "d", "p", "s", "gamma", "g", "nu")}

    for node_name, mapping in NODE_MUSIC_MAP.items():
        if node_name not in sim.values:
            continue
        for port, dim in mapping["channels"].items():
            val = sim.values[node_name].get(port, 0.0)
            if val > vec[dim]:
                vec[dim] = val

    return vec


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    md = pathlib.Path(__file__).parent.parent / "circuitfile-rewritten.md"
    nodes = parse_circuit(md)
    print(f"Parsed {len(nodes)} nodes")

    from collections import Counter
    gt_counts = Counter(n.gate_type.value for n in nodes.values())
    for gt, count in gt_counts.most_common():
        print(f"  {gt}: {count}")

    sim = CircuitSimulator(nodes)

    # 24-hour sphere-driven sweep
    ALL_DIMS = ["r", "h", "d", "p", "s", "gamma", "g", "nu"]
    hourly_8d = {}

    print("\n" + "=" * 80)
    print("CONSTANT-DRIVEN CIRCUIT SIMULATION (24h sphere sweep)")
    print(f"Constants: NOR_DEFAULT={AC.NOR_DEFAULT:.5f}  PLP_DEFAULT={AC.PLP_DEFAULT:.5f}  "
          f"GAIN={AC.M_RISK_GAIN}  DECAY={AC.LAMBDA_RISK_DECAY}")
    print("=" * 80)

    for hour in range(24):
        sim.step(hour=float(hour))
        vec = compute_8d(sim)
        hourly_8d[hour] = dict(vec)
        sphere = sim._get_active_sphere(float(hour))
        vec_str = "  ".join(f"{d}={vec[d]:.2f}" for d in ALL_DIMS)
        print(f"  {hour:02d}:00 [{sphere:8s}] {vec_str}")

    # Compute 24h average 8D
    avg_8d = {}
    for d in ALL_DIMS:
        avg_8d[d] = sum(hourly_8d[h][d] for h in range(24)) / 24.0

    print(f"\n24h Average 8D:")
    print(f"  " + "  ".join(f"{d}={avg_8d[d]:.3f}" for d in ALL_DIMS))

    # Save
    out = pathlib.Path(__file__).parent / "generated" / "circuit_constants_state.json"
    out.parent.mkdir(exist_ok=True)
    state = {
        "hourly_8d": hourly_8d,
        "avg_8d": avg_8d,
        "constants": {
            "NOR_DEFAULT": AC.NOR_DEFAULT,
            "PLP_DEFAULT": AC.PLP_DEFAULT,
            "M_RISK_GAIN": AC.M_RISK_GAIN,
            "LAMBDA_RISK_DECAY": AC.LAMBDA_RISK_DECAY,
            "OMEGA": AC.OMEGA,
        },
        "iteration": sim.iteration,
    }
    out.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"\nSaved state -> {out}")
