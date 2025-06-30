class defer:
  def __init__(self, resource, close_method='close'):
    self.resource = resource
    self.close_method = close_method

  def __enter__(self):
    return self.resource

  def __exit__(self, *exc):
    getattr(self.resource, self.close_method)()