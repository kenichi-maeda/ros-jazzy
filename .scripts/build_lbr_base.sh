#!/usr/bin/env bash
set -euo pipefail

recipes=(
  ros-jazzy-kinematics-interface
  ros-jazzy-kinematics-interface-kdl
  ros-jazzy-iiwa7-moveit-config
  ros-jazzy-iiwa14-moveit-config
  ros-jazzy-med7-moveit-config
  ros-jazzy-med14-moveit-config
  ros-jazzy-lbr-moveit
  ros-jazzy-lbr-moveit-cpp
)

for recipe in "${recipes[@]}"; do
  rattler-build build \
    --recipe "./recipes/${recipe}/recipe.yaml" \
    -m ./conda_build_config_base.yaml \
    -c robostack-jazzy \
    -c https://repo.prefix.dev/conda-forge \
    --skip-existing
done
