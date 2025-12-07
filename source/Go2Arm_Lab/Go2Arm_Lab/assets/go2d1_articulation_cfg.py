import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# GO2D1_USD = os.path.join(current_dir, "go2_d1.usd")
GO2D1_USD = "/home/adam/ChongQing/Go2Arm_Lab/source/Go2Arm_Lab/Go2Arm_Lab/assets/go2_d1_description/urdf/go2_d1/go2_d1_v1.usd"

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

##
# Configuration for Go2 + D1 Arm
##

GO2D1_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=GO2D1_USD,
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
            # D1 arm joints (6 DOF)
            "arm_joint1": 0.0,      # Base rotation (yaw)
            "arm_joint2": 0.0,      # Shoulder pitch
            "arm_joint3": 0.1,      # Elbow pitch
            "arm_joint4": 0.0,      # Wrist roll
            "arm_joint5": -0.54,    # Wrist pitch
            "arm_joint6": 0.0,      # Wrist yaw
            # D1 gripper joints
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
            # D1 specs from URDF:
            # joints 1-3: effort=3.33, velocity=1.05
            # joints 4-6: effort=1.67, velocity=1.73
            effort_limit=10.0,
            saturation_effort=10.0,
            velocity_limit=2.0,
            stiffness=10.0,
            damping=0.5,
            friction=0.0,
        ),
        "d1_gripper": DCMotorCfg(
            joint_names_expr=["arm_gripper.*_joint"],
            effort_limit=15.0,
            saturation_effort=15.0,
            velocity_limit=0.02,
            stiffness=5.0,
            damping=0.5,
            friction=0.0,
        ),
    },
)

# Keep backward compatibility - alias to old name
GO2ARM_CFG = GO2D1_CFG
