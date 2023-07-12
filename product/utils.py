def comparison_of_expected_and_result(httpstatus, response_status, expected_result, response_result):
    assert httpstatus == response_status
    assert expected_result == response_result
