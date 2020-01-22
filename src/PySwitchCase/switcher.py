
class BreakCase(Exception): pass
class ActiveSessionError(Exception): pass
class InactiveSessionError(Exception): pass


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
    _variable_to_check: any
    result = None

    _active: bool = False
    _check_address: bool = False
    _Check_Instance: bool = False
    _Check_SubClass: bool = False
    _no_match_handler: callable
    _no_match_handler_args: tuple
    _no_match_handler_kwargs: dict
    def __init__(self, variable_to_check: any, *,
                 Check_Address: bool = False,
                 Check_Instance: bool = False,
                 Check_SubClass: bool = False,
                 catch_value_to_check: bool = False,

                 no_match_handler: callable or Exception = None,
                 no_match_handler_args: tuple = (),
                 **kwargs):
        """


        :param variable_to_check: the instance to check against.
        :param Check_Address: Checks the addresses between variable_to_check and the value_to_check, using "is".
        :param catch_value_to_check: If match is True, added the value_to_check to on_true_args at the start.
        :param no_match_handler: Optional Method that is called if no match is found or Exception that is raised if no match is found.
        :param no_match_handler_args: no_match_handler's args
        :param kwargs: no_match_handler's kwargs
        """
        if not hasattr(variable_to_check, '__eq__'):
            raise ValueError(f'variable_to_check is not comparable type. {type(variable_to_check)}')
        if no_match_handler is None and no_match_handler_args != () and kwargs != {}:
            raise ValueError('no_match_handler is None but its args and kwargs are passed in.')
        self._variable_to_check = variable_to_check
        self._check_address = Check_Address
        self._Check_Instance = Check_Instance
        self._Check_SubClass = Check_SubClass


        self._no_match_handler = no_match_handler
        self._catch_value_to_check = catch_value_to_check
        self._no_match_handler_args = no_match_handler_args
        self._no_match_handler_kwargs = kwargs

    def __enter__(self):
        self._active = True
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        if isinstance(exc_val, BreakCase): return True
        else:
            if self._no_match_handler is None: pass
            elif callable(self._no_match_handler): self._no_match_handler(*self._no_match_handler_args, **self._no_match_handler_kwargs)
            elif issubclass(self._no_match_handler, BaseException): raise self._no_match_handler(*self._no_match_handler_args, **self._no_match_handler_kwargs)
    def __exit(self):
        raise BreakCase()
    @staticmethod
    def _to_type(obj: any):
        return type(obj) if obj.__class__ != type.__class__ else obj
    def _convert_to_types(self, value_to_check: any) -> tuple or type:
        if isinstance(value_to_check, (list, tuple)):
            return tuple(map(self._to_type, value_to_check))

        elif value_to_check.__class__ != type.__class__:
            return type(value_to_check)
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

    def set_variable_to_check(self, new):
        self._variable_to_check = new

    def __call__(self, value_to_check: any, *args, callback: callable = None, **kwargs) -> bool:
        """
            Exits the Context Manger if a match is found with self.__exit().

        :param value_to_check: the instance or value to check self._variable_to_check against. Should be one of [ variable OR instance OR type OR tuple of types ].
        :type value_to_check: any value (example: integer, string, float, etc.) or tuple of types or type

        :param callback: handler method to be called if match is True.
        :param args: callback's args if match is True: callback(*args, **kwargs).
        :param kwargs: on_true's kwargs if match is True: callback(*args, **kwargs).
        :return: bool.
        """
        if not self._active: self._raise_inactive()
        if self._catch_value_to_check: args = (value_to_check, *args)  # adds this value_to_check to the callback's args.



        checked = False
        if callable(callback):
            if self._Check_SubClass:
                if issubclass(type(self._variable_to_check), self._convert_to_types(value_to_check)):
                    self.result = callback(*args, **kwargs)
                    checked = True


            elif self._Check_Instance:
                if isinstance(self._variable_to_check, self._convert_to_types(value_to_check)):
                    self.result = callback(*args, **kwargs)
                    checked = True


            elif self._check_address and self._variable_to_check is value_to_check:
                self.result = callback(*args, **kwargs)
                checked = True


            elif self._variable_to_check == value_to_check:
                self.result = callback(*args, **kwargs)
                checked = True

        else:
            if self._Check_SubClass:
                checked = issubclass(type(self._variable_to_check), self._convert_to_types(value_to_check))


            elif self._Check_Instance:
                checked = isinstance(self._variable_to_check, self._convert_to_types(value_to_check))


            elif self._check_address:
                checked = self._variable_to_check is value_to_check


            else:
                checked = self._variable_to_check == value_to_check


        if checked: self.__exit()
        return checked



