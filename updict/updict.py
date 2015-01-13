# -*- coding: utf-8 -*-

import copy

from .exceptions import UpdictException

COMMAND_PUSH = '$push'
COMMAND_UNSHIFT = '$unshift'
# COMMAND_SPLICE = '$splice'
COMMAND_SET = '$set'
COMMAND_MERGE = '$merge'
# COMMAND_APPLY = '$apply'

ALL_COMMANDS = [
    COMMAND_PUSH,
    COMMAND_UNSHIFT,
    # COMMAND_SPLICE,
    COMMAND_SET,
    COMMAND_MERGE,
    # COMMAND_APPLY,
]

ALL_COMMANDS_DICT = dict([(x, True) for x in ALL_COMMANDS])


# def splice(a, b, c, d=None):
#     if isinstance(b, (list, tuple)):
#         return a[:b[0]] + [c] + a[b[1]:]
#     return a[:b] + [d] + a[c:]


def invariantArrayCase(value, spec, command):
    if not isinstance(value, (list, tuple)):
        raise UpdictException(
            'updict(): expected target of {} to be an array; got {}.'.format(
                command,
                value
            )
        )
    spec_value = spec[command]
    if not isinstance(spec_value, list):
        raise UpdictException(
            'updict(): expected spec of {} to be an array; got {}. Did you forget to wrap your parameter in an array?'.format(
                command,
                value
            )
        )



def updict(value, spec):
    if not isinstance(spec, dict):
        raise UpdictException(
            'updict(): You provided a key path to updict() that did not contain one of {}. Did you forget to include {{}: ...}?'.format(
                ', '.join(ALL_COMMANDS),
                COMMAND_SET,
            )
        )

    if COMMAND_SET in spec:
        if len(spec.keys()) != 1:
            raise UpdictException(
                'Cannot have more than one key in an object with {}'.format(
                    COMMAND_SET
                )
            )
        return spec[COMMAND_SET]

    next_value = copy.copy(value)

    if COMMAND_MERGE in spec:
        merge_obj = spec[COMMAND_MERGE]
        if not (merge_obj and isinstance(merge_obj, dict)):
            raise UpdictException(
                'updict(): {} expects a spec of type \'dict\'; got {}'.format(
                    COMMAND_MERGE,
                    merge_obj
                )
            )
        if not (next_value and isinstance(next_value, dict)):
            raise UpdictException(
                'updict(): {} expects a target of type \'dict\'; got {}'.format(
                    COMMAND_MERGE,
                    next_value
                )
            )
        next_value.update(spec[COMMAND_MERGE])

    if COMMAND_PUSH in spec:
        invariantArrayCase(value, spec, COMMAND_PUSH)
        next_value.extend(spec[COMMAND_PUSH])

    if COMMAND_UNSHIFT in spec:
        invariantArrayCase(value, spec, COMMAND_UNSHIFT)
        next_value = spec[COMMAND_UNSHIFT] + next_value

    # if COMMAND_SPLICE in spec:
    #     if not isinstance(value, list):
    #         raise UpdictException(
    #             'Expected {} target to be a list; got {}'.format(
    #                 COMMAND_SPLICE,
    #                 value
    #             )
    #         )
    #     if not isinstance(spec[COMMAND_SPLICE], list):
    #         raise UpdictException(
    #             'updict(): expected spec of {} to be a list of lists; got {}. Did you forget to wrap your parameters in an list?'.format(
    #                 COMMAND_SPLICE,
    #                 spec[COMMAND_SPLICE]
    #             )
    #         )
    #     for args in spec[COMMAND_SPLICE]:
    #         if not isinstance(args, list):
    #             raise UpdictException(
    #                 'updict(): expected spec of {} to be a list of lists; got {}. Did you forget to wrap your parameters in an list?'.format(
    #                     COMMAND_SPLICE,
    #                     spec[COMMAND_SPLICE]
    #                 )
    #             )
    #         print args
    #         next_value = splice(next_value, *args)

    for k in spec:
        if not (k in ALL_COMMANDS and ALL_COMMANDS_DICT[k]):
            next_value[k] = updict(value[k], spec[k])

    return next_value