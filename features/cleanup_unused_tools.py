from __future__ import annotations
import io
import csv
from typing import TYPE_CHECKING, Optional
from base import Processor, ProcessorsList, CollectorsSet
from collectors.print_sections import CollectSections, PrintSection, PrintInfo
import logger

if TYPE_CHECKING:
    from base import Context
    from gcode import Line

logger = logger.named_logger(__name__)


class ProcessCleanupUnusedTools(Processor):
    finished = False
    header = False
    slicer_config = False

    def section_predicate(self, section: PrintSection):
        return section.tool == 1

    def process(self, context: Context, line: Line):
        if line.command == self.config.macro.print_start:
            line.params.TOOLS_USED = ','.join(map(lambda t: f'T{t}', context[PrintInfo].used_tools))
            logger.info(f'Added used tools list to print start params {line.params.TOOLS_USED} [{line.no}]: {line}')

        if not line.is_comment:
            return

        if line.comment in ('HEADER_BLOCK_END',):
            self.header = False
            return

        if line.comment in ('HEADER_BLOCK_START',):
            self.header = True
            return

        if line.comment in ('CONFIG_BLOCK_END',):
            self.slicer_config = False
            self.finished = True
            return

        if line.comment in ('CONFIG_BLOCK_START',):
            self.slicer_config = True
            return

        if not self.header and not self.slicer_config:
            return

        sep = ': ' if self.header else ' = '
        setting = line.comment.split(sep, 1)

        if len(setting) != 2:
            return

        key = setting[0]
        value = setting[1]

        if key in ProcessCleanupUnusedTools.COMMA_LIST_PROPS:
            separated = value.strip().split(',')
            filtered = map(lambda e: e[1], filter(lambda e: e[0] in context[PrintInfo].used_tools, enumerate(separated)))
            line.comment = key + sep + ','.join(filtered)
            logger.info(f'Cleaned-up unused tool configurations [{line.no}]: {line}')

        if key in ProcessCleanupUnusedTools.COMPLEX_LIST_PROPS:
            reader = csv.reader(io.StringIO(value), delimiter=';')
            row = next(reader)

            filtered = map(lambda e: e[1], filter(lambda e: e[0] in context[PrintInfo].used_tools, enumerate(row)))

            formatted_row = []
            for item in filtered:
                # Check if the item contains spaces or newlines
                if ' ' in item or '\n' in item or '\\n' in item:
                    # Double-quote the item and escape existing double quotes and newlines
                    item = '"' + item.replace("\"", "\\\"").replace("\\n", "\\\\n").replace("\n", "\\n") + '"'
                formatted_row.append(item)

            line.comment = key + sep + ';'.join(formatted_row)
            logger.info(f'Cleaned-up unused tool configurations [{line.no}]: {line}')


    COMMA_LIST_PROPS = (
        'filament_density', 'filament_diameter',  # header keys
        'activate_air_filtration', 'activate_chamber_temp_control', 'additional_cooling_fan_speed', 'chamber_temperature',
        'close_fan_the_first_x_layers', 'complete_print_exhaust_fan_speed', 'cool_plate_temp', 'cool_plate_temp_initial_layer',
        'during_print_exhaust_fan_speed', 'enable_overhang_bridge_fan', 'enable_pressure_advance', 'eng_plate_temp', 'eng_plate_temp_initial_layer',
        'fan_cooling_layer_time', 'fan_max_speed', 'fan_min_speed', 'filament_cooling_final_speed', 'filament_cooling_initial_speed',
        'filament_cooling_moves', 'filament_cost', 'filament_density', 'filament_diameter', 'filament_flow_ratio', 'filament_is_support',
        'filament_load_time', 'filament_loading_speed', 'filament_loading_speed_start', 'filament_max_volumetric_speed',
        'filament_minimal_purge_on_wipe_tower', 'filament_multitool_ramming', 'filament_multitool_ramming_flow', 'filament_multitool_ramming_volume',
        'filament_shrink', 'filament_soluble', 'filament_toolchange_delay', 'filament_unload_time', 'filament_unloading_speed',
        'filament_unloading_speed_start', 'flush_volumes_matrix', 'flush_volumes_vector', 'full_fan_speed_layer', 'hot_plate_temp',
        'hot_plate_temp_initial_layer', 'nozzle_temperature', 'nozzle_temperature_initial_layer', 'nozzle_temperature_range_high',
        'nozzle_temperature_range_low', 'overhang_fan_speed', 'overhang_fan_threshold', 'pressure_advance', 'reduce_fan_stop_start_freq',
        'required_nozzle_HRC', 'slow_down_for_layer_cooling', 'slow_down_layer_time', 'slow_down_min_speed', 'support_material_interface_fan_speed',
        'temperature_vitrification', 'textured_plate_temp', 'textured_plate_temp_initial_layer', 'wiping_volumes_extruders'
    )

    COMPLEX_LIST_PROPS = (
        'default_filament_colour',
        'filament_colour',
        'filament_end_gcode',
        'filament_ids',
        'filament_notes',
        'filament_ramming_parameters',
        'filament_settings_id',
        'filament_start_gcode',
        'filament_type',
        'filament_vendor',
    )


def load(collectors: CollectorsSet, processors: ProcessorsList, _: Optional[dict]) -> None:
    collectors.add(CollectSections)
    processors.append(ProcessCleanupUnusedTools)


__all__ = ['load']
