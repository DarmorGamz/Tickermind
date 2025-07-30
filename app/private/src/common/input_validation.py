class InputValidator:
    RULES = {
        "userId": {"type": int, "mandatory": True},
        "username": {"type": str, "mandatory": False}
    }
    
    def validate(self, inputs):
        errors = []
        for name, rule in self.RULES.items():
            if name not in inputs:
                if rule["mandatory"]:
                    errors.append(f"Missing mandatory input: {name}")
                continue
            
            value = inputs[name]
            if value is not None and not isinstance(value, rule["type"]):
                errors.append(f"Invalid type for {name}: expected {rule['type'].__name__}, got {type(value).__name__}")
        
        if errors:
            raise ValueError("; ".join(errors))
        return True


# Example usage:
'''
validator = InputValidator()
    
    # Valid input
    try:
        validator.validate({"userId": 123, "username": "john"})
        print("Validation passed")
    except ValueError as e:
        print(f"Validation failed: {e}")
    
    # Invalid: missing mandatory userId
    try:
        validator.validate({"username": "john"})
        print("Validation passed")
    except ValueError as e:
        print(f"Validation failed: {e}")
    
    # Invalid: wrong type for userId
    try:
        validator.validate({"userId": "123", "username": "john"})
        print("Validation passed")
    except ValueError as e:
        print(f"Validation failed: {e}")
'''