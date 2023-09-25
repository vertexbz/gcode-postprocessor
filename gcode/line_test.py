from __future__ import annotations
from gcode.line import Line

def c(s: str):
    return s.replace('\n', '\\n')

def test_change():
    for l in ('', '   ', '\n', '    \n'):
        line = Line(l)
        line.raw = '_PRINT_BEFORE_LAYER_CHANGE LAYER=0 Z=0.2375;close   comment   \n'
        assert line.command == '_PRINT_BEFORE_LAYER_CHANGE'
        assert line.comment == 'close   comment'
        assert len(line.params) == 2
        assert line.params.get('Z') == 0.2375
        assert line.params.get('LAYER') == 0

        line = Line(l)
        line.command = 'g69'
        assert line.command == 'G69'
        assert line.raw == 'G69\n', f"'{c(line.raw)}' == 'G69\\n'"

    # change command
    line = Line(';HEIGHT:0.2375\n')
    line.command = 'g69'
    assert line.command == 'G69'
    assert line.raw == 'G69 ;HEIGHT:0.2375\n', f"'{c(line.raw)}' == 'G69 ;HEIGHT:0.2375\\n'"
    # and comment
    line.comment = 'TEST Comment'
    assert line.comment == 'TEST Comment'
    assert line.raw == 'G69 ; TEST Comment\n', f"'{c(line.raw)}' == 'G69 ; TEST Comment\\n'"

    # change just comment
    line = Line(';HEIGHT:0.2375\n')
    line.comment = 'TEST Comment'
    assert line.raw == '; TEST Comment\n', f"'{c(line.raw)}' == '; TEST Comment\\n'"

    line = Line('M117\n')
    line.comment = 'TEST Comment'
    assert line.raw == 'M117 ; TEST Comment\n', f"'{c(line.raw)}' == 'M117 ; TEST Comment\\n'"

    line = Line('_PRINT_BEFORE_LAYER_CHANGE LAYER=0 Z=0.2375; close   comment   \n')
    line.command = None
    assert line.raw == '; close   comment   \n', f"'{c(line.raw)}' == '; close   comment   \\n'"

    # changing params
    line = Line('SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder2\n')
    assert 'EXTRUDER' in line.params
    assert line.params.get('EXTRUDER') == 'extruder2'
    del line.params['EXTRUDER']
    assert 'EXTRUDER' not in line.params
    assert line.raw == 'SET_PRESSURE_ADVANCE ADVANCE=0\n', f"'{c(line.raw)}' == 'SET_PRESSURE_ADVANCE ADVANCE=0\\n'"

    line = Line('SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder2\n')
    line.params['EXTRUDER'] = 'extruder'
    assert line.raw == 'SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder\n', f"'{c(line.raw)}' == 'SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder\\n'"
    assert line.params['EXTRUDER'] == 'extruder'

    line = Line('SET_PRESSURE_ADVANCE ADVANCE=0\n')
    line.params['EXTRUDER'] = 'extruder'
    assert line.params.EXTRUDER == 'extruder'
    assert line.params.ADVANCE == 0, f"'{line.params.ADVANCE}' == 0"
    assert line.raw == 'SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder\n', f"'{c(line.raw)}' == 'SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder\\n'"
    assert line.params['EXTRUDER'] == 'extruder'

    line = Line('SET_PRESSURE_ADVANCE ADVANCE=0;test comment\n')
    line.params['EXTRUDER'] = 'extruder'
    assert line.raw == 'SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder;test comment\n', f"'{c(line.raw)}' == 'SET_PRESSURE_ADVANCE ADVANCE=0 EXTRUDER=extruder;test comment\\n'"
    assert line.params['EXTRUDER'] == 'extruder'

    line = Line('g1.0000 X101.707 Y56.457\n')
    line.params['X'] = 5.76
    assert line.raw == 'g1.0000 X5.76 Y56.457\n', f"'{c(line.raw)}' == 'g1.0000 X5.76 Y56.457\\n'"

    line = Line('g1.0000 X.707 Y56.457\n')
    assert line.params.X == 0.707, f"'{line.params.X}' == 0.707"
    del line.params.X
    assert line.raw == 'g1.0000 Y56.457\n', f"'{c(line.raw)}' == 'g1.0000 Y56.457\\n'"

    line = Line('g1.0000 X101.707 Y56.457\n')
    line.params['Z'] = 5.76
    assert line.raw == 'g1.0000 X101.707 Y56.457 Z5.76\n', f"'{c(line.raw)}' == 'g1.0000 X101.707 Y56.457 Z5.76\\n'"


