#!/usr/bin/python2.7

""" Handle types and type files """

TYPELIST = []


class TableType(object):
    """ Implements a type and its methods """

    def __init__(self, name, group_cols, count_cols, maincol, tgtcol, totalcol, availcol):
        self.name = name
        self.group_cols = group_cols
        self.count_cols = count_cols
        self.main_col = maincol
        self.target_col = tgtcol
        self.total_col = totalcol
        self.avail_col = availcol

    def get_exhaustion_flag(self):
        """ Gets the exhaustion flag """
        return self.total_col != None and self.total_col != ''

    def get_analysis_flag(self):
        """ Gets the analysis flag """
        return self.main_col != None and self.main_col != ''

    def get_main_col(self):
        """ Gets the main column """
        return self.main_col

    def get_target_col(self):
        """ Gets the target column """
        return self.target_col

    def get_total_col(self):
        """ Gets the total column """
        return self.total_col

    def get_avail_col(self):
        """ Gets the available column """
        return self.avail_col

    def get_name(self):
        """ Gets the name of the type """
        return self.name

    def get_group_cols(self):
        """ Gets the group columns """
        gcols = []
        for col in self.group_cols:
            gcols.append(col[0])
        return gcols

    def get_group_cols_newname(self):
        """ Gets the new name of the group columns """
        gcols = []
        for col in self.group_cols:
            gcols.append(col[1])
        return gcols

    def get_count_cols_newname(self):
        """ Gets the new name of the count columns """
        ccols = []
        for col in self.count_cols:
            ccols.append(col[1])
        return ccols

    def get_count_cols(self):
        """ Gets the count columns """
        ccols = []
        for col in self.count_cols:
            ccols.append(col[0])
        return ccols

    def get_count_cols_condition(self):
        """ Gets the count columns conditions """
        ccols = []
        for col in self.count_cols:
            ccols.append(col[2])
        return ccols

    def get_group_list(self):
        """ Gets the raw group columns list """
        return self.group_cols

    def get_count_list(self):
        """ Gets the raw count columns list """
        return self.count_cols


def initialize_types(filepath):
    """ Initializes the types based on the type file on standart.py """

    global TYPELIST
    TYPELIST = []
    type_file = open(filepath, 'r')

    name = type_file.readline()
    while name != '':
        groups = type_file.readline()
        counts = type_file.readline()
        main_col = type_file.readline()
        target_col = type_file.readline()
        total_col = type_file.readline()
        avail_col = type_file.readline()

        make_type(name, groups, counts, main_col,
                  target_col, total_col, avail_col)
        name = type_file.readline()

    type_file.close()


def make_type(name, groups, counts, main_col, target_col, total_col, avail_col):
    """ Makes a new type and appends it to the TYPELIST variable """

    name = name.rstrip()
    groups = groups.split(';')
    counts = counts.split(';')

    final_groups = []
    for group in groups:
        column = group.split(',')
        final_groups.append(column)
    final_groups[-1][-1] = final_groups[-1][-1].rstrip()

    final_counts = []
    for count in counts:
        column = count.split(',')

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

    new_type = TableType(name, final_groups, final_counts,
                         main_col, target_col, total_col, avail_col)
    TYPELIST.append(new_type)


def get_analysis_flag(name):
    """ Get the analysis flag for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_analysis_flag()

    return False


def get_exhaustion_flag(name):
    """ Get the exhaustion flag for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_exhaustion_flag()

    return False


def get_group_list(name):
    """ Get the group list for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_group_list()

    return []


def get_count_list(name):
    """ Get the count list for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_count_list()

    return []


def get_group_cols(name):
    """ Get the group columns for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_group_cols()

    return []


def get_group_cols_newname(name):
    """ Get the new name of the group columns for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_group_cols_newname()

    return []


def get_count_cols_newname(name):
    """ Get the new name of the count columns for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_count_cols_newname()

    return []


def get_main_col(name):
    """ Get the main column for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_main_col()

    return None


def get_target_col(name):
    """ Get the target column for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_target_col()

    return None


def get_total_col(name):
    """ Get the total column for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_total_col()

    return None


def get_avail_col(name):
    """ Get the available column for a specific type """

    for tb_type in TYPELIST:
        if name == tb_type.get_name():
            return tb_type.get_avail_col()

    return None


def get_type_names():
    """ Gets the names of the types """

    type_names = []
    for tb_type in TYPELIST:
        type_names.append(tb_type.get_name())
    return type_names


def get_analysis_type_names():
    """ Get the name of the type that can be analyzed """
    type_names = []
    for tb_type in TYPELIST:
        if tb_type.get_analysis_flag() is True:
            type_names.append(tb_type.get_name())

    return type_names


