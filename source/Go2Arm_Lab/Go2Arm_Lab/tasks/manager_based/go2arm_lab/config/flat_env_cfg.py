# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass


from Go2Arm_Lab.tasks.manager_based.go2arm_lab.go2arm_lab_env_cfg import LocomotionVelocityEnvCfg
from Go2Arm_Lab.assets.go2arm_articulation_cfg import GO2ARM_CFG


@configclass
class Go2ARMFlatEnvCfg(LocomotionVelocityEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        self.scene.robot = GO2ARM_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # event
        self.events.push_robot = None

        # flat terrain 
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None

        # velocity command - Accelerated curriculum learning (4000→1000, 4x faster)
        self.commands.base_velocity.curriculum_coeff = 1000
        # init
        self.commands.base_velocity.ranges_init.lin_vel_x  = (0.0, 0.0)
        self.commands.base_velocity.ranges_init.lin_vel_y  = (-0.0, 0.0)
        self.commands.base_velocity.ranges_init.ang_vel_z  = (-0.0, 0.0)
        # final
        self.commands.base_velocity.ranges_final.lin_vel_x = (0.0, 1.0)
        self.commands.base_velocity.ranges_final.lin_vel_y = (-0.5, 0.5)
        self.commands.base_velocity.ranges_final.ang_vel_z = (-0.5, 0.5)
  
        # position command - Accelerated curriculum learning (5000→1500, 3.3x faster)
        self.commands.ee_pose.curriculum_coeff = 1500
        # init
        self.commands.ee_pose.ranges_init.pos_x = (0.45, 0.5)
        self.commands.ee_pose.ranges_init.pos_y = (-0.05, 0.05)
        self.commands.ee_pose.ranges_init.pos_z = (0.45, 0.5)
        # final
        self.commands.ee_pose.ranges_final.pos_x = (0.4, 0.65)
        self.commands.ee_pose.ranges_final.pos_y = (-0.35, 0.35)
        self.commands.ee_pose.ranges_final.pos_z = (0.15, 0.6)

        # ================================================================================================================================
        # Reward weights - Balanced for mobile manipulation
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
        
        # Mobile manipulation specific rewards (NEW!)
        self.rewards.arm_self_collision.weight = -1.0          # Prevent arm hitting body
        self.rewards.base_motion_diversity.weight = 0.5         # Encourage moving
        self.rewards.stationary_base_penalty.weight = -0.3      # Discourage staying still


class Go2ARMFlatEnvCfg_PLAY(Go2ARMFlatEnvCfg):
    def __post_init__(self) -> None:
        # post init of parent
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing event
        self.events.base_external_force_torque = None
        self.events.push_robot = None
        # self.events.reset_base = None

        self.commands.ee_pose.is_Go2ARM = False
        self.commands.base_velocity.is_Go2ARM = False
        
        self.commands.ee_pose.is_Go2ARM_Play = True
        
        self.commands.base_velocity.resampling_time_range = (5.0,5.0)
        self.commands.base_velocity.rel_standing_envs = 0.1
        
        self.commands.base_velocity.ranges.lin_vel_x = (0.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-0.5, 0.5)
       
        self.commands.ee_pose.resampling_time_range = (4.0,4.0)
        self.commands.ee_pose.ranges.pos_x = (0.45, 0.6)
        self.commands.ee_pose.ranges.pos_y = (-0.25, 0.25)
        self.commands.ee_pose.ranges.pos_z = (0.2, 0.5)