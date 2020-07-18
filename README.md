# inventory
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e44415220d504cb7a495a6b56e22572b)](https://app.codacy.com/manual/cblack34/inventory?utm_source=github.com&utm_medium=referral&utm_content=cblack34/inventory&utm_campaign=Badge_Grade_Dashboard)
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
