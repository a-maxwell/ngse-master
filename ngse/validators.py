from utils import decode
from pyramid.httpexceptions import (
	HTTPNoContent,
	HTTPBadRequest,
	HTTPUnauthorized,
	HTTPForbidden,
)

def has_admin_rights(request, **kwargs):
	token = request.authorization[1]
	payload = decode(token)

	if payload['level'] != 1:
		raise HTTPForbidden

def has_representative_rights(request, **kwargs):
	token = request.authorization[1]
	payload = decode(token)

	if payload['level'] != 2:
		raise HTTPForbidden

def has_recommender_rights(request, **kwargs):
	token = request.authorization[1]
	payload = decode(token)

	if payload['level'] != 3:
		raise HTTPForbidden

def has_applicant_rights(request, **kwargs):
	token = request.authorization[1]
	payload = decode(token)

	if payload['level'] != 4 and payload['level'] != 5:
		raise HTTPForbidden

def has_form(request, **kwargs):
	token = request.authorization[1]
	payload = decode(token)

	if not payload['level'] in [3,4,5]:
		raise HTTPNoContent

def has_token(request, **kwargs):
	if request.authorization is None:
		raise HTTPUnauthorized

def has_user_id(request, **kwargs):
	if request.params.get('user_id', None) is None:
		raise HTTPBadRequest

def has_form_id(request, **kwargs):
	print request.params
	if request.params.get('form_id', None) is None:
		raise HTTPBadRequest

def has_category_id(request, **kwargs):
	if request.params.get('category_id', None) is None:
		raise HTTPBadRequest

def has_question_id(request, **kwargs):
	if request.params.get('question_id', None) is None:
		raise HTTPBadRequest

def has_answer_id(request, **kwargs):
	if request.params.get('answer_id', None) is None:
		raise HTTPBadRequest