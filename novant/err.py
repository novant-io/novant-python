#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# History:
#   9 Mar 2026  Andy Frank  Creation
#

#############################################################################
# NovantErr
#############################################################################

class NovantErr(Exception):
    """Error returned from the Novant API."""

    def __init__(self, code, body=None):
        self.code = code
        self.body = body
        if body and isinstance(body, dict):
            self.message = body.get("message", body.get("error", str(body)))
        else:
            self.message = f"HTTP {code}"
        super().__init__(self.message)
