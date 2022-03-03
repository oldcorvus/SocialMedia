from kavenegar import *

import string

from random import randint

from django.utils.crypto import get_random_string

def get_random_str(min_length: int, max_length: int) -> str:
    """
    This simple function return random character with your min length
    and max length with ascii letters
    """
    alph_l = string.ascii_letters
    random_length = randint(min_length, max_length)
    random_string = get_random_string(random_length, alph_l)
    return random_string

def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI('kooft')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f'{code} کد تایید شما '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)
