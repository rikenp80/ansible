#!/usr/bin/python3
import json
import mysql.connector
from getpass import getpass
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--list", action="store_true", dest="all", default=True)
parser.add_option("--host", action="store", type="string", dest="single")

(options, args) = parser.parse_args()

#p = getpass("Enter password:")

cnx = mysql.connector.connect(
    user='dbadmin',
    password='1L@rg3B!ll$',
    host='10.105.136.107',
    database='dbadmin'
)

cursor = cnx.cursor()

if options.all and not options.single:

    query = ("""select a.ip, c.var, c.value from serverlist_serverslist a 
                  inner join serverlist_serverslist_groups b
                    on a.id=b.serverslist_id
                  inner join serverlist_grouphostsvars c
                    on b.groups_id=c.groupid_id
                UNION ALL 
                select a.ip, b.var, b.value from serverlist_serverslist a 
                  inner join serverlist_singlehostsvars b
                     on a.id=b.serverid_id;""")

    cursor.execute(query)

    jsonvar = {"_meta": {}}

    jsonvar["_meta"]["hostvars"] = {}

    for (ip, var, value) in cursor:
        if ip not in jsonvar["_meta"]["hostvars"]:
            jsonvar["_meta"]["hostvars"][ip] = {}
        jsonvar["_meta"]["hostvars"][ip][var] = value

    cursor.close()

    cursor = cnx.cursor()
    query = """select a.ip, IFNULL(c.groupName,'ungrouped')
                 from serverlist_serverslist as a
                   Left join serverlist_serverslist_groups as b
                     on a.id=b.serverslist_id
                   LEFT join serverlist_groups as c
                     on b.groups_id=c.id;"""
    cursor.execute(query)

    groups = []

    jsonvar["all"] = {}

    for ip, groupName in cursor:
        if "ungrouped" not in groups:
            groups.append("ungrouped")
        if groupName not in groups:
            groups.append(groupName)
        if "ungrouped" not in jsonvar:
            jsonvar["ungrouped"] = {}
        if "hosts" not in jsonvar["ungrouped"]:
            jsonvar["ungrouped"]["hosts"] = []
        if groupName not in jsonvar:
            jsonvar[groupName] = {}
        if "hosts" not in jsonvar[groupName]:
            jsonvar[groupName]["hosts"] = []
        jsonvar[groupName]["hosts"].append(ip)

    cursor.close()

    jsonvar["all"]["children"] = groups

    results = json.dumps(jsonvar, indent=4, separators=(',', ': '))
    sys.stdout.write(str(results))
    sys.stdout.flush()
elif options.single:
    query = """select a.ip, c.var,c.value
                 from serverlist_serverslist as a
                  inner join serverlist_serverslist_groups b
                    on a.id=b.serverslist_id
                  inner join serverlist_grouphostsvars c
                    on b.groups_id=c.groupid_id
                 where ip = '{0}'
               UNION ALL 
               select a.ip, b.var, b.value from serverlist_serverslist a 
                 inner join serverlist_singlehostsvars b
                   on a.id=b.serverid_id
                 where ip = '{0}';""".format(options.single)
    cursor.execute(query)
    jsonvar = {}
    for _, var, value in cursor:
        jsonvar[var] = value
    json.dumps(jsonvar)
else:
    print("no options selected")
