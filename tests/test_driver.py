"""Unit tests for volttron-lib-fake-driver"""

from volttron.driver.interfaces.fake.fake import BaseInterface, Fake


def test_driver():
    driver = Fake()
    assert isinstance(driver, BaseInterface)
