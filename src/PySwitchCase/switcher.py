import re
from abc import ABC
from typing import Callable, Dict, Tuple




__all__ = ['SwitchCase', 'CallBackException', 'ActiveSessionError', 'InvalidRegexObject', 'InactiveSessionError']

class BreakCase(Exception): pass
class ActiveSessionError(Exception): pass
class InactiveSessionError(Exception): pass
class InvalidRegexObject(Exception): pass
class CallBackException(Exception): pass





def _to_type(obj: any): return type(obj) if obj.__class__ != type.__class__ else obj
def _convert_to_types(value_to_check: any) -> tuple or type:
    if isinstance(value_to_check, (list, tuple)):
        return tuple(map(BaseSwitchCase._to_type, value_to_check))

    elif value_to_check.__class__ != type.__class__:
        return type(value_to_check)



class CallbackhHandler(object):
    def __init__(self, func: Callable[[Tuple, Dict], bool], *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs) -> bool:
        args = self._args or args
        kwargs = self._kwargs or kwargs
        return self._func(*args, **kwargs)



class BaseSwitchCase(object, ABC):
    result = None
    _variable: any
    _active: bool = False
    no_match_handler: CallbackhHandler or Exception = None
    def __init__(self, variable: __eq__):
        """
        :param variable: the instance to check against.
        :param no_match_handler_args (args): no_match_handler's args
        :param no_match_handler_kwargs (kwargs): no_match_handler's kwargs
        """
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not a comparable type. {type(variable)}')

        self._variable = variable

    def _get_config(self) -> dict:
        return {
                'variable':                 repr(self._variable),
                'no_match_callback':        repr(self.no_match_handler),
                }
    def __enter__(self):
        self._active = True
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        if isinstance(exc_val, BreakCase): return True
        if self.no_match_handler is None: return
        if callable(self.no_match_handler): return self.no_match_handler()
        if issubclass(self.no_match_handler, Exception): raise self.no_match_handler() from exc_val
    def _exit(self): raise BreakCase()

    def __setattr__(self, key, value):
        if key not in ['result', '_active'] and self._active: self._raise_active(key, value)
        super().__setattr__(key, value)

    def _raise_inactive(self):
        raise InactiveSessionError(""" Context Manager Must be Used

        For example:

        # value_to_check = one of [ variable OR instance OR type OR tuple of types ]
        with SwitchCase(value_to_check) as sc:
            sc(value_to_search_for)
            ...
        """)
    def _raise_active(self, key, value):
        raise ActiveSessionError(f"""Attributes cannot be changed while context manager is active. 
    key: {key} 
    value: {value} """)

    def _check(self, value_to_check: any, *args, **kwargs) -> bool: raise NotImplementedError()
    def __call__(self, value_to_check: any, *args, **kwargs) -> bool: raise NotImplementedError()



class RegexSwitchCase(BaseSwitchCase):
    """
        Works on any class or variable type that contains a definition for __eq__.
        the nested BreakCase exception is the only exception suppressed. All others are passed on.

        ------------- Usage Examples -------------

            # example 1
            test = 10
            with SwitchCase(test) as sc:
                sc(2, on_true=print, on_true_args=('test 1',) )
                print('sub 1')
                sc(10, on_true=print, on_true_args=('test 2',) )  # will break here due to match found.
                print('sub 2')
                sc(12, on_true=print, on_true_args=('test 3',) )

            # example 2
            test = '10'
            with SwitchCase(test, catch_value_to_check=True) as sc:
                on_true = lambda x: print(f'testing... {x}')

                sc(2, on_true=on_true)
                print('sub 1')
                sc('1', on_true=on_true)
                print('sub 2')
                sc('10', on_true=on_true)  # will break here due to match found.

            # example 3
            def run_test(*args, **kwargs):
                return {
                        'args': args,
                        'kwargs': kwargs
                        }
            test = '10'
            switcher = SwitchCase(test, catch_value_to_check=True)
            with switcher as sc:
                on_true = lambda x: run_test(x, test=True)

                sc(2, on_true=on_true)
                print('sub 1')
                sc('1', on_true=on_true)  # will break here.
                print('sub 2')
                sc('10', on_true=on_true)
            print(switcher.result)
    """
    def __init__(self, regex: re.Pattern or re.compile):
        """
        :param regex: the instance to check against.
        """
        self._variable = regex

    def __call__(self, value_to_check: any) -> bool:
        if not self._active: self._raise_inactive()
        return self.__regex__(value_to_check)
    def __regex__(self, value_to_check: str) -> bool:  # TODO: implement regex parsing for the value_to_check
        if not isinstance(value_to_check, str): return False

        return self._variable(value_to_check) is not None



