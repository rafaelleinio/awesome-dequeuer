# awesome-dequeuer
Welcome to my solution to the job queues problem from Nubank!
Before we start to talk about the solution I just wanted to say that it was quite a challenge but in the end I could learn new things and it was fun.

## Introduction
The main problem here was to implement a dequeuer function that giving a set of agents, jobs and job_request the program should produce a set of job_assignments (assign a job to agent).
According to the description this program need to follow the following rules:

- You can assume the list of jobs passed in is ordered by the time that they have entered the system.
- Jobs that arrived first should be assigned first, unless it has a "urgent" flag, in which case it has a higher priority.
- A job cannot be assigned to more than one agent at a time.
- An agent is not handed a job whose type is not among its skill sets.
- An agent only receives a job whose type is contained among its secondary skill set if no job from its primary skill set is available.

Among these rules I assume some other observations that maybe is implied:
- An agent can ask more than one job
- A job_request has always a valid `agent_id`
- If there is a normal job that fits a agents primary skills and and a second job that is urgent but fits only the secondary skills of this agent, the first one will be assigned to this agent.
- In a case where there is no job_requests the output is empty: `[]`
- In a case where no job_request match is possible the output is empty `[]`

## How to run
The code itself use pure Python 3.6 so there is no other requirements for running the code. But if you want to perform the unit tests (with a set of sample inputs and outputs) `pytest` is needed, so just hit `pip3 install pytest` in your terminal.

To run a python job that performs the expected behaviour described in the problem (reading from stdind and printing the result in the stdout), just run from the root of the repository:
```bash
 python awesome_dequeuer/jobs/sample_job.py
```
You will be asked to paste the input json content, with a final blank line the script will execute and the output will be printed

To run the unit tests running all the sample data under `tests/tests_data/` just run from the root of the repository:
```bash
pytest tests/
```

## Code Explain
I tried to make the code very modular and flexible for future changes and tests. So there is the core business class `Dequeuer` that contains all the business logic to solve the problem. But I did not fixed many rules, so the code can experiment later other job filtering and sorting rules for example.

So the code is all modular with all these blocks being used to compose the logic of the python job that will in fact perform the extract, transform and load in the data.  

### dequeuer/extractors
Here I implemented functions to extract the json content from some source and return this data as a dictionary in Python.
- **stdin_extractor**:
This extractor reads the data from stdin, I used this extractor in the sample_job as it was a requirement for the solution

- **file_extractor**:
This one reads the data from a file, just need to pass the file of the input json in the function.

\* Extractors are a good approach since we could later implement extractors for getting data from databases and APIs for example. So the logic to solve the problem is not fixed to the source of the data.

### dequeuer/filter_rules
Here is implemented the rules for filtering the jobs list. So for a job_request the system needs to know what jobs an agent is able to do.

- **default_filter_rule**: Here is implemented the rule described in the problem, an agent is only allowed to get jobs that are in his primary or secondary skillset

\* This is a good modularization because later we could implement other rules for filtering the jobs based on other attributes of the agent for example. Or the schema of the data can change so is easy to just adjust the code in this module, in the business class there is no reference from "primary" or "secondary skillset". 

### dequeuer/sorting_rules
Here is implemented the rules for sorting the jobs. So for a set of jobs that an agent can do the system needs to know which job has more priority.
- **default_sorting_rule**: Here is implemented the rule described in the problem, the priority needs to be a job that fits in the primary skills of an agent over a job that only fits in the secondary skills, and urgent tasks first. So just summarizing: urgent primary skills jobs, normal primary skills jobs, urgent secondary skills jobs and normal secondary skills jobs in this following order.

\* So here is the same justification as I wrote in the extractors subtopic, we could easily implement other sorting rules without changing anything in other parts of the code. 

### dequeuer/dequeuer
So here is finally implemented the business class **Dequeuer** that contains the main logic to solve the problem.
The constructor of this class needs a sorting rule and a filter rule. So you just need to chose one for each of those rules in the related modules to create a dequeuer object.

So the problem can be solved by calling 2 functions of this class in sequence:
- **queue_partitioner**: giving the json data input as a python dictionary this function will partition the data in agents, jobs and jobs_requests

- **job_assigner**: giving the agents, jobs and job_requests this function will produce the expected output of job assignments. For each job_requests that function get the agent that is requesting the job and search for the best job based on defined rules (`find_job` function). If no job could be found, there is no assignment.

Another important function to explain is the `find_job` function. Giving an agent, the jobs list, the job request and the list of job assignments this function will return one or an empty job assignment. First the function just create the `sorting_rule` and the `filter_rule` passing the `agent` to the functions that create these rules. Than from the jobs list is filtered only the jobs that this agent can do (with the `filtering_rule`), than these `doable_jobs` are sorted with the `sorting_rule` to put the most relevant jobs at the beginning. Than the function construct the `job_assigned` json schema if the job is not already assigned (this information is in `job_assignments` that was passed to the function).

### dequeuer/loaders
Here is implemented the functions that giving data in python dictionaries it will load this data as json to some data sink.

- **stdout_loader**: this functions just prints the json in the stdout. That was required in the problem description.

\* Here again, like all the other modules we have the facility to implement new loaders because we may need these results in a database or in a datalake for example.

### jobs
In the jobs folder we can put all that the python scripts that will in fact use all this code architecture and will run what we expect.
So here is just implemented on `sample_job.py` that has the desire behaviour described in the problem for getting the data in the stdin and than just print the result in the stdout.

You can see that the structure of a job if very simple. We just import from awesome_dequeuer everything we will use and just build the pipeline. In the case of the sample_job he gets a `default_filter_rule` and the `default_sorting_rule` to create the Dequeuer object with these rules. Then he uses the `stdin_extractor` to get the data, process this data with the 2 steps from Dequeuer class that I explained above and finally dump the results with the `stdout_loader`.
