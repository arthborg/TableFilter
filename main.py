import standart as std
import pypostgre as ppg
import analytics as ant
import convert as cvt

def main():
    print 'LETS GET THIS PARTY STARTEDDDD'
    db = std.DBNAME

    if ppg.check_database(db) is False:
        s = raw_input('Digite a senha para criar uma db: ')
        ppg.create_database(db, s)

    else:
        print 'DB LOCALIZADA'

    std.standardize()
    


main()


# EXCEL TO CSV
# CSV TO TABLE
# EXCEL TO TABLE




'''

________________________________________________________________________
|               ___________                                             |
|    filename = [_________]                                             |
|    O create csv file                                                  |
|                                                                       |
|                                                                       |
|                                                                       |
|                                                                       |
|                                                                       |
|              ______________                                           |
|    analizar [______________]                                          |
|    select   [______________]                                          |
|                                                                       |
|    O media movel                                                      |
|    O sse                                                              |
|    O media movel ponderada                                            |
|                                                                       |
|                                                                       |
|                                                                       |
|                                                                       |
|    O gerar tabela                                                     |
|                                                                       |
|                                                                       |
|                                                                       |
|                                                                       |
|_______________________________________________________________________|


'''