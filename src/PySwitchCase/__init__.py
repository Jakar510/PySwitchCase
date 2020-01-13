
"""
I thought of a way to efficiently do a c++ style switch case in Python 3.6+.

I would like feedback, however, if there any ways to improve it. Please see the docstring for the SwitchCase class for usage examples. I do plan on making a package for it soon.
"""

class SwitchCase(object):
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
    class BreakCase(Exception): pass
    _variable_to_check: any
    result = None

    _check_address: bool = False
    _no_match_handler: callable
    _no_match_handler_args: tuple
    _no_match_handler_kwargs: dict
    def __init__(self, variable_to_check: any, *, check_address: bool = False, catch_value_to_check: bool = False, no_match_handler: callable or Exception = None, no_match_handler_args: tuple = (), **kwargs):
        """


        :param variable_to_check: the instance to check against.
        :param check_address: Checks the addresses between variable_to_check and the value_to_check, using "is".
        :param catch_value_to_check: If match is True, added the value_to_check to on_true_args at the start.
        :param no_match_handler: Optional Method that is called if no match is found or Exception that is raised if no match is found.
        :param no_match_handler_args: no_match_handler's args
        :param kwargs: no_match_handler's kwargs
        """
        if not hasattr(variable_to_check, '__eq__'): raise ValueError(f'variable_to_check is not comparable type. {type(variable_to_check)}')
        if no_match_handler is None and no_match_handler_args != () and kwargs != {}: raise ValueError('no_match_handler is None but its args and kwargs are passed in.')
        self._variable_to_check = variable_to_check
        self._check_address = check_address
        self._no_match_handler = no_match_handler
        self._catch_value_to_check = catch_value_to_check
        self._no_match_handler_args = no_match_handler_args
        self._no_match_handler_kwargs = kwargs

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, self.BreakCase): return True
        else:
            if self._no_match_handler is None: pass
            elif callable(self._no_match_handler): self._no_match_handler(*self._no_match_handler_args, **self._no_match_handler_kwargs)
            elif issubclass(self._no_match_handler, BaseException): raise self._no_match_handler(*self._no_match_handler_args, **self._no_match_handler_kwargs)
    def __exit(self):
        raise self.BreakCase()
    def __call__(self, value_to_check, *, on_true: callable = None, on_true_args: tuple = (), **kwargs) -> bool:
        """
            Exits the Context Manger if a match is found with self.__exit().

        :param value_to_check: the instance or value to check self._variable_to_check against.
        :param on_true: handler method to be called if match is True.
        :param on_true_args: on_true's args if match is True.
        :param kwargs: on_true's kwargs if match is True.
        :return: bool.
        """
        result = False
        if self._catch_value_to_check: on_true_args = (value_to_check, *on_true_args)
        print(on_true_args)
        if callable(on_true):
            if self._check_address and self._variable_to_check is value_to_check:
                self.result = on_true(*on_true_args, **kwargs)
                result = True

            elif self._variable_to_check == value_to_check:
                self.result = on_true(*on_true_args, **kwargs)
                result = True

        else:
            if self._check_address:
                result = self._variable_to_check is value_to_check
            else:
                result = self._variable_to_check == value_to_check

        if result: self.__exit()

        return result


