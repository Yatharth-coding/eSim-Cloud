"""
chatbotAPI/services/context.py

Placeholder for context-building utilities. Will be used to gather
relevant schematic/simulation data before sending it to the LLM.
"""


def build_context(request_data):
    """
    Build a context dictionary from the incoming chat request data.

    Parameters
    ----------
    request_data : dict
        The raw request payload from the chat endpoint.

    Returns
    -------
    dict
        A context dictionary to pass to the LLM client.

    Notes
    -----
    Stub only — returns an empty dict today. Will be expanded to pull
    schematic metadata, simulation history, and error logs when the
    chat endpoint is fully implemented.
    """
    return {}