def get_details(name):
    """ Get the details from a specific type """

    target = None
    for tb_type in TYPELIST:
        if tb_type.get_name() == name:
            target = tb_type

    if target is None:
        return ''

    group_cols = target.get_group_cols()
    group_cols_new = target.get_group_cols_newname()

    details = 'CONFIGURACOES DE FILTRAGEM\n'
    details += 'COLUNAS DE AGRUPAMENTO:\n'
    for i, item in enumerate(group_cols):

        details += '\tNome original: ' + \
            item + '\n\tNome na tabela filtrada: ' + \
            group_cols_new[i] + '\n'

    count_cols = target.get_count_cols()
    count_cols_new = target.get_count_cols_newname()
    count_condition = target.get_count_cols_condition()

    new_list = []

    for element in count_condition:

        finalelement = '('
        for elmt in element:
            finalelement += elmt
            if elmt is not element[-1]:
                finalelement += ', '

        finalelement += ')'
        new_list.append(finalelement)

    details += '\nCOLUNAS DE CONTAGEM:\n'

    for i, item in enumerate(count_cols):

        details += '\tNome original: ' + item + '\n\tNome na tabela filtrada: ' + \
            count_cols_new[i] + \
            '\n\tValor analizado na contagem: ' + new_list[i] + '\n'

    details += '\nCONFIGURACOES DE ANALIZE\n\n'
    details += 'Analize feita pela coluna: ' + target.get_main_col() + '\n'
    details += 'Analize feita usando dados da coluna: ' + target.get_target_col() + \
        '\n'
    details += 'Coluna que guarda o total: ' + target.get_total_col() + '\n'
    details += 'Coluna que guarda a disponibilidade: ' + target.get_avail_col() + \
        '\n'

    return details


def write_new_type(filename, name, count_cols, group_cols, main, target, total, avail):
    """ Writes the new type on the type file """

    type_file = open(filename, 'a')
    type_file.write(name)

    strgroup = ''

    for group in group_cols:
        strgroup += group[0] + ',' + group[1]
        if group is not group_cols[-1]:
            strgroup += ';'
    type_file.write('\n')
    type_file.write(strgroup)

    strcount = ''

    for count in count_cols:
        strcount += count[0] + ',' + count[1] + ','

        conditions = count[2].split('|')

        for cond in conditions:
            strcount += cond
            if cond is not conditions[-1]:
                strcount += '|'

        if count is not count_cols[-1]:
            strcount += ';'
    type_file.write('\n')
    type_file.write(strcount)

    type_file.write('\n')
    type_file.write(main)

    type_file.write('\n')
    type_file.write(target)

    type_file.write('\n')
    type_file.write(total)

    type_file.write('\n')
    type_file.write(avail)
    type_file.write('\n')

    type_file.close()

    initialize_types(filename)


def purge_type(filename, name):
    """ Delets a type """

    index = None
    #global TYPELIST

    for i, item in enumerate(TYPELIST):

        if item.get_name() == name:
            index = i
            break

    del TYPELIST[index]
    rewrite_list(filename)


def rewrite_list(filename):
    """ Rewrites the list of types on the type file """

    type_file = open(filename, 'w')
    #global TYPELIST

    for tb_type in TYPELIST:
        type_file.write(tb_type.get_name())
        group = tb_type.get_group_cols()
        groupnew = tb_type.get_group_cols_newname()

        strgrp = ''
        for i, item in enumerate(group):
            strgrp += item + ',' + groupnew[i]
            if i != len(group) - 1:
                strgrp += ';'
        type_file.write('\n')
        type_file.write(strgrp)

        count = tb_type.get_count_cols()
        countnew = tb_type.get_count_cols_newname()
        countcond = tb_type.get_count_cols_condition()

        strcnt = ''
        for i, item in enumerate(count):
            strcnt += item + ',' + countnew[i] + ','

            for cond in countcond[i]:
                strcnt += cond
                if cond is not countcond[i][-1]:
                    strcnt += '|'

            if i != len(count) - 1:
                strcnt += ';'
        type_file.write('\n')
        type_file.write(strcnt)

        type_file.write('\n')
        type_file.write(tb_type.get_main_col())
        type_file.write('\n')
        type_file.write(tb_type.get_target_col())
        type_file.write('\n')
        type_file.write(tb_type.get_total_col())
        type_file.write('\n')
        type_file.write(tb_type.get_avail_col())
        type_file.write('\n')

    type_file.close()
    initialize_types(filename)
