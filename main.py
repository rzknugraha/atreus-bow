import sys
import importlib

def run_controller(controller_name):
    try:
        # Dynamically import the specified controller module
        module = importlib.import_module(f"controllers.{controller_name}")

        # Ensure the module has an `execute` function
        if not hasattr(module, 'execute'):
            raise AttributeError(f"'{controller_name}' module does not contain an 'execute' function.")

        # Call the `execute` function of the imported module
        module.execute()
    
    except ModuleNotFoundError:
        # Handle the case where the specified controller module isn't found
        print(f"Error: Controller '{controller_name}' does not exist. Please provide a valid controller name.")
    
    except AttributeError as e:
        # Handle cases where the module exists but lacks the necessary function
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if the command-line argument was provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <controller_name>")
        sys.exit(1)

    # Get the controller name from the command-line argument
    controller_name = sys.argv[1]
    
    # Run the corresponding controller module
    run_controller(controller_name)
