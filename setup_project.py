import os

def create_directories():
    directories = [
        'app',
        'app/api',
        'app/core',
        'app/models',
        'app/services',
        'app/utils',
        'tests',
        'frontend',
        'data',
        'models'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create an empty __init__.py file in each Python package directory
        if directory.startswith('app'):
            with open(os.path.join(directory, '__init__.py'), 'w') as f:
                pass

if __name__ == '__main__':
    create_directories()
