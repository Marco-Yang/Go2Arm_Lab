#!/bin/bash

# 优化的测试脚本
# 使用更少的环境数量和适当的可视化设置

echo "运行策略测试..."
echo "使用权重: logs/rsl_rl/unitree_Go2arm_flat/2025-12-04_20-35-45/model_14999.pt"
echo ""

# 方案 1: 单环境 + GUI + 可视化箭头
echo "方案 1: 单环境 GUI 模式（可以看到箭头）"
python scripts/rsl_rl/play.py \
    --task Isaac-Go2Arm-Flat-Play \
    --num_envs 1 \
    --load_run 2025-12-04_20-35-45

# 如果上面太慢，可以尝试：
# 方案 2: headless 模式（性能最好但看不到箭头）
# echo ""
# echo "方案 2: Headless 模式（性能最好）"
# python scripts/rsl_rl/play.py \
#     --task Isaac-Go2Arm-Flat-Play \
#     --num_envs 1 \
#     --load_run 2025-12-04_20-35-45 \
#     --headless
