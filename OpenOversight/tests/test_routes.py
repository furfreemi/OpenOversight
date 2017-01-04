# Routing and view tests
import pytest
from flask import url_for, current_app
from OpenOversight.app.main.forms import FindOfficerForm, FindOfficerIDForm
from urlparse import urlparse


@pytest.mark.parametrize("route", [
    ('/'),
    ('/index'),
    ('/find'),
    ('/about'),
    ('/contact'),
    ('/privacy'),
    ('/label'),
    ('/auth/login'),
    ('/auth/register'),
    ('/auth/reset')
])
def test_routes_ok(route, client):
    rv = client.get(route)
    assert rv.status_code == 200


# All login_required views should redirect if there is no user logged in
@pytest.mark.parametrize("route", [
    ('/auth/unconfirmed'),
    ('/auth/logout'),
    ('/auth/confirm/abcd1234'),
    ('/auth/confirm'),
    ('/auth/change-password'),
    ('/auth/change-email'),
    ('/auth/change-email/abcd1234')
])
def test_route_login_required(route, client):
    rv = client.get(route)
    assert rv.status_code == 302

#
# def test_find_form_submission(client, mockdata):
#     with current_app.test_request_context():
#         form = FindOfficerForm()
#         assert form.validate() == True
#         rv = client.post(url_for('main.get_officer'), data=form.data, follow_redirects=False)
#         assert rv.status_code == 307
#         assert urlparse(rv.location).path == '/gallery'
#
#
# def test_bad_form(client, mockdata):
#     with current_app.test_request_context():
#         form = FindOfficerForm(dept='')
#         assert form.validate() == False
#         rv = client.post(url_for('main.get_officer'), data=form.data, follow_redirects=False)
#         assert rv.status_code == 307
#         assert urlparse(rv.location).path == '/find'
#
#
# def test_find_form_redirect_submission(client, session):
#     with current_app.test_request_context():
#         form = FindOfficerForm()
#         assert form.validate() == True
#         rv = client.post(url_for('main.get_officer'), data=form.data, follow_redirects=False)
#         assert rv.status_code == 200


def test_tagger_lookup(client, session):
    with current_app.test_request_context():
        form = FindOfficerIDForm()
        assert form.validate() == True
        rv = client.post(url_for('main.label_data'), data=form.data, follow_redirects=False)
        assert rv.status_code == 307
        assert urlparse(rv.location).path == '/tagger_gallery'


def test_tagger_gallery(client, session):
    with current_app.test_request_context():
        form = FindOfficerIDForm()
        assert form.validate() == True
        rv = client.post(url_for('main.get_tagger_gallery'), data=form.data)
        assert rv.status_code == 200


def test_tagger_gallery_bad_form(client, session):
    with current_app.test_request_context():
        form = FindOfficerIDForm(dept='')
        assert form.validate() == False
        rv = client.post(url_for('main.get_tagger_gallery'), data=form.data, follow_redirects=False)
        assert rv.status_code == 307
        assert urlparse(rv.location).path == '/label'