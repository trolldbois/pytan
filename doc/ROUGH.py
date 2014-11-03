self = sw

object_type = 'question'
objects_dict = {
    object_type: {
        'selects': {
            "select": [
                {
                    "sensor": {"name": "Computer Name"},
                },
            ],
        },
    },
}

request_args = {
    'command': 'AddObject',
    'object_type': object_type,
    'objects_dict': objects_dict,
    'auth_dict': self.auth.token,
}

request = SoapRequest(**request_args)
response = self.call_api(request)
