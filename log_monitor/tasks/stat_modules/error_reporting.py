from typing import List, Tuple, Callable
from log_monitor.models import LogEntry


def _is_client_error(entry: LogEntry) -> bool:
    """
    Checks if the request resulted in a client error (4xx status code)
    :param entry: log entry
    :return: True if user error
    """
    return entry.status // 100 == 4


def _is_server_error(entry: LogEntry) -> bool:
    """
    Checks if the request resulted in a server error (5xx status code)
    :param entry: log entry
    :return: True if server error
    """
    return entry.status // 100 == 5


def _get_error_stats(entries: List[LogEntry], error_type_func: Callable[[LogEntry], bool]) -> Tuple[int, int]:
    """
    Computes stats on  errors, returning the number and % of requests resulting in the specified kind of error
    :param entries: list of entries
    :param error_type_func: function that selects type of error
    :return: (number of errors, % of errors rounded down)
    """
    if not entries:
        return 0, 0
    n_errors = 0
    for entry in entries:
        if error_type_func(entry):
            n_errors += 1
    return n_errors, n_errors * 100 // len(entries)


def _get_server_error_stats(entries: List[LogEntry]) -> Tuple[int, int]:
    """
    Computes stats on server errors, returning the number and % of requests resulting in 5xx
    :param entries: list of entries
    :return: (number of errors, % of errors rounded down)
    """
    return _get_error_stats(entries, _is_server_error)


def _get_client_error_stats(entries: List[LogEntry]) -> Tuple[int, int]:
    """
    Computes stats on client errors, returning the number and % of requests resulting in 5xx
    :param entries: list of entries
    :return: (number of errors, % of errors rounded down)
    """
    return _get_error_stats(entries, _is_client_error)


def error_reporting(entries: List[LogEntry], _: float):
    n_client_error, percent_client_error = _get_client_error_stats(entries)
    n_server_error, percent_server_error = _get_server_error_stats(entries)
    n_error, percent_error = n_client_error + n_server_error, percent_client_error + percent_server_error
    if n_error > 0:
        msg = f"{n_error} errors ({percent_error}%): " + \
              f"{n_client_error} client errors ({percent_client_error}%), " + \
              f"{n_server_error} server errors ({percent_server_error}%)"
        print(msg)
