"""Configuration for Go2 + X5A on flat terrain."""

from isaaclab.utils import configclass

import Go2Arm_Lab.tasks.manager_based.go2arm_lab.mdp as mdp

from Go2Arm_Lab.tasks.manager_based.go2arm_lab.go2x5a_base_env_cfg import Go2X5ABaseEnvCfg, Go2X5ABaseEnvCfg_PLAY


@configclass
class Go2X5AFlatEnvCfg(Go2X5ABaseEnvCfg):
    """Configuration for Go2 + X5A on flat terrain."""

    def __post_init__(self):
        super().__post_init__()
        # Flat terrain curriculum
        self.scene.terrain.terrain_type = "generator"
        self.scene.terrain.terrain_generator = mdp.FLAT_TERRAIN_CFG
        self.curriculum.terrain_levels = None


@configclass
class Go2X5AFlatEnvCfg_PLAY(Go2X5ABaseEnvCfg_PLAY):
    """Configuration for Go2 + X5A on flat terrain (play mode)."""

    def __post_init__(self):
        super().__post_init__()
        # Flat terrain
        self.scene.terrain.terrain_type = "generator"
        self.scene.terrain.terrain_generator = mdp.FLAT_TERRAIN_CFG
