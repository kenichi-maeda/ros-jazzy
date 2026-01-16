#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

FRI_SHAS = {
    "1_11": "2a48b0ce3eb2cff817d5fbbca32a0ff15c2c73a4",
    "1_14": "7b73b1a41357007f15b4ab0b4e2b401f3f944102",
    "1_15": "dc7d613d42571e458dd62ea814a0a47a209487d8",
    "1_16": "1995140f591e0e8be6010c28b896f1c72ac9e18c",
    "1_17": "1f80137c0771fde6a6c4cdff4daa16aa5dc07eed",
    "2_5": "05b4284d077d3886c52cfd1a6872e1c90ebb5989",
    "2_7": "49979142829dad5e2dcfb87a72aa21526f41abf8",
}

PIN_PKGS = (
    "ros-jazzy-fri-client-sdk",
    "ros-jazzy-lbr-fri-idl",
    "ros-jazzy-lbr-fri-ros2",
)
FRI_VARIANT_EXPR = "${{ fri_client_version }}"

TARGET_RECIPES = [
    "recipes/ros-jazzy-fri-client-sdk/recipe.yaml",
    "recipes/ros-jazzy-lbr-description/recipe.yaml",
    "recipes/ros-jazzy-lbr-fri-idl/recipe.yaml",
    "recipes/ros-jazzy-lbr-fri-ros2/recipe.yaml",
    "recipes/ros-jazzy-lbr-ros2-control/recipe.yaml",
    "recipes/ros-jazzy-lbr-demos-cpp/recipe.yaml",
    "recipes/ros-jazzy-lbr-demos-advanced-cpp/recipe.yaml",
    "recipes/ros-jazzy-lbr-demos-advanced-py/recipe.yaml",
    "recipes/ros-jazzy-lbr-demos-py/recipe.yaml",
    "recipes/ros-jazzy-lbr-fri-ros2-stack/recipe.yaml",
    "recipes/ros-jazzy-lbr-bringup/recipe.yaml",
]


def ensure_build_string(text: str) -> str:
    lines = [
        line
        for line in text.splitlines()
        if line.strip() != f"string: fri{FRI_VARIANT_EXPR}"
    ]
    text = "\n".join(lines) + "\n"
    if re.search(r"^build:\n  string: fri\\$\\{\\{ fri_client_version \\}\\}", text, re.M):
        return text
    return re.sub(
        r"^build:\n",
        "build:\n  string: fri${{ fri_client_version }}\n",
        text,
        count=1,
        flags=re.M,
    )


def pin_dependencies(text: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        for pkg in PIN_PKGS:
            if f"- {pkg} * *fri{FRI_VARIANT_EXPR}*" in line:
                continue
            if re.search(rf"^\\s*-\\s+{re.escape(pkg)}\\s*$", line):
                indent = re.match(r"^(\\s*)-", line).group(1)
                lines[idx] = f"{indent}- {pkg} * *fri{FRI_VARIANT_EXPR}*"
    return "\n".join(lines) + "\n"


def update_fri_client_sdk(text: str) -> str:
    order = ["1_11", "1_14", "1_15", "1_16", "1_17", "2_5", "2_7"]
    last_key = order[-1]
    expr = ""
    for key in order[:-1]:
        expr += f"'{FRI_SHAS[key]}' if fri_client_version == '{key}' else "
    expr += f"'{FRI_SHAS[last_key]}'"
    rev_expr = "${{ " + expr + " }}"
    text = re.sub(
        r"^  rev: .*",
        f"  rev: {rev_expr}",
        text,
        count=1,
        flags=re.M,
    )
    return text


def process_recipe(path: Path) -> None:
    text = path.read_text()
    text = ensure_build_string(text)
    text = pin_dependencies(text)
    if path.name == "recipe.yaml" and path.parent.name == "ros-jazzy-fri-client-sdk":
        text = update_fri_client_sdk(text)
    path.write_text(text)


def main() -> None:
    for rel in TARGET_RECIPES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing recipe: {path}")
        process_recipe(path)


if __name__ == "__main__":
    main()
