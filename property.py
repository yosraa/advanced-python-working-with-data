class Rectangle:
    def __init__(self, width, height):
        self._width = width  # Private attribute
        self._height = height  # Private attribute

    # Define a property for "width"
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive.")
        self._width = value

    # Define a property for "height"
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive.")
        self._height = value

    # Calculated property: area
    @property
    def area(self):
        return self._width * self._height


# Using the Rectangle class
rect = Rectangle(5, 10)

# Accessing the properties
print(f"Width: {rect.width}")  # Uses the getter for width
print(f"Height: {rect.height}")  # Uses the getter for height
print(f"Area: {rect.area}")  # Calculated dynamically

# Modifying properties
rect.width = 7
print(f"New width: {rect.width}")
print(f"New area: {rect.area}")

# Trying to set a negative width
try:
    rect.width = -3
except ValueError as e:
    print(f"Error: {e}")
