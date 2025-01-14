def parse_request(req):
    """Parse and validate the incoming request."""
    try:
        data = req.get_json(force=True)
        return data.get('question', '').strip()
    except Exception:
        return None
