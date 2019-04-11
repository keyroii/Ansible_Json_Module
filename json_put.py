#!/usr/bin/python
#
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: json_put

short_description: A small json module

version_added: "1.0"

description:
    - "A little json module to update / add entrys in json files"

author:
    - Kevin-Marvin Müller (@keyroii)
'''

EXAMPLES = '''
# pass in a message and have changed true
- name: Test with a message and changed output
  json_put:
    path: "PATH/TO/JSON"
    content: {
        "valueToChange":"this is the new value",
        "valuetoadd":{
          "this":"is",
          "a":"added",
          "dict":{
            "example":"exampleValue"
          }
        }
      }

# fail the module
- name: Test failure of the module
  json_put:
    name: fail me
    path: "INVALID_PATH"
'''


from ansible.module_utils.basic import *
import sys
import json
import collections


def openJson(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        json_file.close()
    return data


def editData(jsonData, newData):
    for key, value in newData.items():
        if isinstance(value, collections.Mapping):
            jsonData[key] = editData(jsonData.get(key, {}), value)
        else:
            jsonData[key] = value
    return jsonData


def saveNewJson(path, data):
    with open(path, 'w+') as output_file:
        json.dump(data, output_file, sort_keys=True, indent=4)
        output_file.close()


def putDict(path, data):
    dictData = openJson(path)
    dictData = editData(jsonData=dictData, newData=data)
    saveNewJson(path=path, data=dictData)
    return dictData


def main():
    module = AnsibleModule(argument_spec={
        "path":{"required":True,"type":"str"},
        "content":{"type":"dict"}
    },
    supports_check_mode=False)

    resultingJson = putDict(path=module.params['path'], data=module.params['content'])

    module.exit_json(changed=True, new_json=resultingJson)

if __name__ == '__main__':
    main()