def test_parser():
    for l in ('', '   ', '\n', '    \n'):
        line = Line(l)
        assert line.command is None
        assert line.comment is None
        assert len(line.params) == 0
        assert len(line.params.keys()) == len(line.params)
        assert len(line.params.items()) == len(line.params)
        assert len(line.params.values()) == len(line.params)

    line = Line(';HEIGHT:0.2375\n')
    assert line.command is None
    assert line.comment == 'HEIGHT:0.2375'
    assert len(line.params) == 0
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)

    line = Line(';TYPE:Skirt\n')
    assert line.command is None
    assert line.comment == 'TYPE:Skirt'
    assert len(line.params) == 0
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)

    line = Line('; first layer extrusion width = 0.47mm\n')
    assert line.command is None
    assert line.comment == 'first layer extrusion width = 0.47mm'
    assert len(line.params) == 0
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)

    line = Line('SET_PRESSURE_ADVANCE ADVANCE=0\n')
    assert line.command == 'SET_PRESSURE_ADVANCE'
    assert line.comment is None
    assert len(line.params) == 1, f'{len(line.params)} == 1'
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('ADVANCE') == 0

    line = Line('_PRINT_BEFORE_LAYER_CHANGE LAYER=0 Z=0.2375;close   comment   \n')
    assert line.command == '_PRINT_BEFORE_LAYER_CHANGE'
    assert line.comment == 'close   comment'
    assert len(line.params) == 2, f'{len(line.params)} == 1, {line.params}'
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('Z') == 0.2375
    assert line.params.get('LAYER') == 0

    line = Line('_print_before_layer_change layer=0 z=0.2375;close   comment   \n')
    assert line.command == '_PRINT_BEFORE_LAYER_CHANGE'
    assert line.comment == 'close   comment'
    assert len(line.params) == 2, f'{len(line.params)} == 1, {line.params}'
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('Z') == 0.2375
    assert line.params.get('LAYER') == 0

    line = Line('_PRINT_LAYER_CHANGE LAYER=0 ; a comment\n')
    assert line.command == '_PRINT_LAYER_CHANGE'
    assert line.comment == 'a comment'
    assert len(line.params) == 1, f'{len(line.params)} == 1'
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('LAYER') == 0

    line = Line('G92 E0; a comment\n')
    assert line.command == 'G92'
    assert line.comment == 'a comment'
    assert len(line.params) == 1, f'{len(line.params)} == 1'
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('E') == 0

    line = Line('G1 E-0.3 F3000\n')
    assert line.command == 'G1'
    assert line.comment is None
    assert len(line.params) == 2
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('E') == -0.3
    assert line.params.get('F') == 3000

    line = Line('M117\n')
    assert line.command == 'M117'
    assert line.comment is None
    assert len(line.params) == 0
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)

    line = Line('M204 S1000\n')
    assert line.command == 'M204'
    assert line.comment is None
    assert len(line.params) == 1
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('S') == 1000

    line = Line('M204.7654 S1000\n')
    assert line.command == 'M204.7654'
    assert line.comment is None
    assert len(line.params) == 1
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('S') == 1000

    line = Line('G1 X101.707 Y56.457\n')
    assert line.command == 'G1'
    assert line.comment is None
    assert len(line.params) == 2
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('X') == 101.707
    assert line.params.get('Y') == 56.457

    line = Line('g1.0000 X101.707 Y56.457\n')
    assert line.command == 'G1.0000'
    assert line.comment is None
    assert len(line.params) == 2
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('X') == 101.707
    assert line.params.get('Y') == 56.457

    line = Line('g1 x101.307 y57.951 e0.02652\n')
    assert line.command == 'G1'
    assert line.comment is None
    assert len(line.params) == 3
    assert len(line.params.keys()) == len(line.params)
    assert len(line.params.items()) == len(line.params)
    assert len(line.params.values()) == len(line.params)
    assert line.params.get('X') == 101.307
    assert line.params.get('Y') == 57.951
    assert line.params.get('E') == 0.02652


if __name__ == "__main__":
    test_parser()
    test_change()
