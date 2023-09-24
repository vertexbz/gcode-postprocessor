# G-Code Postprocessor
Modular G-Code postprocessor for Prusa/SuperSlicer

## Installation
Clone this repository `git clone ...`

Provide path to `./run.sh` file of the cloned repository in `Print Settings > Output options > Post-processing scripts` of your slicer

## Configuration

### Log level
Log level / verbosity can be used by providing `-v` (or `--verbose`) CLI flag, multiple use increases verbosity

#### Levels
- Default: Error
- `v`: Info
- `vv`: Info, long format
- `vvv`: Debug
- `vvvv`: Debug, long format

### Config files
Default configuration is available in and loaded from `./config.default.yaml`\
User defaults can be provided via `./config.yaml` (or `./config.yml`) *this file is not part of this repository, default one can be used as template*\
Defaults are overriden by file provided via `-c` (or `--config`) CLI parameter


### Dry run
Dry run mode fully processes the input but doesn't save the output to file 

<table><tr>
<th>CLI</th><th>YAML</th>
</tr><tr>
<td valign="top">

`-d`\
`--dry`\
`--dry-run`
</td>
<td valign="top">

```yaml
dry_run: True
```
```yaml
dry-run: False
```
```yaml
dryRun: true
```
```yaml
dryrun: false
```
</td>
</tr></table>

### Macros

Features look for popular custom macros which names may vary \
Default configuration file contains full list of used macros

<table><tr>
<th>CLI</th><th>YAML</th>
</tr><tr>
<td valign="top">

`-m print_start=HELLO_THERE`\
`--macro print_end=BYE_BYE`
</td>
<td valign="top">

```yaml
macro:
  print_start: MY_CUSTOM_START_PRINT
  print_end: MY_CUSTOM_END_PRINT
```
</td>
</tr></table>


### Features
To have actual benefit from using postprocessor, desired features have to be enabled, via configuration file or with CLI flag

> - Features can be specified multiple times, with same or different configurations
> - Features are applied in the order provided, first config files, then cli
> - Configuration file features configuration overrides previous ones, CLI specified features are appended

<table><tr>
<th>CLI</th>
<td valign="top">

`-f start-xy -f pa-extruder-fixer`\
`--feature start-xy --feature feature-with-config=option1=value,other_option={options_option=1}`
</td>
</tr><tr>
<th>YAML</th>
<td valign="top">

```yaml
feature:
  - pa-extruder-fixer
  - start-xy
  - feature-with-config:
      option1: value
      other_option: 
        options_option: 1
```

to clear all prior features
```yaml
feature: []
```
</td>
</tr></table>


## Built-in features

### [`start-xy`](features%2Fstart_xy.py)
Detects first coordinate in g-code and sets X and Y coordinates to START_X and START_Y params of print start macro respectively

### [`no-final-unload`](features%2Fno_final_unload.py)
Removes final filament unload procedure for multi-material prints

### [`pa-extruder-fixer`](features%2Fpa_extruder_fixer.py)
Fixes `SET_PRESSURE_ADVANCE` gcode for clipper and multi-material prints (removes `EXTRUDER` parameter)

### [`no-morning-jumps`](features%2Fno_morning_jumps.py)
Removes `Z` axis movements prior to moving to initial `XY` position
