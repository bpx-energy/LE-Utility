


def ImportByScenario(scenarioName):
    import BPXDatabase as bpxdb
    import QueryFile as qf
    import pandas as pd

    #Create ODS and EDW objects
    ODSobj = bpxdb.GetDBEnvironment('ProdODS', 'OVERRIDE')
    EDWobj = bpxdb.GetDBEnvironment('ProdEDW', 'OVERRIDE')

    scenario_query = qf.ScenarioQuery(scenarioName)
    results = ODSobj.Query(scenario_query)

    #Extract APINumbers from the results and concatenate into an 'IN' sql clause
    API_list = []
    for result in results[0]:
        if not result['API10'] in API_list:
            API_list.append(result['API10'])

    in_clause = 'where '

    

