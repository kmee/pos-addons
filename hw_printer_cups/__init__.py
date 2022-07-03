# Copyright 2022 Luis Felipe Mileo <mileo@kmee.com.br>
# License MIT (https://opensource.org/licenses/MIT).

from . import escpos

def post_load():
    from . import controllers
