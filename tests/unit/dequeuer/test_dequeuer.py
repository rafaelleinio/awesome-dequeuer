import os
from glob import glob

import pytest

from awesome_dequeuer.dequeuer import Dequeuer
from awesome_dequeuer.dequeuer.filter_rules import default_filter_rule
from awesome_dequeuer.dequeuer.sorting_rules import default_sorting_rule
from awesome_dequeuer.dequeuer.extractors import file_extractor

dequeuer = Dequeuer(default_filter_rule, default_sorting_rule)


def default_rules_test_cases():
    input_paths = sorted(
        glob(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../tests_data/default_rules/input/*.json",
            )
        )
    )

    output_paths = sorted(
        glob(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../tests_data/default_rules/output/*.json",
            )
        )
    )

    return list(zip(input_paths, output_paths))


class TestDequeuer:
    @pytest.mark.parametrize("input_path, output_path", default_rules_test_cases())
    def test_dequeuer_default_rules(self, input_path, output_path):
        # arrange
        raw_data = file_extractor(input_path)
        expected_result = file_extractor(output_path)

        # act
        agents, jobs, job_requests = dequeuer.queue_partitioner(raw_data)
        job_assignements = dequeuer.job_assigner(agents, jobs, job_requests)

        # assert
        print(job_assignements)
        print(expected_result)
        assert job_assignements == expected_result
