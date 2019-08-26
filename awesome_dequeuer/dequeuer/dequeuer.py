class Dequeuer:
    def __init__(self, filter_rule, sorting_rule):
        self.filter_rule = filter_rule
        self.sorting_rule = sorting_rule

    def queue_partitioner(self, json_dict):
        agents = {}
        jobs = []
        job_requests = []
        for element in json_dict:
            if element and isinstance(element, dict):
                key = list(element.keys())[0]
                if key == "new_agent":
                    agents[element[key]["id"]] = {
                        k: v for k, v in element[key].items() if k != "id"
                    }
                elif key == "new_job":
                    jobs.append(element[key])
                elif key == "job_request":
                    job_requests.append(element[key])

        return agents, jobs, job_requests

    def jobs_filter(self, jobs, filter_rule):
        return filter(filter_rule, jobs)

    def jobs_sorting(self, jobs, sorting_rule):
        return sorted(jobs, key=sorting_rule)

    def find_job(self, agent, job_request, jobs, job_assignments):
        assigned_job_ids = [a["job_assigned"]["job_id"] for a in job_assignments]
        sorting_rule = self.sorting_rule(agent)
        filter_rule = self.filter_rule(agent)

        doable_jobs = self.jobs_filter(jobs, filter_rule)
        sorted_doable_jobs = self.jobs_sorting(doable_jobs, sorting_rule)
        assignments = [
            {"job_assigned": {"job_id": x["id"], "agent_id": job_request["agent_id"]}}
            for x in sorted_doable_jobs
            if x["id"] not in assigned_job_ids
        ]
        return assignments[:1]

    def job_assigner(self, agents, jobs, job_requests):

        job_assignments = []
        for job_request in job_requests:
            agent = agents[job_request["agent_id"]]
            job_assignments += self.find_job(agent, job_request, jobs, job_assignments)
        return job_assignments
