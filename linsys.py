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
            
    def solve(self):
        rref= self.compute_rref()
            
        # no solution, 0=k, infinite solution, 0=0 for pivot
        
        # if there's 0=k in any equation, print no solution, return rref
        for i in range(len(self)):
            if rref[i].normal_vector.is_zero() and (rref[i].constant_term != 0):
                print self.NO_SOLUTIONS_MSG
                return rref
            
        
        # if variables > number of equations, then print infinite solutions, return rref
        if self.dimension > len(self):
            print self.INF_SOLUTIONS_MSG
            self.parametrization(rref)
            return rref

        # if there's 0=0 in any pivot equation, print infinite solution, return rref        
        for i in range(self.dimension):
            if rref[i].normal_vector.is_zero() and (rref[i].constant_term == 0):
                print self.INF_SOLUTIONS_MSG
                self.parametrization(rref)
                return rref
            
        print 'one solution'
        return rref

    def parametrization(self, rref):
        

        free_variables= []
        for i, j in enumerate(rref.indices_of_first_nonzero_terms_in_each_row()):
            if i != j:
                free_variables.append(i)
        free_variables
        

        pivot_in_eq= rref.indices_of_first_nonzero_terms_in_each_row()
        # i need to know which variable in which equations, because sometimes x_3 in 2nd equation
        for i in range(self.dimension):
            # start from first variables
            output= 'x_{}'.format(i+1) + ' = '
            if i in pivot_in_eq:
                # not free
                eq= pivot_in_eq.index(i) # get which equation
                output+= str(round(rref[eq].constant_term, 3))
                for k, l in enumerate(free_variables):
                    if l >= self.dimension:
                    # sometime there will be more free variables than dimension
                        break
                    if rref[eq].normal_vector.coordinates[l] >= 0:
                        output= output + ' - ' + str(round(rref[eq].normal_vector.coordinates[l],3))
                    else:
                        output= output + ' + ' + str(round(abs(rref[eq].normal_vector.coordinates[l]),3))
                    output+= ' t_{}'.format(k+1)  
                print output               
            else:
                for k, l in enumerate(free_variables):
                    if l >= self.dimension:
                        break
                    if i == l:
                        # i == l means i-th variables is free variable
                        output+= '+ 1.0t_{}'.format(k+1)
                    else:
                        # append other variables
                        output+= '+ 0.0t_{}'.format(k+1)            
                print output

                
        
        
            
    def compute_rref(self):
        tf= self.compute_triangular_form()
        
        # if the system has less equation than dimension, or other way around,
        # it may cause index out of range. n stands for number of pivot(maximum)
        if self.dimension > len(self):
            n= len(self)
        else:
            n= self.dimension
        
        # all coefficient of pivot become 1
        for i in range(n):
            for j in range(i, self.dimension):
                # if the coe is 0 on pivot position, then search for next
                if not MyDecimal(tf[i].normal_vector.coordinates[j]).is_near_zero():
                    coe= Decimal('1.0')/tf[i].normal_vector.coordinates[j]
                    tf.multiply_coefficient_and_row(coe, i)
                    break # once done, break the current loop
                    
        for i, j in reversed(list(enumerate(tf.indices_of_first_nonzero_terms_in_each_row()))):
            # i means i-th equation, j means first non-zero variable on i-th equation
            if j == -1:
                # j == -1 means all coe zero, skip this loop
                continue
            for k in range(i-1, -1, -1):             
                coe= tf[k].normal_vector.coordinates[j]
                tf.add_multiple_times_row_to_row(-coe, i, k)
            
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
        pass         


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
p1 = Plane(normal_vector=Vector(['2','4','6']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','2','4']), constant_term='3')


s = LinearSystem([p0,p1,p2])
print s.solve()

p0 = Plane(normal_vector=Vector(['0.786','0.786','0.588']), constant_term='-0.714')
p1 = Plane(normal_vector=Vector(['-0.138','-0.138','0.244']), constant_term='0.319')
s = LinearSystem([p0,p1])
print s.solve()

p0 = Plane(normal_vector=Vector(['8.631','5.112','-1.816']), constant_term='-5.113')
p1 = Plane(normal_vector=Vector(['4.315','11.132','-5.27']), constant_term='-6.775')
p2 = Plane(normal_vector=Vector(['-2.158','3.01','-1.727']), constant_term='-0.831')
s = LinearSystem([p0,p1, p2])
print s.solve()

p0 = Plane(normal_vector=Vector(['0.935','1.76','-9.365']), constant_term='-9.955')
p1 = Plane(normal_vector=Vector(['0.187','0.352','-1.873']), constant_term='-1.991')
p2 = Plane(normal_vector=Vector(['0.374','0.704','-3.746']), constant_term='-3.982')
p3 = Plane(normal_vector=Vector(['-0.561','-1.056','5.619']), constant_term='5.973')
s = LinearSystem([p0, p1, p2, p3])
print s.solve()
