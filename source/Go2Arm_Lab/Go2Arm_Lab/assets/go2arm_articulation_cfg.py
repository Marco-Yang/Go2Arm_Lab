import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# Updated to use Go2 + D1 arm USD file
GO2ARM_USD = os.path.join(current_dir, "go2_d1.usd")

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

##
# Configuration - Now using Unitree D1 Arm
##

GO2ARM_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=GO2ARM_USD,
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=0,
        ),
        # collision_props=sim_utils.CollisionPropertiesCfg(
        #     collision_enabled=True,
        #     contact_offset=0.02,
        #     rest_offset=0.005 ,
        # ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.35),
        joint_pos={
            # Go2 leg joints
            ".*L_hip_joint": 0.1,
            ".*R_hip_joint": -0.1,
            "F[L,R]_thigh_joint": 0.8,
            "R[L,R]_thigh_joint": 1.0,
            ".*_calf_joint": -1.5,
            # D1 arm joints (6 DOF) - within D1-550 limits
            # Joint1: ±135° (±2.36 rad)
            # Joint2,3,5: ±90° (±1.57 rad)  
            # Joint4,6: ±135° (±2.36 rad)
            "arm_joint1": 0.0,      # Base rotation: 0° (within ±135°)
            "arm_joint2": 0.0,      # Shoulder pitch: 0° (within ±90°)
            "arm_joint3": 0.1,      # Elbow pitch: ~5.7° (within ±90°)
            "arm_joint4": 0.0,      # Wrist roll: 0° (within ±135°)
            "arm_joint5": -0.54,    # Wrist pitch: ~-31° (within ±90°)
            "arm_joint6": 0.0,      # End effector roll: 0° (within ±135°)
            # D1 gripper joints (0-65mm stroke)
            "arm_gripper_left_joint": 0.0,
            "arm_gripper_right_joint": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "base_legs": DCMotorCfg(
            joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
            effort_limit=40.5,
            saturation_effort=23.5,
            velocity_limit=30.0,
            stiffness=40.0,
            damping=1.0,
            friction=0.0,
        ),
        "d1_arm": DCMotorCfg(
            joint_names_expr=["arm_joint[1-6]"],
            # D1-550 arm specifications from URDF and official docs:
            # Joint1-3: effort=3.33 N·m, velocity=1.05 rad/s
            # Joint4-6: effort=1.67 N·m, velocity=1.73 rad/s
            # Using average values for simplified control
            effort_limit=3.33,      # Max torque from joint1-3
            saturation_effort=3.0,   # Slightly lower for safety
            velocity_limit=1.73,     # Max velocity from joint4-6
            stiffness=20.0,          # Moderate stiffness for D1
            damping=1.0,             # Moderate damping
            friction=0.1,            # Small friction
        ),
        "d1_gripper": DCMotorCfg(
            joint_names_expr=["arm_gripper.*_joint"],
            # D1 gripper: 0-65mm stroke (prismatic joints)
            effort_limit=10.0,       # Reasonable gripper force
            saturation_effort=8.0,
            velocity_limit=0.1,      # Slow gripper movement
            stiffness=50.0,          # High stiffness for gripper
            damping=2.0,             # High damping for stability
            friction=0.2,
        ),
    },
)

