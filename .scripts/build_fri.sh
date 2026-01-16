#!/usr/bin/env bash
set -euo pipefail

recipes=(
  ros-jazzy-fri-client-sdk
  ros-jazzy-lbr-description
  ros-jazzy-lbr-fri-idl
  ros-jazzy-lbr-fri-ros2
  ros-jazzy-lbr-ros2-control
  ros-jazzy-lbr-fri-ros2-stack
  ros-jazzy-lbr-demos-cpp
  ros-jazzy-lbr-demos-advanced-cpp
  ros-jazzy-lbr-demos-advanced-py
  ros-jazzy-lbr-demos-py
  ros-jazzy-lbr-bringup
)

for recipe in "${recipes[@]}"; do
  rattler-build build \
    --recipe "./recipes/${recipe}/recipe.yaml" \
    -m ./conda_build_config.yaml \
    -c robostack-jazzy \
    -c https://repo.prefix.dev/conda-forge \
    --skip-existing
done
