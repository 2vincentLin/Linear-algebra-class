from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec= 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
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
        new_coordinates= [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        coordinates_squared= [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))
        # after sqrt(), type will become float
    
    def normalized(self):
        try:
            temp= self.magnitude()
            return self.times_scalar(Decimal('1.0')/self.magnitude())
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot normalize the zero vector')
            
    def dot(self, v):
        return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])
    
    def angle_with(self, v, in_degrees= False):
        try:
            u1= self.normalized()
            u2= v.normalized()
            angle_in_radians= acos(u1.dot(u2))
            
            if in_degrees:
                return angle_in_radians*180./pi
            else:
                return angle_in_radians
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot compute angle with zero vector')
        # if zero vector, normalized will raise ZeroDivisionError
        
    def is_orthogonal_to(self, v, tolerance= 1e-20):
        return abs(self.dot(v)) < tolerance
    
    def is_zero(self):
        return sum([abs(x) for x in self.coordinates]) == 0
    
    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi)

    def component_parallel_to(self, basis):
        try:
            u= basis.normalized()
            return u.times_scalar(self.dot(u))
        except ZeroDivisionError:
            raise ZeroDivisionError('Zero vector has no unique parallel component')
            
    def component_orthogonal_to(self, basis):
        try:
            projection= self.component_parallel_to(basis)
            return self.minus(projection)
        except ZeroDivisionError:
            raise ZeroDivisionError('Zero vector has no unique orthogonal component')
        # in here, from normalized() to component_parallel_to(), you have to
        # keep raise ZeroDivisionError, 
        
        
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

test= Vector([0, 0])
test1= Vector([0,1])

print test.component_orthogonal_to(test1)
