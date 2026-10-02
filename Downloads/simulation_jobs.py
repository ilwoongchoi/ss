#!/usr/bin/env python3
"""Compute personality mapping (128 profiles) for simulation-domain jobs.

Domain: fighter / tank / vehicle simulation games + training products + digital twins.
We map each job to a weighted 8D target profile, then rank all 128 personalities.

8D interpretation (consistent with existing framework names):
- r: execution/iteration density (real-time responsiveness, tuning loops)
- h: multi-factor complexity/creativity (complex interactions, design synthesis)
- d: hardness/edge-case tolerance (damage, failure modes, safety constraints)
- p: process/discipline/predictability (verification, spec adherence)
- s: perception/visual attention (rendering, UI, visualization)
- gamma: spatial/immersion (3D space, acoustics, environment)
- g: system architecture/structure (integration, time/step control)
- nu: recursion/long-horizon modeling (feedback loops, AI planning, ecosystems)
"""

from particle_to_8d import particles_to_dims, MBTI_TYPES, BLOOD_TYPES, GENDERS

PROFILES = [f"{mbti}_{g}_{b}" for mbti in MBTI_TYPES for g in GENDERS for b in BLOOD_TYPES]

# A fairly comprehensive set of roles across the simulation pipeline.
# weights: positive means "more is better".
JOBS = {
    # Core simulation science / modeling
    "Flight_Model_Dynamics_Engineer":          {"p":3, "s":1, "h":1, "d":4, "r":3, "gamma":3, "g":3, "nu":2},
    "Ground_Vehicle_Dynamics_Engineer":        {"p":3, "s":1, "h":1, "d":4, "r":3, "gamma":2, "g":3, "nu":2},
    "Ballistics_Penetration_Damage_Modeler":   {"p":4, "s":0, "h":0, "d":5, "r":3, "gamma":1, "g":3, "nu":1},
    "Sensor_Radar_IR_EO_Modeler":              {"p":4, "s":2, "h":1, "d":4, "r":2, "gamma":2, "g":3, "nu":3},
    "EW_Signals_Propagation_Modeler":          {"p":3, "s":1, "h":1, "d":4, "r":2, "gamma":2, "g":3, "nu":4},
    "Atmosphere_Weather_Propagation_Modeler":  {"p":2, "s":2, "h":2, "d":2, "r":2, "gamma":4, "g":2, "nu":4},
    "Terrain_Geospatial_Synthesis_Engineer":    {"p":2, "s":4, "h":2, "d":2, "r":2, "gamma":3, "g":2, "nu":3},
    "Physics_Integrator_TimeStep_Engineer":     {"p":4, "s":0, "h":0, "d":4, "r":4, "gamma":1, "g":4, "nu":2},

    # Real-time engine / graphics / performance
    "RealTime_Engine_Systems_Architect":       {"p":4, "s":1, "h":0, "d":3, "r":4, "gamma":1, "g":5, "nu":2},
    "Rendering_Graphics_Engineer":             {"p":2, "s":5, "h":2, "d":2, "r":3, "gamma":3, "g":2, "nu":1},
    "Performance_Optimization_Engineer":       {"p":4, "s":1, "h":0, "d":3, "r":5, "gamma":1, "g":4, "nu":1},
    "Tools_Pipeline_Engineer":                 {"p":5, "s":1, "h":0, "d":2, "r":4, "gamma":1, "g":4, "nu":1},
    "Build_Release_DevOps_SRE":                {"p":5, "s":0, "h":0, "d":3, "r":4, "gamma":1, "g":4, "nu":1},

    # Networking / multiplayer / security
    "Netcode_Multiplayer_Engineer":            {"p":4, "s":0, "h":0, "d":3, "r":5, "gamma":1, "g":4, "nu":2},
    "AntiCheat_Security_Engineer":             {"p":4, "s":0, "h":0, "d":5, "r":4, "gamma":0, "g":3, "nu":3},

    # AI / autonomy / behavior
    "Tactical_AI_Behavior_Engineer":           {"p":3, "s":1, "h":2, "d":3, "r":3, "gamma":1, "g":3, "nu":5},
    "Autonomy_PathPlanning_Swarm":             {"p":3, "s":1, "h":1, "d":3, "r":3, "gamma":2, "g":3, "nu":5},
    "ML_Telemetry_Balance_Scientist":          {"p":4, "s":1, "h":1, "d":3, "r":3, "gamma":1, "g":3, "nu":4},

    # Human factors / UX / cockpit / training
    "Cockpit_HMI_UX_Designer":                 {"p":3, "s":5, "h":2, "d":1, "r":2, "gamma":2, "g":2, "nu":1},
    "Human_Factors_Training_Designer":         {"p":3, "s":3, "h":3, "d":2, "r":2, "gamma":3, "g":2, "nu":2},
    "Simulation_Instructor_Operator":          {"p":3, "s":2, "h":2, "d":2, "r":3, "gamma":2, "g":2, "nu":2},

    # Content / mission / scenario / worldbuilding
    "Mission_Scenario_Designer":               {"p":2, "s":2, "h":4, "d":2, "r":2, "gamma":3, "g":2, "nu":3},
    "Doctrine_RulesOfEngagement_Designer":      {"p":4, "s":0, "h":1, "d":4, "r":2, "gamma":0, "g":4, "nu":3},
    "Vehicle_Systems_Designer_Loadout":        {"p":3, "s":1, "h":2, "d":3, "r":3, "gamma":1, "g":3, "nu":2},
    "3D_Environment_Artist_Terrain":           {"p":1, "s":5, "h":3, "d":1, "r":2, "gamma":3, "g":1, "nu":2},
    "Vehicle_HardSurface_Artist":              {"p":2, "s":5, "h":2, "d":1, "r":3, "gamma":2, "g":1, "nu":1},
    "Technical_Artist_Shaders":                {"p":3, "s":5, "h":2, "d":2, "r":3, "gamma":2, "g":2, "nu":1},
    "Sound_Designer_Vehicle_Ambience":         {"p":1, "s":2, "h":5, "d":2, "r":2, "gamma":5, "g":1, "nu":3},

    # QA / verification / certification (games + defense-grade)
    "QA_Test_Automation":                      {"p":5, "s":2, "h":0, "d":3, "r":4, "gamma":0, "g":3, "nu":1},
    "Verification_Validation_Safety":          {"p":5, "s":1, "h":0, "d":4, "r":3, "gamma":0, "g":4, "nu":2},

    # Product / program / customer integration
    "Program_Manager_Simulation_Product":      {"p":5, "s":1, "h":1, "d":2, "r":3, "gamma":1, "g":4, "nu":1},
    "Defense_Customer_Integration_Engineer":   {"p":4, "s":2, "h":1, "d":3, "r":3, "gamma":1, "g":4, "nu":1},
    "Standards_Compliance_Licensing":          {"p":5, "s":0, "h":0, "d":3, "r":2, "gamma":0, "g":4, "nu":1},

    # Emerging: digital twins / synthetic environments
    "DigitalTwin_Architect":                   {"p":4, "s":2, "h":1, "d":3, "r":3, "gamma":2, "g":5, "nu":3},
    "SyntheticEnvironment_DataEngineer":       {"p":4, "s":2, "h":0, "d":3, "r":3, "gamma":2, "g":4, "nu":3},
}


def top_profiles_for(weights, k=3):
    scored = []
    for label in PROFILES:
        d = particles_to_dims(label, "day")["dims"]
        score = 0.0
        for dim, w in weights.items():
            score += d.get(dim, 0.5) * w
        scored.append((label, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(lbl, round(sc, 4)) for lbl, sc in scored[:k]]


def main():
    for job, weights in JOBS.items():
        tops = top_profiles_for(weights, k=3)
        print(f"{job}: {tops[0][0]} | {tops[1][0]} | {tops[2][0]}")


if __name__ == "__main__":
    main()
