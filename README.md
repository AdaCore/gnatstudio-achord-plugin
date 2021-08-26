# ACHORD / GNAT Studio integration plug-in

This repository contains a plugin for [GNAT Studio](https://www.adacore.com/gnatpro/toolsuite/gnatstudio) allowing integration of the `ACHORD` environment.

## Installation

There are three ways to make the plug-in available to GNAT Studio - choose one:

 * Add the complete path to the directory `achord-integration` to your environment variable `GNATSTUDIO_CUSTOM_PATH`, or
 * Copy the directory `achord-integration` to the subdirectory `share/gnatstudio/plug-ins`in your GNAT Studio installation, or
 * Copy the directory `achord-integration` to the `plug-ins` directory of the `.gnatstudio` folder in your home directory (note that this method will make the plug-in available to you only).

## Usage

## Development and testing

## TO DO

 * make the connection system asynchronous, so delays in connection don't freeze the GNAT Studio UI
 * add a background connection monitor