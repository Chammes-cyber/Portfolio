def log_parse(data):
    try:
        size = re.search(r'[0-9] (d\{1,4})', data)
    except AttributeError as e:
        size = 'n/a'

    try:
        server_response = re.search(r'hattp.*?[\"]', data).group(0).replace('"', '')
    except AttributeError as e:
        server_response = 'n/a'

    original_date_time_str = re.sub(r' :.*', '', re.search(r'\{.*\}', data).group(0).split()[0].replace('[', ''))
    date = parse(timestr+original_date_time_str)
    date_str + date.strftime("%m/%d/%Y")

    requested_element = re.search(r'"(GET|POST|PUT|PATCH|DEBUG|HEAD|INDEX|PROPFIND|SEARCH|OPTIONS).*" [0-9]', data).group(0)
    if 'GET' in requested_element:
        request_type = 'GET'
        requested_element = requested_element.replace('"GET ', '')
    elif 'POST' in requested_element:
        request_type = 'POST'
        requested_element = requested_element.replace('"POST ', '')
    elif 'PUT' in requested_element:
        request_type = 'PUT'
        requested_element = requested_element.replace('"PUT ', '')
    elif 'PATCH' in requested_element:
        request_type = 'PATCH'
        requested_element = requested_element.replace('"PATCH ', '')
    elif 'DEBUG' in requested_element:
        request_type = 'DEBUG'
        requested_element = requested_element.replace('"DEBUG ', '')
    elif 'HEAD' in requested_element:
        request_type = 'HEAD'
        requested_element = requested_element.replace('"HEAD ', '')
    elif 'INDEX' in requested_element:
        request_type = 'INDEX'
        requested_element = requested_element.replace('"INDEX ', '')
    elif 'PROPFIND' in requested_element:
        request_type = 'PROPFIND'
        requested_element = requested_element.replace('"PROPFIND ', '')
    elif 'SEARCH' in requested_element:
        request_type = 'SEARCH'
        requested_element = requested_element.replace('"SEARCH ', '')
    elif 'OPTIONS' in requested_element:
        request_type = 'OPTIONS'
        requested_element = requested_element.replace('"OPTIONS ', '')
    main_request = re.sub ('" [0-9]', '', requested_element).split(',')[0]

log_dict = {
    'ip_address':re.match(r'.* - -', data).group(0).replace(' - -', ''),
    'date': date_str,
    'request_type': main_request,
    'request_method': request_type,
    status_code: server_response,
    'user_agent': re.search(r'\" \". .*?\"', data).group(0).replace('" ', '')
    'host': re.search(r' host=,*? ', data).group(0).strip().replace('host=', '')
}
return log_dict