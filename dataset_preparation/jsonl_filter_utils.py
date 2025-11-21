import json 

def read_jsonl_file(jsonl_filename):
    """
    Reads a JSONL file and returns a list of JSON objects.
    """
    data = []
    with open(jsonl_filename, 'r') as f:
        for line in f:
            entry = json.loads(line)
            data.append(entry)
    return data

def is_predicate_satisfied(metadata, predicate):
    field, expression = next(iter(predicate.items()))
    operator, predicate_value = next(iter(expression.items()))
    metadata_value = metadata[field]

    if operator == '$eq':
        if metadata_value != predicate_value:
            return False
    elif operator == '$ne':
        if metadata_value == predicate_value:
            return False
    elif operator == '$lt':
        if metadata_value >= predicate_value:
            return False
    elif operator == '$lte':
        if metadata_value > predicate_value:
            return False
    elif operator == '$gt':
        if metadata_value <= predicate_value:
            return False
    elif operator == '$gte':
        if metadata_value < predicate_value:
            return False
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    return True

# Computes whether a given metadata string satisfies the given filter condition
def is_match(metadata, query_filter):
    match = True
    if '$and' in query_filter['filter']:
        for cond in query_filter['filter']['$and']:
            match = match and is_predicate_satisfied(metadata, cond)
    else: 
        match = match and is_predicate_satisfied(metadata, query_filter['filter'])
    return match 

# Example usage from files in the caselaw dataset release:

# metadata_file = "caselaw_base_metadata.jsonl"
# query_filter_file = "caselaw_query_filters.jsonl"

# base_metadata = read_jsonl_file(metadata_file)
# query_filters = read_jsonl_file(query_filter_file)

# match_0_0 = is_match(base_metadata[0], query_filters[0])