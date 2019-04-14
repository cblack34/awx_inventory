# inventory
[![Build Status](https://travis-ci.org/cblack34/inventory.svg?branch=master)](https://travis-ci.org/cblack34/inventory)
Build inventories of computers that can be grouped. Mainly for use with awx/ansible dynamic inventory.


What the json should look like for ansible:
```json
{
  "_meta": {
    "hostvars": {
        "host1": {
            "var2": "val2"
        }
    }
  },
  
  "group1": {
    "hosts": [
      "host1"
    ],
    
    "vars": {
        "var1": "val1"
    }
  }
}
```