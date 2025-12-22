"""Base environment configuration for Go2 + ARX5 robot."""

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

from Go2Arm_Lab.tasks.manager_based.go2arm_lab.go2arm_lab_env_cfg import LocomotionVelocityEnvCfg
from Go2Arm_Lab.assets.go2arx5_articulation_cfg import GO2ARX5_CFG
import Go2Arm_Lab.tasks.manager_based.go2arm_lab.mdp as mdp


@configclass
class Go2ARX5ActionsCfg:
    """Action specifications for Go2 + X5A (using only 6 arm joints, not gripper)."""
    
    joint_pos = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=[
            "FL_hip_joint", "FL_thigh_joint", "FL_calf_joint",
            "FR_hip_joint", "FR_thigh_joint", "FR_calf_joint",
            "RL_hip_joint", "RL_thigh_joint", "RL_calf_joint",
            "RR_hip_joint", "RR_thigh_joint", "RR_calf_joint",
            "joint1", "joint2", "joint3",
            "joint4", "joint5", "joint6"
            # Note: joint7, joint8 (gripper) not controlled to maintain 18 actions (12 legs + 6 arm)
        ],
        scale={
            ".*_hip_joint": 0.5,
            ".*_thigh_joint": 0.5,
            ".*_calf_joint": 0.5,
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
class Go2ARX5BaseEnvCfg(LocomotionVelocityEnvCfg):
    """Base configuration for Go2 + ARX5 environment."""

    def __post_init__(self):
        super().__post_init__()
        
        # Update robot configuration
        self.scene.robot = GO2ARX5_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        self.actions = Go2ARX5ActionsCfg()
        
        # Update sensor paths (ARX5 uses "base" not "base_link")
        self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/base"
        self.scene.contact_forces.prim_path = "{ENV_REGEX_NS}/Robot/.*"
        
        # Update event configurations for X5A body names
        self.events.add_base_mass.params["asset_cfg"] = SceneEntityCfg("robot", body_names="base")
        self.events.add_ee_mass.params["asset_cfg"] = SceneEntityCfg("robot", body_names="link6")
        # Fix base_external_force_torque to use "base" instead of "base_link"
        self.events.base_external_force_torque.params["asset_cfg"] = SceneEntityCfg("robot", body_names="base")
        
        # Update termination conditions
        self.terminations.base_contact.params["sensor_cfg"] = SceneEntityCfg("contact_forces", body_names="base")
        
        # Update reward configurations for X5A body names
        self.rewards.arm_self_collision.params["sensor_cfg"] = SceneEntityCfg("contact_forces", body_names=["link[1-8]", "x5a_base_link"])
        self.rewards.end_effector_position_tracking.params["asset_cfg"] = SceneEntityCfg("robot", body_names="link6")
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"] = SceneEntityCfg("robot", body_names="link6")


@configclass
class Go2ARX5BaseEnvCfg_PLAY(Go2ARX5BaseEnvCfg):
    """Configuration for Go2 + ARX5 play mode."""
    
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        self.observations.policy.enable_corruption = False
        self.events.base_external_force_torque = None
        self.events.push_robot = None
        self.curriculum = None
