provider_registry = {}

def register_provider(name, provider_class):
    """Register a provider class under a specific name."""
    provider_registry[name] = provider_class

def get_provider(name):
    """Retrieve a provider class by name."""
    provider_class = provider_registry.get(name)
    if provider_class is None:
        raise ValueError(f"No provider registered under the name '{name}'")
    return provider_class
