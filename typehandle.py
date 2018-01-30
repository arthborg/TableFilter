#!/usr/bin/ent Python 2.7

#==============================================================================
#TYPE HANDLE
#==============================================================================


TYPELIST = []


class TableType():

    def __init__(self, name, group_cols, count_cols, maincol, tgtcol, totalcol, availcol):
        self.name = name
        self.group_cols = group_cols
        #EL = target, newname, [cond1, cond2 ..., condn]
        self.count_cols = count_cols
        self.main_col = maincol
        self.target_col = tgtcol
        self.total_col = totalcol
        self.avail_col = availcol

        self.analysis_flag = True if (self.main_col != None and self.main_col != '') else False
        self.exhaustion_flag = True if (self.total_col != None and self.total_col != '') else False


    def get_exhaustion_flag(self):
        return self.exhaustion_flag

    def get_analysis_flag(self):
        return self.analysis_flag

    def get_main_col(self):
        return self.main_col

    def get_target_col(self):
        return self.target_col

    def get_total_col(self):
        return self.total_col

    def get_avail_col(self):
        return self.avail_col

    def get_name(self):
        return self.name

    def get_group_cols(self):
        gcols = []
        for col in self.group_cols:
            gcols.append(col[0])
        return gcols

    def get_group_cols_newname(self):
        gcols = []
        for col in self.group_cols:
            gcols.append(col[1])
        return gcols

    def get_count_cols_newname(self):
        ccols = []
        for col in self.count_cols:
            ccols.append(col[1])
        return ccols

    def get_count_cols(self):
        ccols = []
        for col in self.count_cols:
            ccols.append(col[0])
        return ccols

    def get_count_cols_condition(self):
        ccols = []
        for col in self.count_cols:
            ccols.append(col[2])
        return ccols

    def get_group_list(self):
        return self.group_cols

    def get_count_list(self):
        return self.count_cols



def initialize_types(filepath):

    global TYPELIST
    TYPELIST = []
    f = open(filepath, 'r')

    name = f.readline()
    while(name != ''):
        groups = f.readline()
        counts = f.readline()
        main_col = f.readline()
        target_col = f.readline()
        total_col = f.readline()
        avail_col = f.readline()

        make_type(name, groups, counts, main_col, target_col, total_col, avail_col)
        name = f.readline()


def make_type(name, groups, counts, main_col, target_col, total_col, avail_col):

    name = name.rstrip()
    groups = groups.split(';')
    counts = counts.split(';')

    final_groups = []
    for g in groups:
        column = g.split(',')
        final_groups.append(column)
    final_groups[-1][-1] = final_groups[-1][-1].rstrip()

    final_counts = []
    for c in counts:
        column = c.split(',')

        condlist = column[2]
        condlist = condlist.split('|')

        column[2] = []
        for i in condlist:
            column[2].append(i)

        final_counts.append(column)

    final_counts[-1][-1][-1] = final_counts[-1][-1][-1].rstrip()

    main_col = main_col.rstrip()
    target_col = target_col.rstrip()
    total_col = total_col.rstrip()
    avail_col = avail_col.rstrip()

    new_type = TableType(name, final_groups, final_counts, main_col, target_col, total_col, avail_col)
    TYPELIST.append(new_type)


def get_analysis_flag(name):
    for t in TYPELIST:
        if name == t.get_name():
            return t.get_analysis_flag()

    return False


def get_exhaustion_flag(name):
    for t in TYPELIST:
        if name == t.get_name():
            return t.get_exhaustion_flag()

    return False


def get_group_list(name):
    for t in TYPELIST:
        if name == t.get_name():
            return t.get_group_list()

    return []


def get_count_list(name):
    for t in TYPELIST:
        if name == t.get_name():
            return t.get_count_list()

    return []


def get_group_cols(name):

    for t in TYPELIST:
        if name == t.get_name():
            return t.get_group_cols()

    return []


def get_group_cols_newname(name):
    
    for t in TYPELIST:
        if name == t.get_name():
            return t.get_group_cols_newname()

    return []


def get_count_cols_newname(name):

    for t in TYPELIST:
        if name == t.get_name():
            return t.get_count_cols_newname()

    return []


def get_main_col(name):

    for t in TYPELIST:
        if name == t.get_name():
            return t.get_main_col()

    return None

def get_target_col(name):

    for t in TYPELIST:
        if name == t.get_name():
            return t.get_target_col()

    return None

def get_total_col(name):

    for t in TYPELIST:
        if name == t.get_name():
            return t.get_total_col()

    return None


