import pytest
from syntax_practice import safe_div, slugify, median


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # normal cases
        (10, 2, 5.00),
        (199, 4, 49.750),
        (50.4, 2, 25.200),
        (100, 3, 33.333),
        (780.58, 3, 260.193),
        # Max bound
        (100000000000000, 765432, 130645178.148),
        # Low bound
        (3, 1000000000000, 0.000),
        (3, 100, 0.030),
        # Invalid
        (5, 0, None),
        # Negative
        (-9, 3, -3),
        (9, -3, -3),
        (-50.4, 2, -25.200),
        (-50, -10, 5),
    ],
)
def test_safe_div(a, b, expected):
    "Testing safe_div:"
    assert safe_div(a, b) == expected


@pytest.mark.parametrize(
    "a, expected",
    [
        # normal cases
        ("hello world", "hello-world"),
        ("  hi, there  ", "hi-there"),
        ("Programming", "programming"),
        ("New-Tutorials", "new-tutorials"),
        ("change # ! ) % # > comin@g", "change-coming"),
        # large string
        (
            "This is a very large string with $ many of this numbers as well 0123456789 also punctuations$$$$$, WHAT else is there to give                                                 , ok many and m@ny of the spaces and now punctuations coming !@#$%^&*()_+{[}]| ok ending     ",
            "this-is-a-very-large-string-with-many-of-this-numbers-as-well-0123456789-also-punctuations-what-else-is-there-to-give-ok-many-and-mny-of-the-spaces-and-now-punctuations-coming-ok-ending",
        ),
        # edge cases
        ("abc&d \%\% p", "abcd-p"),
        ("Hello   &&**&  ---  &&&&  world! ", "hello-----world"),
    ],
)
def test_slugify(a, expected):
    "Testing slugify:"
    assert slugify(a) == expected


@pytest.mark.parametrize(
    "a, expected",
    [
        # Happy Path
        ([3, 1, 4, 1, 5], 3),
        ([3, 1, 4, 1, 5, 9], 3.5),
        # Edge Case
        ([10], 10),
        ([1, 5, 2, 5, 1], 2),
        ([-5, -1, -10, -2, -8], -5),
        ([-1, 1, -2, 2, 0], 0),
        ([1.5, 2.5, 0.5, 3.5], 2.0),
        ([10, 20, 30, 40, 50], 30),
        # Max bound
        ([1e9, 5e9, 2e9], 2e9),
        # Lower bound
        ([0.0001, 0.0003, 0.0002], 0.0002),
        # large dataset
        (list(range(1000001)), 500000),
    ],
)
def test_median(a, expected):
    "Testing median:"
    assert median(a) == expected


def test_median_empty_list_raises_error():
    "Test median with empty list"
    with pytest.raises(ValueError, match="The list is Empty"):
        median([])
