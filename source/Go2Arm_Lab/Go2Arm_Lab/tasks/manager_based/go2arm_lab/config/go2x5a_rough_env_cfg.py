"""Configuration for Go2 + X5A on rough terrain."""

from isaaclab.utils import configclass

import Go2Arm_Lab.tasks.manager_based.go2arm_lab.mdp as mdp

from Go2Arm_Lab.tasks.manager_based.go2arm_lab.go2x5a_base_env_cfg import Go2X5ABaseEnvCfg, Go2X5ABaseEnvCfg_PLAY


@configclass
class Go2X5ARoughEnvCfg(Go2X5ABaseEnvCfg):
    """Configuration for Go2 + X5A on rough terrain."""

    def __post_init__(self):
        super().__post_init__()
        # Rough terrain
        self.scene.terrain.terrain_type = "generator"
        self.scene.terrain.terrain_generator = mdp.ROUGH_TERRAINS_CFG


@configclass
class Go2X5ARoughEnvCfg_PLAY(Go2X5ABaseEnvCfg_PLAY):
    """Configuration for Go2 + X5A on rough terrain (play mode)."""

    def __post_init__(self):
        super().__post_init__()
        # Rough terrain
        self.scene.terrain.terrain_type = "generator"
        self.scene.terrain.terrain_generator = mdp.ROUGH_TERRAINS_CFG
