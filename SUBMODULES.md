# Git Submodules Guide

This repository contains Git submodules that need to be properly initialized and updated when cloning the repository.

## Current Submodules

- `hailo_apps/hailo_app_python/apps/gstreamer-ardupilot` - GStreamer ArduPilot integration

## Cloning the Repository with Submodules

### Method 1: Clone with Submodules (Recommended)

When cloning the repository for the first time, use the `--recursive` flag to automatically initialize and update all submodules:

```bash
git clone --recursive git@github.com:UkrDroneAI/hailo-apps-infra.git
```

### Method 2: Clone First, Then Initialize Submodules

If you've already cloned the repository without submodules:

```bash
# Clone the repository
git clone git@github.com:UkrDroneAI/hailo-apps-infra.git
cd hailo-apps-infra

# Initialize and update submodules
git submodule init
git submodule update
```

Or use the shorthand:
```bash
git submodule update --init --recursive
```
