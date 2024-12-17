import os

def generate_api_code(service_name, method, operation_id):
    # Define paths for the app, logic, and _init_ files
    app_file = os.path.join(service_name, "app.py")
    logic_file = os.path.join(service_name, "logic.py")
    init_file = os.path.join(service_name, "_init.py")  # Create or update __init_.py file

    # Ensure the service directory exists
    os.makedirs(service_name, exist_ok=True)

    # Create the _init_.py file to treat the directory as a package
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write(f"# {service_name} service initialization\n")
            f.write(f"from .app import app\n")  # Expose the app in the package

    # Check if the operation_id is already in the app.py file
    if os.path.exists(app_file):
        with open(app_file, "r") as f:
            existing_code = f.read()
            if f"@app.{method}(\"/{operation_id}\")" in existing_code:
                print(f"Operation ID '{operation_id}' already exists in {app_file}. Skipping...")
                return

    # FastAPI Skeleton Code with Class Import and Static Method
    app_code = f"""
from fastapi import FastAPI
from {service_name}.logic import {service_name.capitalize()}Logic  # Import the service logic class
from pydantic import BaseModel  # For request body validation

app = FastAPI()
"""

    # Check if app.py exists and if it's empty, then write the base code
    if not os.path.exists(app_file):
        with open(app_file, "w") as f:
            f.write(app_code)

    # Define the new operation route dynamically for each operation_id
    route_code = f"""
@app.{method}("/{operation_id}")
async def {operation_id}():
    # Call the operation method directly from the class (static method)
    return {service_name.capitalize()}Logic.{operation_id}()
"""

    # Append the route for the new operation to app.py
    with open(app_file, "a") as f:
        f.write(route_code)

    # Logic Class and Method (ensure the method doesn't exist)
    logic_code = f"""
    @staticmethod
    def {operation_id}():
        # Implement the logic for {operation_id} here
        # This is a placeholder
        return {{"message": "Logic for {operation_id} not implemented yet."}}
"""

    # Read the existing logic file to check if the class already exists
    if os.path.exists(logic_file):
        with open(logic_file, "r") as f:
            logic_content = f.read()
            if f"class {service_name.capitalize()}Logic" in logic_content:
                # Class already exists, check if the method exists
                if f"def {operation_id}()" in logic_content:
                    print(f"Method '{operation_id}' already exists in {logic_file}. Skipping...")
                    return
                else:
                    with open(logic_file, "a") as f:
                        f.write(logic_code)
            else:
                with open(logic_file, "w") as f:
                    f.write(f"# Logic for {service_name.capitalize()} service\n")
                    f.write(f"class {service_name.capitalize()}Logic:\n")
                    f.write(logic_code)
    else:
        # If logic file doesn't exist, create it and add the class
        with open(logic_file, "w") as f:
            f.write(f"# Logic for {service_name.capitalize()} service\n")
            f.write(f"class {service_name.capitalize()}Logic:\n")
            f.write(logic_code)

    print(f"API skeleton and logic for '{operation_id}' added to {service_name}.")

if __name__ == "__main__":

    print("Welcome to the Advanced API Code Generation Script for FastAPI!")
    service_name = input("Enter the service name (e.g., service1): ").strip()
    method = input("Enter the HTTP method (get, post, patch, delete): ").lower().strip()
    operation_id = input("Enter the operation ID (unique identifier for the API): ").strip()

    generate_api_code(service_name, method, operation_id)

    print(f"Code generation completed for {service_name}.")