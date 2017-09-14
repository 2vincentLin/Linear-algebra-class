from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec= 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])

            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    # vector plu vector
    def plus(self, v):
        try:
            if self.dimension != v.dimension:
                raise ValueError
        except ValueError:
            raise ValueError('Length is not equal')
            
        new_coordinates= [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    # vectore minus vector
    def minus(self, v):
        try:
            if self.dimension != v.dimension:
                raise ValueError
        except ValueError:
            raise ValueError('Length is not equal')
            
        new_coordinates= [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)     

    # vector time a constant
    def times_scalar(self, c):
        new_coordinates= [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    # calculate the magnitude of the vector    
    def magnitude(self):
        coordinates_squared= [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))
        # after sqrt(), type will become float
 
    # normalize the vector
    def normalized(self):
        try:
            temp= self.magnitude()
            return self.times_scalar(Decimal('1.0')/self.magnitude())
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot normalize the zero vector')
    
    # dot product (inner product)        
    def dot(self, v):
        return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])

    # calculate the angle between two vectors    
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

    # return the if the two vectors orthogonal to each other        
    def is_orthogonal_to(self, v, tolerance= 1e-20):
        return abs(self.dot(v)) < tolerance
    
    # return if the vector is zero vector (I didn't use tolerance)
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

    def cross(self, v):
        try:
            a1, a2, a3= self.coordinates
            b1, b2, b3= v.coordinates
            new_coordinates= [a2*b3 - a3*b2, a3*b1 - b3*a1, a1*b2 - b1*a2]
            return Vector(new_coordinates)
        except Exception as e:
            print str(e)
            print 'only support 3 dimensions vectors'
            
    def area_of_parallelogram_with(self, v):
        return (self.cross(v)).magnitude()
    
    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v)/Decimal('2.0')
        
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates




