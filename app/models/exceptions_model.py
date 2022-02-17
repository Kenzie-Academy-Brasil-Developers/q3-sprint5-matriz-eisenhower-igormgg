class Eisenhower_Error(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = 400

    @staticmethod
    def eisenhower_err_description(importance, urgency):
        return {
            'msg': {
                "valid_options": {
                    "importance": [1, 2],
                    "urgency": [1, 2]
                },
                "received_options": {
                    "importance": f"{importance}",
                    "urgency": f"{urgency}"
                }
            }
        }