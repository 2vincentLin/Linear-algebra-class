from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def is_parallel_to(self, ell):
        return self.normal_vector.is_parallel_to(ell.normal_vector)
    
    def __eq__(self, ell):
        # if self and other all zero, check constant
        # if self is zero and other not, or vise versa, not way equal
        if self.normal_vector.is_zero():
            if not ell.normal_vector.is_zero():
                return False
            else:
                return MyDecimal(self.constant_term - ell.constant_term).is_near_zero()
        elif ell.normal_vector.is_zero():
            return False
        
        # if they aren't parallel, then no way they are the same
        if not self.is_parallel_to(ell):
            return False
        
        # if the same, then normal vector should orthogonal to itself.
        # in here, self.basepoint.minus(ell.basepoint) is itself
        return self.normal_vector.is_orthogonal_to(self.basepoint.minus(ell.basepoint))
    
    def intersection_with(self, ell):
        # I use a1*x_1 + a2*x_2 = k1
        try:
            a1, a2= self.normal_vector.coordinates
            b1, b2= ell.normal_vector.coordinates
            k1, k2= self.constant_term, ell.constant_term
            
            p1, p2= b2*k1 - a2*k2, a1*k2 - b1*k1
            
            return Vector([p1, p2]).times_scalar(Decimal('1.0')/(a1*b2 - a2*b1))
        except ZeroDivisionError:
            if self == ell:
                return self
            else:
                return None

    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector.coordinates

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

test= Line(Vector([1, 1]), 4)
test1= Line(Vector([1, 1]), 3)


print test.intersection_with(test1)
