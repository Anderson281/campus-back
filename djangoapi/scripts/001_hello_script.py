"""
This files can be executed in the following way:

    python manage.py runscript script_without_extension

The scripts must be in the folder scripts

You can pass parameters to the scritp in the following way:+

    python manage.py runscript script_without_extension --script-args param1 param2 ...

    python manage.py runscript --script-args jaime martin 10 20

All parameters are received in string format

"""

def run(*args):
    """python manage.py runscript --script-args jaime martin 10 20 ..."""
    print(__file__)
    print("Hello script")

    if args:
        print("All args are received in string format")
        print(args)
        for arg in args:
            print(f"Hola, recibí el parámetro: {arg}")
    else:
        print("No se pasaron parámetros.")