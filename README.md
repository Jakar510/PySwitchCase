# PySwitchCase
A pure python way to efficiently do a c++ style switch case in Python 3.7+. Should work in 3.6 as well.



# ------------- Usage -------------
See https://github.com/Jakar510/PySwitchCase/blob/master/src/PySwitchCase/examples.py for more examples.

example 1

    test = 10
    with SwitchCase(test) as sc:
        sc(2, on_true=print, on_true_args=('test 1',) )
        print('sub 1')
        sc(10, on_true=print, on_true_args=('test 2',) )  # will break here due to match found.
        print('sub 2')
        sc(12, on_true=print, on_true_args=('test 3',) )

example 2

    test = '10'
    with SwitchCase(test, catch_value_to_check=True) as sc:
        on_true = lambda x: print(f'testing... {x}')

        sc(2, on_true=on_true)
        print('sub 1')
        sc('1', on_true=on_true)
        print('sub 2')
        sc('10', on_true=on_true)  # will break here due to match found.

example 3
    
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