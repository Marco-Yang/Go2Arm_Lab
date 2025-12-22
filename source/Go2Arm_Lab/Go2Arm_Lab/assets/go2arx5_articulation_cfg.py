"""Configuration for the Unitree Go2 + X5A robot."""

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the Go2+X5A URDF file
# Updated to use official X5A arm URDF with correct meshes
GO2ARX5_URDF_PATH = os.path.join(current_dir, "go2_arx5/go2_arx5_finray_x85_z94.urdf")

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

##
# Configuration for Unitree Go2 + ARX5 Arm
##

GO2ARX5_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=GO2ARX5_URDF_PATH,
        activate_contact_sensors=True,
        fix_base=False,  # ✅ Added: Robot is not fixed to the ground
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
        # ✅ Added: Joint drive configuration with stiffness
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            drive_type="force",
            target_type="position",
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=0.0,  # Will be overridden by actuator configs
                damping=None,
            ),
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.35),
        joint_pos={
            # Go2 leg joints - same as before
            ".*L_hip_joint": 0.1,
            ".*R_hip_joint": -0.1,
            "F[L,R]_thigh_joint": 0.8,
            "R[L,R]_thigh_joint": 1.0,
            ".*_calf_joint": -1.5,
            
            # X5A arm joints - original ARX5 pose
            "joint1": 0.0,      # Base rotation: neutral
            "joint2": 0.3,      # Shoulder pitch
            "joint3": 0.5,      # Elbow pitch
            "joint4": 0.0,      # Wrist joint 1: neutral
            "joint5": 0.0,      # Wrist joint 2: neutral
            "joint6": 0.0,      # Wrist joint 3: neutral
            "joint7": 0.0,      # Gripper finger 1: closed
            "joint8": 0.0,      # Gripper finger 2: closed
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "base_legs": DCMotorCfg(
            joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
            # Go2 leg actuator specs
            effort_limit=40.5,
            saturation_effort=23.5,
            velocity_limit=30.0,
            stiffness=40.0,
            damping=1.0,
            friction=0.0,
        ),
        "x5a_arm": DCMotorCfg(
            joint_names_expr=["joint[1-6]"],
            # X5A arm specifications - using conservative values for stability
            # Note: URDF specifies effort=100 N·m, velocity=1000 rad/s
            # But we use lower values similar to ARX5 for stable training
            effort_limit=30.0,      # Same as ARX5 for stability
            saturation_effort=25.0,
            velocity_limit=10.0,    # CRITICAL: Use 10.0 not 1000.0!
            stiffness=100.0,
            damping=3.0,
            friction=0.1,
        ),
        "x5a_gripper": ImplicitActuatorCfg(
            joint_names_expr=["joint[7-8]"],
            # X5A gripper (prismatic joints)
            effort_limit=100.0,
            velocity_limit=100.0,
            stiffness=1000.0,
            damping=50.0,
        ),
    },
)
