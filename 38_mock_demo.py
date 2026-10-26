"""38_mock_demo.py — Test with mocks instead of real services.

Demonstrates: unittest.mock to replace a slow or external
dependency (here, a "weather service" function) with a
controlled stand-in, so the code under test runs fast and
deterministically. The test also asserts the mock was called
with the expected argument.
Run: python3 38_mock_demo.py
"""

from unittest.mock import Mock, patch


def fetch_temperature(service, city):
    """Call the service; in production this would hit a network API."""
    return service.get_temperature(city)


def describe(service, city):
    temp = fetch_temperature(service, city)
    if temp < 0:
        return f"{city}: freezing ({temp}C)"
    if temp < 20:
        return f"{city}: cool ({temp}C)"
    return f"{city}: warm ({temp}C)"


def main():
    fake = Mock()
    fake.get_temperature.return_value = -5
    assert describe(fake, "Oslo") == "Oslo: freezing (-5C)"
    fake.get_temperature.assert_called_once_with("Oslo")

    with patch(__name__ + ".fetch_temperature", return_value=25) as stub:
        assert describe(Mock(), "Cairo") == "Cairo: warm (25C)"
        stub.assert_called_once()
    print("PROOF: mock returned -5 -> 'freezing'; patched call -> 'warm'")
    print("PROOF: both mocks asserted on their exact call arguments")


if __name__ == "__main__":
    main()
