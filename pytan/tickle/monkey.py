'''Overload Tanium NG classes with utility methods from tickle.tools.'''
import pytan


def to_xml(self, **kwargs):
    """Deserialize self ``obj`` into an XML body, relies on tickle"""
    result = pytan.tickle.tools.to_xml(self, **kwargs)
    return result


def to_dict(self, **kwargs):
    """Deserialize self ``obj`` into a dict, relies on tickle"""
    result = pytan.tickle.tools.to_dict(self, **kwargs)
    return result


def to_json(self, **kwargs):
    """Deserialize self ``obj`` into a JSON string, relies on tickle"""
    result = pytan.tickle.tools.to_json(self, **kwargs)
    return result


def to_csv(self, **kwargs):
    """Deserialize self ``obj`` into a CSV string, relies on tickle"""
    result = pytan.tickle.tools.to_csv(self, **kwargs)
    return result


def result_to_csv(self, **kwargs):
    """Deserialize self ``obj`` into a CSV string, relies on tickle"""
    result = pytan.tickle.tools.result_to_csv(self, **kwargs)
    return result


def result_to_json(self, **kwargs):
    """Deserialize self ``obj`` into a JSON string, relies on tickle"""
    result = pytan.tickle.tools.result_to_json(self, **kwargs)
    return result


def result_to_dicts(self, **kwargs):
    """Deserialize self ``obj`` into a list of dicts, relies on tickle"""
    result = pytan.tickle.tools.result_to_dicts(self, **kwargs)
    return result


pytan.tanium_ng.BaseType.to_xml = to_xml
pytan.tanium_ng.BaseType.to_dict = to_dict
pytan.tanium_ng.BaseType.to_json = to_json
pytan.tanium_ng.BaseType.to_csv = to_csv

pytan.tanium_ng.ResultSetList.result_to_csv = result_to_csv
pytan.tanium_ng.ResultSetList.result_to_json = result_to_json
pytan.tanium_ng.ResultSetList.result_to_dicts = result_to_dicts
