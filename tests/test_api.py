# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import pytest
from gusregon import GUS
from vcr import VCR


vcr = VCR(path_transformer=VCR.ensure_suffix('.yaml'),
          cassette_library_dir=os.path.join('tests', 'cassettes'))


@pytest.fixture
def client():
    return GUS(sandbox=True)


def test_required_api_key():
    with pytest.raises(AttributeError):
        GUS()


@vcr.use_cassette
def test_get_sid():
    gus = GUS(sandbox=True)
    assert gus.sid is not None


@pytest.mark.parametrize('kwargs', [{'nip': '5170359458'}, {'regon': '180853177'}])
@vcr.use_cassette
def test_get_company_type_p_address(client, kwargs):
    data = client.get_address(**kwargs)
    assert 'ASSECO' in data['name']
    assert data['street_address'] == 'ul. Test-Krucza 14'
    assert data['postal_code'] == '35-322'
    assert data['city'] == 'Rzeszów'


@pytest.mark.parametrize('kwargs', [{'nip': '8991051697'}, {'regon': '022225213'}])
@vcr.use_cassette
def test_get_company_type_f_address(client, kwargs):
    data = client.get_address(**kwargs)
    assert 'MECHANIKA POJAZDOWA' in data['name']
    assert data['street_address'] == 'ul. Test-Krucza 24'
    assert data['postal_code'] == '50-502'
    assert data['city'] == 'Wrocław'


@pytest.mark.parametrize('kwargs', [{'nip': '5170359458'}, {'regon': '180853177'}])
@vcr.use_cassette
def test_get_company_type_p_details(client, kwargs):
    data = client.search(**kwargs)
    assert 'ASSECO' in data['nazwa']
    assert data['adsiedzulica_nazwa'] == 'ul. Test-Krucza'
    assert data['adsiedznumernieruchomosci'] == '14'
    assert data['adsiedzkodpocztowy'] == '35322'
    assert data['adsiedzmiejscowosc_nazwa'] == 'Rzeszów'
    assert data['podstawowaformaprawna_nazwa'] == 'OSOBA PRAWNA'


@pytest.mark.parametrize('kwargs', [{'nip': '8991051697'}, {'regon': '022225213'}])
@vcr.use_cassette
def test_get_company_type_f_details(client, kwargs):
    data = client.search(**kwargs)
    assert 'MECHANIKA POJAZDOWA' in data['nazwa']
    assert data['adsiedzulica_nazwa'] == 'ul. Test-Krucza'
    assert data['adsiedznumernieruchomosci'] == '24'
    assert data['adsiedzkodpocztowy'] == '50502'
    assert data['adsiedzmiejscowosc_nazwa'] == 'Wrocław'
