import config
import json
import collections

def get_feature_names(file_id):
    json_file_path='{}{}.json'.format(config.dir_path, file_id)
    with open(json_file_path) as json_data:
        try:
            json_file = json.load(json_data)
        except:
            return 'Could not read json file'
    c = collections.Counter()
    if 'features' in json_file:
        for item in json_file['features']:
            c[item['geometry']['type']]+=1
            result =  dict(c)
            with open('{}outfile{}.json'.format(config.dir_path, file_id), 'w') as outfile:
                    json.dump(result, outfile)
        if len(result) > 0:
            return result
        else: return 'File does not contain features'
    else:
        return 'File does not contain field "features"'

get_feature_names('BQADAgADAwIAAkd2UEuSxhiOG-5p0wI')
