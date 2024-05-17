# config catalogs

def columns_str_to_type(columns_str):
    ''' 
        Convierte una cadena de nombre de columnas separados por coma a un 
        diccionario del tipo dType para método read_exce() de la lib Pandas
        
        Parameters:
            columns_str : str Ejm:'column1, column2, ...'
        
        Return:
            columns_type = { 'column1' : str, 'column2' : str, ... }
    '''
    columns_type = {}
    if len(columns_str.strip()) > 0:    
        for column in columns_str.split(','):
            columns_type[column.strip()] = str
    return columns_type

