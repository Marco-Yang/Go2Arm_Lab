"""Configuration for the Unitree Go2 + X5A robot."""

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the Go2+X5A URDF file
GO2X5A_URDF_PATH = os.path.join(current_dir, "go2_x5a/go2_x5a.urdf")

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

##
# Configuration for Unitree Go2 + X5A Arm
##

GO2X5A_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=GO2X5A_URDF_PATH,
        activate_contact_sensors=True,
        fix_base=False,
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
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            drive_type="force",
            target_type="position",
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=0.0,
                damping=None,
            ),
        ),
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
            
            # X5A arm joints (6 revolute + 2 prismatic for gripper)
            "joint1": 0.0,      # Base rotation
            "joint2": 0.5,      # Shoulder pitch
            "joint3": 1.0,      # Elbow pitch  
            "joint4": 0.0,      # Wrist pitch
            "joint5": 0.0,      # Wrist roll
            "joint6": 0.0,      # End effector rotation
            "joint7": 0.02,     # Gripper finger 1
            "joint8": 0.02,     # Gripper finger 2
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
        "x5a_arm": DCMotorCfg(
            joint_names_expr=["joint[1-6]"],
            effort_limit=100.0,
            saturation_effort=80.0,
            velocity_limit=10.0,
            stiffness=100.0,
            damping=3.0,
            friction=0.1,
        ),
        "x5a_gripper": ImplicitActuatorCfg(
            joint_names_expr=["joint[7-8]"],
            effort_limit=100.0,
            velocity_limit=1.0,
            stiffness=1000.0,
            damping=100.0,
        ),
    },
)
