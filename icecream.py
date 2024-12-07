def icAll(func, verbose=False):
    """
    A decorator that uses icecream to automatically applies ic to every variable in the function

    :param func: Function to be decorated
    :param verbose: If True, print meta information ('variables', 'func', 'signature', 'parameters')
    :return: decorator
    """
    def wrapper(*args, **kwargs):
        # Retrieve the function's signature (parameters)
        signature = inspect.signature(func)
        parameters = signature.parameters

        # Combine function arguments and keyword arguments into a dictionary
        variables = {k: v for k, v in zip(parameters, args)}
        variables.update(kwargs)

        # Retrieve local variables defined in the function body
        result = func(*args, **kwargs)

        # Get the local variables in the function using inspect
        frame = inspect.currentframe().f_locals
        variables.update(frame)

        # Log variables using icecream
        for var_name, var_value in variables.items():
            if verbose:
                ic(var_name, var_value)  # Print variable names and values if verbose is Truei
            else:
                if var_name not in ['variables', 'func', 'signature', 'parameters']:
                    ic(var_name, var_value)

        return result

    return wrapper

@icAll
def example_function(cameraPoint1, cameraPoint2, cameraPoint3, real_point1, real_point2):
    c = (cameraPoint1[0] + real_point1[0]) / 2
    d = (cameraPoint2[1] + real_point2[1]) / 2
    return c, d

example_function((1, 3), (1.5, 1.5), (1, 3), (2, 4), (2, 2.5))
