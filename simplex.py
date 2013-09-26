import re
class Simplex():
    def __init__(self):
        self.m = 0
        self.n = 0
        self.basic_vars = []
        self.non_basic_vars = []
        self.b_vec = []
        self.matrix = []
        self.coeff = []
        self.objective_value = 0
        self.decision_vars = []
        self.slack_vars = []


    def solve(self):
        counter = 0
        while True:
            val = self.pivot()
            if val == 0:
                print("UNBOUNDED")
                return
            if val == 1:
                print(self.objective_value)
                print(counter)
                return
            counter +=1

    def pivot(self):
        enter_var = self.choose_entervariable()
        leaving_var = self.choose_leavingvariable(enter_var)
        if enter_var == -1:
            return 1
        elif leaving_var == -1:
            return 0
        else:
            self.rearange(enter_var,leaving_var)            


    def rearange(self,enter_var,leaving_var):
        if leaving_var == -1 or enter_var == -1:
            return
        row_index = self.basic_vars.index(leaving_var)
        col_index = self.non_basic_vars.index(enter_var)
        row = self.matrix[row_index] 
        row_elem = row[col_index]
        whole_row = [self.b_vec[row_index]]+row
        new_row = []
        #calculate new row
        new_row = [elem/abs(row_elem) for elem in whole_row]
        new_row[col_index+1] = -1/abs(row_elem)
        self.b_vec[row_index] = new_row[0]
        #update matrix
        new_matrix = []
        m_add_row = new_row[1:]
        for mrow in self.matrix:
            if mrow == row:
                new_matrix.append(m_add_row)
            else:
                factor = mrow[col_index]
                coeff_add = [factor*coef for coef in m_add_row]
                new_matrix_row = [a+b for (a,b) in zip(mrow,coeff_add)]
                new_matrix_row[col_index] = coeff_add[col_index]
                new_matrix.append(new_matrix_row)
        #self.matrix = new_matrix
        #update bvec
        new_b_vec = list(self.b_vec)
        for (index,elem) in zip(range(0,len(self.b_vec)),self.b_vec):
            if index != row_index:
                factor = self.matrix[index][col_index]
                add = factor*new_row[0]
                new_b_vec[index] +=add
        #refresh coeff
        factor = self.coeff[col_index]
        coeff_add = [factor*coef for coef in new_row]
        new_coeff = [a+b for (a,b) in zip(self.coeff,coeff_add[1:])]
        new_coeff[col_index] = coeff_add[col_index+1]
        old_obj = self.objective_value
        new_obj = old_obj+coeff_add[0]
        self.objective_value = new_obj
        self.coeff = new_coeff
        #update non- and basic-vars
        self.non_basic_vars[col_index] = leaving_var
        self.basic_vars[row_index] = enter_var
        self.matrix = new_matrix
        self.b_vec = new_b_vec
       # self.basic_vars[row_index] = enter_var
       # print("new non_basic: "+str(self.non_basic_vars))
       # print("new basic: "+str(self.non_basic_vars))
       # print("new coeff: "+str(self.coeff))



    def choose_entervariable(self):
        possible_zip = zip(self.non_basic_vars,self.coeff)
        possible = [elem for elem in possible_zip if elem[1]>0]
        choose = 0
        if len(possible)==0:
            return -1
        else:
            choose = possible[0][0]
            for elem in possible:
                if elem[0]<choose:
                    choose= elem[0]
        return choose
                 

    def choose_leavingvariable(self,enter_var):
        if enter_var == -1:
            return -1
        index_help =zip(range(0,len(self.coeff)),self.non_basic_vars,\
                self.coeff)
        index_help = list(index_help)
        index = -1
        for elem in index_help:
            if elem[1] == enter_var:
                index = elem[0]
        assert(index != -1)
        b_vec = self.b_vec
        matrix = self.matrix
        basic_vars = self.basic_vars
        possible = [row[index] for row in matrix]
        possible_zip = zip(range(0,len(possible)),basic_vars,possible,b_vec)
        possible = [(abs(elem[3]/elem[2]),elem) for elem in possible_zip \
                if elem[2]<0]
        if len(possible) == 0:
            return -1
        choose = possible[0][1]
        minval = possible[0][0]
        for elem in possible:
            if elem[0] < minval:
                choose = elem[1]
                minval = elem[0]
        collection = []
        for elem in possible:
            if minval == elem[0]:
                collection.append(elem)
        if len(collection)>1:
            for elem in collection:
                if elem[1][1] < choose[1]:
                    choose = elem[1]
        return choose[1]

    def match_input(self,line):
        matcher = re.compile("(-\d+\.\d+)|(\d+\.\d+)|(-\d+)|(\d+)")
        elems = []
        i = 0
        while i<len(line):
            if i<len(line) and line[i]!= " ":
                str = line[i:]
                m = matcher.match(str)
                elems.append(m.group())
                end = m.end()
                i+=end
            i+=1
        return [float(elem) for elem in elems]

    def set_NM(self):
        line = input()
        xs =self.match_input(line)
        self.m = int(xs[0])
        self.n = int(xs[1])

    def set_basic_vars(self):
        line = input()
        vars = self.match_input(line)
        for i in vars:
            self.basic_vars.append(int(i))
            

    def set_non_basic_vars(self):
        line = input()
        vars = self.match_input(line)
        for i in vars:
            self.non_basic_vars.append(int(i))

    def set_b_vec(self):
        line = input()
        self.b_vec = self.match_input(line)

    def set_matrix(self):
        for i in range (0,self.m):
            line = input()
            self.matrix.append(self.match_input(line))
            
    def set_coeff(self):
        line = input()
        self.objective_value = self.match_input(line)[0]
        self.coeff = self.match_input(line)[1:]

    def set_decision_vars(self):
        for i in range(1,self.n+1):
           self.decision_vars.append("x"+str(i))

    def set_slack_vars(self):
        for i in range(self.n+1,self.n+self.m+1):
            self.slack_vars.append("x"+str(i))
            
    def build_from_input(self):
        self.set_NM()
        self.set_basic_vars()
        self.set_non_basic_vars()
        self.set_b_vec()
        self.set_matrix()
        self.set_coeff()
        self.set_decision_vars()
        self.set_slack_vars()
