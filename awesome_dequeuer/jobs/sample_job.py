from awesome_dequeuer.dequeuer import Dequeuer
from awesome_dequeuer.dequeuer.filter_rules import default_filter_rule
from awesome_dequeuer.dequeuer.sorting_rules import default_sorting_rule
from awesome_dequeuer.dequeuer.extractors import stdin_extractor
from awesome_dequeuer.dequeuer.loaders import stdout_loader

dequeuer = Dequeuer(default_filter_rule, default_sorting_rule)

if __name__ == "__main__":
    # extract data
    raw_data = stdin_extractor()

    # transform the data
    agents, jobs, job_requests = dequeuer.queue_partitioner(raw_data)
    job_assignements = dequeuer.job_assigner(agents, jobs, job_requests)

    # load the data
    stdout_loader(job_assignements)
