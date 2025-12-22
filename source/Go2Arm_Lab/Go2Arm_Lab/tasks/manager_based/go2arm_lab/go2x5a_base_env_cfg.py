"""Base environment configuration for Go2 + X5A robot."""

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

from Go2Arm_Lab.tasks.manager_based.go2arm_lab.go2arm_lab_env_cfg import LocomotionVelocityEnvCfg
from Go2Arm_Lab.assets.go2x5a_articulation_cfg import GO2X5A_CFG
import Go2Arm_Lab.tasks.manager_based.go2arm_lab.mdp as mdp


@configclass
class Go2X5AActionsCfg:
    """Action specifications for Go2 + X5A."""
    
    joint_pos = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=[
            # Go2 leg joints (12 DOF)
            "FL_hip_joint", "FL_thigh_joint", "FL_calf_joint",
            "FR_hip_joint", "FR_thigh_joint", "FR_calf_joint",
            "RL_hip_joint", "RL_thigh_joint", "RL_calf_joint",
            "RR_hip_joint", "RR_thigh_joint", "RR_calf_joint",
            # X5A arm joints (6 DOF revolute) - NOT including gripper joints 7-8
            "joint1", "joint2", "joint3",
            "joint4", "joint5", "joint6"
        ],
        scale={
            # Leg joints
            ".*_hip_joint": 0.5,
            ".*_thigh_joint": 0.5,
            ".*_calf_joint": 0.5,
            # X5A arm joints
            "joint1": 0.25,
            "joint2": 0.25,
            "joint3": 0.25,
            "joint4": 0.25,
            "joint5": 0.25,
            "joint6": 0.25,
        },
        use_default_offset=True,
    )


@configclass
class Go2X5ABaseEnvCfg(LocomotionVelocityEnvCfg):
    """Base configuration for Go2 + X5A environment."""

    def __post_init__(self):
        super().__post_init__()
        
        # Update robot configuration to use X5A
        self.scene.robot = GO2X5A_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        self.actions = Go2X5AActionsCfg()
        
        # Update sensor paths (X5A uses "base" like Go2, not "x5a_base_link")
        self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/base"
        self.scene.contact_forces.prim_path = "{ENV_REGEX_NS}/Robot/.*"
        
        # Update event configurations for X5A body names
        self.events.add_base_mass.params["asset_cfg"] = SceneEntityCfg("robot", body_names="base")
        self.events.add_ee_mass.params["asset_cfg"] = SceneEntityCfg("robot", body_names="link6")
        # Fix base_external_force_torque to use "base" instead of "base_link"
        self.events.base_external_force_torque.params["asset_cfg"] = SceneEntityCfg("robot", body_names="base")
        
        # Update termination conditions
        self.terminations.base_contact.params["sensor_cfg"] = SceneEntityCfg("contact_forces", body_names="base")
        
        # Update reward configurations for X5A
        # X5A has link1-6, similar naming to ARX5
        self.rewards.arm_self_collision.params["sensor_cfg"] = SceneEntityCfg(
            "contact_forces", body_names=["link[1-6]", "x5a_base_link"]
        )
        self.rewards.end_effector_position_tracking.params["asset_cfg"] = SceneEntityCfg(
            "robot", body_names="link6"
        )
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"] = SceneEntityCfg(
            "robot", body_names="link6"
        )


@configclass
class Go2X5ABaseEnvCfg_PLAY(Go2X5ABaseEnvCfg):
    """Configuration for Go2 + X5A play mode."""
    
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        self.observations.policy.enable_corruption = False
        self.events.base_external_force_torque = None
        self.events.push_robot = None
        self.curriculum = None