class SwitchCase(BaseSwitchCase):
    """
        Works on any class or variable type that contains a definition for __eq__.
        the nested BreakCase exception is the only exception suppressed. All others are passed on.

        ------------- Usage Examples -------------

            # example 1
            test = 10
            with SwitchCase(test) as sc:
                sc(2, on_true=print, on_true_args=('test 1',) )
                print('sub 1')
                sc(10, on_true=print, on_true_args=('test 2',) )  # will break here due to match found.
                print('sub 2')
                sc(12, on_true=print, on_true_args=('test 3',) )

            # example 2
            test = '10'
            with SwitchCase(test, catch_value_to_check=True) as sc:
                on_true = lambda x: print(f'testing... {x}')

                sc(2, on_true=on_true)
                print('sub 1')
                sc('1', on_true=on_true)
                print('sub 2')
                sc('10', on_true=on_true)  # will break here due to match found.

            # example 3
            def run_test(*args, **kwargs):
                return {
                        'args': args,
                        'kwargs': kwargs
                        }
            test = '10'
            switcher = SwitchCase(test, catch_value_to_check=True)
            with switcher as sc:
                on_true = lambda x: run_test(x, test=True)

                sc(2, on_true=on_true)
                print('sub 1')
                sc('1', on_true=on_true)  # will break here.
                print('sub 2')
                sc('10', on_true=on_true)
            print(switcher.result)
    """
    def __init__(self, variable: __eq__):
        """
        :param variable: the instance to check against.
        """
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not a comparable type. {type(variable)}')

        self._variable = variable

    def __call__(self, value_to_check: any) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(value_to_check): self._exit()
        return False

    def _check(self, value_to_check): return self._variable == value_to_check



class CallbackSwitchCase(BaseSwitchCase):
    """
        Works on any class or variable type that contains a definition for __eq__.
        the nested BreakCase exception is the only exception suppressed. All others are passed on.

        ------------- Usage Examples -------------

            # example 1
            test = 10
            with SwitchCase(test) as sc:
                sc(2, on_true=print, on_true_args=('test 1',) )
                print('sub 1')
                sc(10, on_true=print, on_true_args=('test 2',) )  # will break here due to match found.
                print('sub 2')
                sc(12, on_true=print, on_true_args=('test 3',) )

            # example 2
            test = '10'
            with SwitchCase(test, catch_value_to_check=True) as sc:
                on_true = lambda x: print(f'testing... {x}')

                sc(2, on_true=on_true)
                print('sub 1')
                sc('1', on_true=on_true)
                print('sub 2')
                sc('10', on_true=on_true)  # will break here due to match found.

            # example 3
            def run_test(*args, **kwargs):
                return {
                        'args': args,
                        'kwargs': kwargs
                        }
            test = '10'
            switcher = SwitchCase(test, catch_value_to_check=True)
            with switcher as sc:
                on_true = lambda x: run_test(x, test=True)

                sc(2, on_true=on_true)
                print('sub 1')
                sc('1', on_true=on_true)  # will break here.
                print('sub 2')
                sc('10', on_true=on_true)
            print(switcher.result)
    """
    def __init__(self, variable: __eq__):
        """
        :param variable: the instance to check against.
        """
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not a comparable type. {type(variable)}')

        self._variable = variable

    def __call__(self, value_to_check: any, callback: CallbackhHandler = None) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(value_to_check):
            callback()
            self._exit()

        return False

    def _check(self, value_to_check): return self._variable == value_to_check



class InstanceSwitchCase(BaseSwitchCase):
    """
     variable: the instance to check against.
     regex: the instance to check against.
     regex_pattern: the instance to check against.
     Check_Address: Checks the addresses between variable and the value_to_check, using "is".
     catch_value_to_check: If match is True, added the value_to_check to on_true_args at the start.
     no_match_callback: Optional Method that is called if no match is found or Exception that is raised if no match is found.
     no_match_handler_args (args): no_match_handler's args
     no_match_handler_kwargs (kwargs): no_match_handler's kwargs
    """
    def __init__(self, variable: __eq__):
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not comparable type. {type(variable)}')

        self._variable = variable
    def __call__(self, *types: type) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(*types): self._exit()
        return False

    def _check(self, *types): return isinstance(self._variable, types)



class TypeSwitchCase(BaseSwitchCase):
    """
     variable: the instance to check against.
     regex: the instance to check against.
     regex_pattern: the instance to check against.
     Check_Address: Checks the addresses between variable and the value_to_check, using "is".
     catch_value_to_check: If match is True, added the value_to_check to on_true_args at the start.
     no_match_callback: Optional Method that is called if no match is found or Exception that is raised if no match is found.
     no_match_handler_args (args): no_match_handler's args
     no_match_handler_kwargs (kwargs): no_match_handler's kwargs
    """
    def __init__(self, variable: type):
        if not hasattr(variable, '__eq__'):
            raise ValueError(f'variable is not comparable type. {type(variable)}')

        self._variable = variable
    def __call__(self, *types: type) -> bool:
        if not self._active: self._raise_inactive()
        if self._check(*types): self._exit()
        return False

    def _check(self, *types): return issubclass(self._variable, types)
