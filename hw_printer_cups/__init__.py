# License MIT (https://opensource.org/licenses/MIT).

from . import escpos

def post_load():
    from . import controllers
