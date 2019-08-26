def default_filter_rule(agent):
    skillset = agent["primary_skillset"] + agent["secondary_skillset"]
    return lambda job: (job["type"] in skillset)
