import requests
from requests.exceptions import HTTPError
api_host_url='https://developers.rockethealth.africa/api/interview'
payload = {
    'api_user':7373902
}

def get_dataset3():
    try:
        resp = requests.get(api_host_url+'/api-token', params=payload)
        resp.raise_for_status()
    except HTTPError as http_err:
        return {'success': False, 'message': str(http_err)}
    except Exception as err:
        return {'success': False, 'message': str(err)}

    resp_data=resp.json()
    headers = {
        'Authorization': 'Bearer ' +resp_data['data']['auth_token']
    }

    try:
        resp = requests.post(api_host_url + '/employees-blog-actions', data=payload, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        return {'success': False, 'message': str(http_err)}
    except Exception as err:
        return {'success': False, 'message': str(err)}

    resp_data=resp.json()
    return resp_data['data']
