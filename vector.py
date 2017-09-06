from math import sqrt

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            # tuple will raise a TypeError if coordinates is not iterable
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')
            
    def plus(self, v):
        try:
            if self.dimension != v.dimension:
                raise ValueError
        except ValueError:
            raise ValueError('Length is not equal')
            
        new_coordinates= [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self, v):
        try:
            if self.dimension != v.dimension:
                raise ValueError
        except ValueError:
            raise ValueError('Length is not equal')
            
        new_coordinates= [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)     

    def times_scalar(self, c):
        new_coordinates= [c*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        coordinates_squared= [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))
    
    def normalized(self):
        try:
            return self.times_scalar(1./self.magnitude())
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot normalize the zero vector')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

test= Vector([0])

print test.normalized()

