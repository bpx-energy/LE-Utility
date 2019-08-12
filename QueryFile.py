
 
def GetRoutes(area):
    query = 'select distinct Route from [dimensions].[wells] where [Area] = \'' + area + '\''
    return query

def GetWells(area, route):
    query = 'select distinct WellName from [dimensions].[wells] where [Route] = \'' + route + '\' and [Area] = \'' + area + '\''
    return query



