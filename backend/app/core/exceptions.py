class GuestQuotaExceededError(Exception):
  def __init__(self) -> None:
    super().__init__("Guest request limit exceeded.")