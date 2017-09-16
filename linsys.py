from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)
            
            
    def compute_rref(self):
        tf= self.compute_triangular_form()
        
        # if the system has less equation than dimension, or other way around,
        # it may cause index out of range
        if self.dimension > len(self):
            n= len(self)
        else:
            n= self.dimension
        
        # all coefficient of pivot go to 1
        for i in range(n):
            if not MyDecimal(tf[i].normal_vector.coordinates[i]).is_near_zero():
                coe= Decimal('1.0')/tf[i].normal_vector.coordinates[i]
                tf.multiply_coefficient_and_row(coe, i)
        
        # this loop perform elimination from bottom to top        
        for i in range(n - 1, 0, -1):
            # loop from [n -1, ... ,2,1]
            for j in range(i-1, -1, -1):
                # loop from [n-1,..., 1,0]
                if not MyDecimal(tf[i].normal_vector.coordinates[i]).is_near_zero():
                    # this check may not be necessary because impossible to have ZeroDivisionError

                    coe= tf[j].normal_vector.coordinates[i]
                    tf.add_multiple_times_row_to_row(-coe, i, j)      
                            
        return tf
            
    def compute_triangular_form(self):
        system= deepcopy(self)
        

        for i in range(len(system)-1):
            
            # this loop will swap equations when its pivot = 0 to next (downward)
            # equation whose variable on the same position is not 0            
            for j in range(system.dimension):
                if (i == j) and (MyDecimal(system[i].normal_vector.coordinates[i]).is_near_zero()):
                    temp= i+1
                    while temp < len(system):
                        #print system[temp].normal_vector.coordinates[j]
                        if system[temp].normal_vector.coordinates[i] != 0:
                            system.swap_rows(i, temp)
                            break
                        temp += 1
                        
            #print 'after swap: \n', system

            # this loop will perform elimination downward for each i
            for j in range(i+1, len(system)):
                #print 'i, j: ', i, j
                
                # when there are two equal equations in the system, will have ZeroDivisionError
                if not MyDecimal(system[i].normal_vector.coordinates[i]).is_near_zero():
                    #print system[i].normal_vector.coordinates[i], system[j].normal_vector.coordinates[i]
                    coe= system[j].normal_vector.coordinates[i]/system[i].normal_vector.coordinates[i]
                    system.add_multiple_times_row_to_row(-coe, i, j)


        return system


    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]


    def multiply_coefficient_and_row(self, coefficient, row):
        new_n= self[row].normal_vector.times_scalar(coefficient)
        new_k= self[row].constant_term*coefficient
        self[row]= Plane(normal_vector=new_n, constant_term= new_k)
        pass # add your code here


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        add_vector= self[row_to_add].normal_vector.times_scalar(coefficient)
        add_term= self[row_to_add].constant_term*coefficient
        new_vector= self[row_to_be_added_to].normal_vector.plus(add_vector)
        new_constant= self[row_to_be_added_to].constant_term + add_term
        self[row_to_be_added_to]= Plane(new_vector, new_constant)
        pass # add your code here
        



    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        # these method can let you use LinearSystem[i] to access self.planes[i]
        return self.planes[i]


    def __setitem__(self, i, x):
        # like __getitem__, this method can let you use LinearSystem[i] == new plane
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps



p0 = Plane(normal_vector=Vector(['1','2','3']), constant_term='1')
p1 = Plane(normal_vector=Vector(['4','5','6']), constant_term='4')
p2 = Plane(normal_vector=Vector(['7','8','4']), constant_term='8')

s = LinearSystem([p0,p1,p2])

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1','0','0']), constant_term='-1') and
        r[1] == p2):
    print 'test case 1 failed'

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
r = s.compute_rref()
if not (r[0] == p1 and
        r[1] == Plane(constant_term='1')):
    print 'test case 2 failed'

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
s = LinearSystem([p1,p2,p3,p4])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1','0','0']), constant_term='0') and
        r[1] == p2 and
        r[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
        r[3] == Plane()):
    print 'test case 3 failed'

p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1','0','0']), constant_term=Decimal('23')/Decimal('9')) and
        r[1] == Plane(normal_vector=Vector(['0','1','0']), constant_term=Decimal('7')/Decimal('9')) and
        r[2] == Plane(normal_vector=Vector(['0','0','1']), constant_term=Decimal('2')/Decimal('9'))):
    print 'test case 4 failed'