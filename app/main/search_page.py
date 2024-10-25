from flask import render_template, request

from .views import main_bp, Link
from owlready2 import default_world

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    # Parameters
    rdf_type = request.args.get('rdf_type', '?type')
    search = request.args.get('name', '')

    pageSize = int(request.args.get('pageSize', 20))
    page = int(request.args.get('page', 1))

    # Count filters
    count_filters = []

    # Procedure count filter
    procedure_count = request.args.get('procedureCount')
    if (procedure_count):
        if (rdf_type == 'ifixthat:Part'):
            count_filters.append(
                ('(COUNT(?procedure) AS ?procedureCount)',
                 '?procedure ifixthat:guideOf ?entity .',
                 f'COUNT(?procedure) >= {procedure_count}'))
        elif (rdf_type == 'ifixthat:Item'):
            count_filters.append(
                ('(COUNT(?procedure) AS ?procedureCount)',
                 '?procedure ifixthat:guideOf ?entity .',
                 f'COUNT(?procedure) >= {procedure_count}'))
    
    # Step count filter     
    step_count = request.args.get('stepCount')
    if (step_count):
        if (rdf_type == 'ifixthat:Tool'):
            count_filters.append(
                ('(COUNT(?step) AS ?stepCount)',
                 '?step ifixthat:usesTool ?entity .',
                 f'COUNT(?step) >= {step_count}'))
        elif (rdf_type == 'ifixthat:Procedure'):
            count_filters.append(
                ('(COUNT(?step) AS ?stepCount)',
                 '?entity ifixthat:hasStep ?step .',
                 f'COUNT(?step) >= {step_count}'))
            
    # Item count filter  
    item_count = request.args.get('itemCount')
    if (item_count):
        if (rdf_type == 'ifixthat:Part'):
            count_filters.append(
                ('(COUNT(?item) AS ?itemCount)',
                 '?entity ifixthat:partOf ?item .',
                 f'COUNT(?item) >= {item_count}'))
            
    # Part count filter
    part_count = request.args.get('partCount')
    if (part_count):
        if (rdf_type == 'ifixthat:Item'):
            count_filters.append(
                ('(COUNT(?part) AS ?partCount)',
                 '?part ifixthat:partOf ?entity .',
                 f'COUNT(?part) >= {part_count}'))
            
    # Tool count filter     
    tool_count = request.args.get('toolCount')
    if (tool_count):
        if (rdf_type == 'ifixthat:Procedure'):
            count_filters.append(
                ('(COUNT(?tool) AS ?toolCount)',
                 '?entity ifixthat:requiresTool ?tool .',
                 f'COUNT(?tool) >= {tool_count}'))
            
    select_clause = ' '.join([count_filter[0] for count_filter in count_filters])
    where_clause = '\n'.join([count_filter[1] for count_filter in count_filters])
    having_clause = ' && '.join([count_filter[2] for count_filter in count_filters])
    if (having_clause != ''):
        having_clause = f'HAVING({having_clause})'

    print(select_clause)
    print(where_clause)
    print(having_clause)

    # Query
    query = f"""
        PREFIX ifixthat: <http://ifixthat.org/>
        SELECT DISTINCT ?entity {select_clause}
        WHERE {{
            ?entity rdf:type {rdf_type} .
            ?entity rdfs:label ?label .
            {where_clause}
            FILTER REGEX(?label, "{search}", "i")
        }}
        GROUP BY ?entity
        {having_clause}
        LIMIT {pageSize} OFFSET {(page - 1) * pageSize}
    """

    results = []
    for row in default_world.sparql(query):
        results.append(Link(row[0]))

    return render_template('search.html', results=results)

