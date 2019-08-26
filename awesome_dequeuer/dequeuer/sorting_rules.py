def default_sorting_rule(agent):
    primary_skillset = agent["primary_skillset"]
    secondary_skillset = agent["secondary_skillset"]
    return lambda job: (
        not job["type"] in primary_skillset,
        not job["type"] in secondary_skillset,
        not job["urgent"],
    )
