from parma_analytics.reporting.notification_rule_helper import compare_to_threshold


# Test case for values below the threshold
def test_compare_to_threshold_below_threshold():
    previous_value = 100.0
    new_value = 105.0
    threshold = 10.0
    result = compare_to_threshold(previous_value, new_value, threshold)
    expected_result = -1
    assert result == expected_result


# Test case for values above the threshold
def test_compare_to_threshold_above_threshold():
    previous_value = 100.0
    new_value = 120.0
    threshold = 10.0
    result = compare_to_threshold(previous_value, new_value, threshold)
    expected_result = 20.0
    assert result == expected_result


# Test case for values equal to the threshold
def test_compare_to_threshold_equal_to_threshold():
    previous_value = 100.0
    new_value = 110.0
    threshold = 10.0
    result = compare_to_threshold(previous_value, new_value, threshold)
    expected_result = 10.0
    assert result == expected_result


# Test case for integer values
def test_compare_to_threshold_integer_values():
    previous_value = 10
    new_value = 12
    threshold = 10
    result = compare_to_threshold(previous_value, new_value, threshold)
    expected_result = 20.0
    assert result == expected_result


# Test case for zero threshold
def test_compare_to_threshold_zero_threshold():
    previous_value = 100.0
    new_value = 105.0
    threshold = 0.0
    result = compare_to_threshold(previous_value, new_value, threshold)
    expected_result = 5.0
    assert result == expected_result
