def load_json_to_class(json_file_path, cls):
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Ensure the JSON file has the correct structure (a list of objects)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("The JSON file must contain a list of objects.")

    # Extract attribute names from the class by instantiating an empty instance
    temp_instance = cls()
    class_attributes = temp_instance.__dict__.keys()

    # List to store instances of the class
    instances = []

    for obj_data in data:
        # Filter JSON data to only include keys matching class attributes
        filtered_data = {k: v for k, v in obj_data.items() if k in class_attributes}

        # Check for missing attributes and set them to None
        missing_attrs = set(class_attributes) - set(obj_data.keys())
        for missing in missing_attrs:
            filtered_data[missing] = None
            warnings.warn(f"Attribute '{missing}' is missing in JSON data and will be set to None.")

        # Create an instance of the class with the filtered data
        instance = cls(**filtered_data)
        instances.append(instance)

    return instances

instances = load_json_to_class('file.json', MyClass)
for instance in instances:
    print(instance)
