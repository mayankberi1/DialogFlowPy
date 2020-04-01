class Payload(dict):

    def __init__(self, payload_type: str = 'google', payload: dict = None) -> None:
        super().__init__()
        if payload is None:
            payload = dict()

        self[payload_type] = payload

    @property
    def payload(self):
        # return the value of the self dictionary
        for item in self.values():
            return item

    @payload.setter
    def payload(self, payload: dict):
        for key in self:
            self[key] = payload