def get_avail_col(name):

    for t in TYPELIST:
        if name == t.get_name():
            return t.get_avail_col()

    return None


def get_type_names():

    type_names = []
    for t in TYPELIST:
        type_names.append(t.get_name())
    return type_names


def get_analysis_type_names():

    type_names = []
    for t in TYPELIST:
        if t.get_analysis_flag() is True:
            type_names.append(t.get_name())

    return type_names


def get_details(name):
    
    target = None
    for t in TYPELIST:
        if t.get_name() == name:
            target = t
    
    if target is None:
        return ''
    
    group_cols = target.get_group_cols()
    group_cols_new = target.get_group_cols_newname()
    
    details = 'CONFIGURACOES DE FILTRAGEM\n'
    details += 'COLUNAS DE AGRUPAMENTO:\n'
    for i in range(0, len(group_cols)):

        details += '\tNome original: '+group_cols[i]+ '\n\tNome na tabela filtrada: '+group_cols_new[i]+'\n'

    count_cols = target.get_count_cols()
    count_cols_new = target.get_count_cols_newname()
    count_condition = target.get_count_cols_condition()

    new_list = []

    for element in count_condition:
        
        finalelement = '('
        for el in element:
            finalelement += el
            if el is not element[-1]:
                finalelement += ', '
        
        finalelement += ')'
        new_list.append(finalelement)

    details += '\nCOLUNAS DE CONTAGEM:\n'

    for i in range(0, len(count_cols)):

        details += '\tNome original: '+count_cols[i]+'\n\tNome na tabela filtrada: '+count_cols_new[i]+'\n\tValor analizado na contagem: '+new_list[i]+'\n' 
    

    details += '\nCONFIGURACOES DE ANALIZE\n\n'
    details += 'Analize feita pela coluna: ' + target.get_main_col() + '\n'
    details += 'Analize feita usando dados da coluna: ' + target.get_target_col() + '\n'
    details += 'Coluna que guarda o total: ' + target.get_total_col() + '\n'
    details += 'Coluna que guarda a disponibilidade: ' + target.get_avail_col() + '\n'

    return details
    

def write_new_type(filename, name, count_cols, group_cols, main, target, total, avail):
    
    f = open(filename, 'a')
    f.write(name)

    strgroup = ''

    for g in group_cols:
        strgroup += g[0] + ',' + g[1]
        if g is not group_cols[-1]:
            strgroup += ';'
    f.write('\n')
    f.write(strgroup)

    strcount = ''

    for c in count_cols:
        strcount += c[0] + ',' + c[1] + ','
        
        conditions = c[2].split('|')

        for cond in conditions:
            strcount += cond
            if cond is not conditions[-1]:
                strcount += '|'

        if c is not count_cols[-1]:
            strcount += ';'
    f.write('\n')
    f.write(strcount)

    f.write('\n')
    f.write(main)

    f.write('\n')
    f.write(target)

    f.write('\n')
    f.write(total)

    f.write('\n')
    f.write(avail)
    f.write('\n')
    
    f.close()

    initialize_types(filename)


def purge_type(filename, name):

    index = None
    global TYPELIST
    
    for i in range(0,len(TYPELIST)):

        if TYPELIST[i].get_name() == name:
            index = i
            break

    del TYPELIST[index]
    rewrite_list(filename)


def rewrite_list(filename):

    f = open(filename, 'w')
    global TYPELIST

    for t in TYPELIST:
        f.write(t.get_name())
        group = t.get_group_cols()
        groupnew = t.get_group_cols_newname()

        strgrp = ''
        for i in range(0,len(group)):
            strgrp += group[i] + ',' + groupnew[i]
            if i != len(group)-1:
                strgrp += ';'
        f.write('\n')
        f.write(strgrp)

        count = t.get_count_cols()
        countnew = t.get_count_cols_newname()
        countcond = t.get_count_cols_condition()

        strcnt = ''
        for i in range(0,len(count)):
            strcnt += count[i] + ',' + countnew[i] + ','
            
            for cond in countcond[i]:
                strcnt += cond
                if cond is not countcond[i][-1]:
                    strcnt += '|'

            if i != len(count)-1:
                strcnt += ';'
        f.write('\n')
        f.write(strcnt)

        f.write('\n')
        f.write(t.get_main_col())
        f.write('\n')
        f.write(t.get_target_col())
        f.write('\n')
        f.write(t.get_total_col())
        f.write('\n')
        f.write(t.get_avail_col())
        f.write('\n')

    f.close()
    initialize_types(filename)