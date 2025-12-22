# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for the Go2+ARX5 robot on flat terrain."""

from isaaclab.utils import configclass

from Go2Arm_Lab.tasks.manager_based.go2arm_lab.go2arx5_base_env_cfg import Go2ARX5BaseEnvCfg
from Go2Arm_Lab.assets.go2arx5_articulation_cfg import GO2ARX5_CFG


@configclass
class Go2ARX5FlatEnvCfg(Go2ARX5BaseEnvCfg):
    """Configuration for Go2+ARX5 robot on flat terrain."""
    
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        
        # Replace robot with Go2+ARX5
        self.scene.robot = GO2ARX5_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Disable push robot event for flat terrain
        self.events.push_robot = None

        # Use flat terrain instead of generated terrain
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None

        # ================================================================================================================================
        # Velocity command configuration - Accelerated curriculum learning (4000→1000, 4x faster)
        # ================================================================================================================================
        self.commands.base_velocity.curriculum_coeff = 1000
        # init
        self.commands.base_velocity.ranges_init.lin_vel_x  = (0.0, 0.0)
        self.commands.base_velocity.ranges_init.lin_vel_y  = (-0.0, 0.0)
        self.commands.base_velocity.ranges_init.ang_vel_z  = (-0.0, 0.0)
        # final
        self.commands.base_velocity.ranges_final.lin_vel_x = (0.0, 1.0)
        self.commands.base_velocity.ranges_final.lin_vel_y = (-0.5, 0.5)
        self.commands.base_velocity.ranges_final.ang_vel_z = (-0.5, 0.5)
  
        # ================================================================================================================================
        # Position command (end-effector) - Accelerated curriculum learning (5000→1500, 3.3x faster)
        # ================================================================================================================================
        self.commands.ee_pose.curriculum_coeff = 1500
        self.commands.ee_pose.body_name = "link6"  # ARX5 end-effector link name
        
        # init - conservative workspace
        self.commands.ee_pose.ranges_init.pos_x = (0.45, 0.5)
        self.commands.ee_pose.ranges_init.pos_y = (-0.05, 0.05)
        self.commands.ee_pose.ranges_init.pos_z = (0.45, 0.5)
        # final - expanded workspace
        self.commands.ee_pose.ranges_final.pos_x = (0.4, 0.65)
        self.commands.ee_pose.ranges_final.pos_y = (-0.35, 0.35)
        self.commands.ee_pose.ranges_final.pos_z = (0.15, 0.6)

        # ================================================================================================================================
        # Reward weights
        # ================================================================================================================================
        # ARM manipulation rewards
        self.rewards.end_effector_position_tracking.weight = 3.0
        self.rewards.end_effector_orientation_tracking.weight = -2.0
        self.rewards.end_effector_action_rate.weight = -0.01
        self.rewards.end_effector_action_smoothness.weight = -0.04
        
        # LEG locomotion rewards  
        self.rewards.tracking_lin_vel_x_l1.weight = 3.5
        self.rewards.track_ang_vel_z_exp.weight = 2.0
        self.rewards.lin_vel_z_l2.weight = -2.5
        self.rewards.ang_vel_xy_l2.weight = -0.05
        self.rewards.dof_torques_l2.weight = -2.0e-5
        self.rewards.dof_acc_l2.weight = -2.5e-7
        self.rewards.action_rate_l2.weight = -0.01
        
        # Gait rewards
        self.rewards.feet_air_time.weight = 0.0
        self.rewards.F_feet_air_time.weight = 1.0
        self.rewards.R_feet_air_time.weight = 1.0
        self.rewards.feet_height.weight = -0.0
        self.rewards.feet_height_body.weight = -3.0
        self.rewards.foot_contact.weight = 0.003
        
        # Posture & stability rewards
        self.rewards.hip_deviation.weight = -0.2
        self.rewards.joint_deviation.weight = -0.01
        self.rewards.action_smoothness.weight = -0.02
        self.rewards.height_reward.weight = -2.0
        self.rewards.flat_orientation_l2.weight = -1.0
        
        # Mobile manipulation specific rewards
        self.rewards.arm_self_collision.weight = -1.0
        self.rewards.base_motion_diversity.weight = 0.5
        self.rewards.stationary_base_penalty.weight = -0.3


@configclass
class Go2ARX5FlatEnvCfg_PLAY(Go2ARX5FlatEnvCfg):
    """Configuration for Go2+ARX5 robot on flat terrain for play/inference."""
    
    def __post_init__(self) -> None:
        # post init of parent
        super().__post_init__()

        # make smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        
        # spawn robot with no randomization
        self.observations.policy.enable_corruption = False
        
        # disable randomization for play
        self.events.push_robot = None
        self.events.add_base_mass = None
        self.events.reset_robot_joints.params["position_range"] = (1.0, 1.0)
        self.events.reset_base.params["pose_range"]["x"] = (0.0, 0.0)
        self.events.reset_base.params["pose_range"]["y"] = (0.0, 0.0)
        self.events.base_external_force_torque.params["force_range"] = (0.0, 0.0)
        self.events.base_external_force_torque.params["torque_range"] = (0.0, 0.0)
        
        # Command ranges for play mode
        self.commands.base_velocity.ranges.lin_vel_x = (0.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-0.5, 0.5)
       
        self.commands.ee_pose.resampling_time_range = (4.0, 4.0)
        self.commands.ee_pose.ranges.pos_x = (0.45, 0.6)
        self.commands.ee_pose.ranges.pos_y = (-0.25, 0.25)
        self.commands.ee_pose.ranges.pos_z = (0.2, 0.5)
