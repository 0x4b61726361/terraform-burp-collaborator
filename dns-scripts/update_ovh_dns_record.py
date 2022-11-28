import json
import ovh
import argparse
import sys
import os 

parser = argparse.ArgumentParser(description='Provide server public IP, subdomain to create on OVH and your base domain. ')
parser.add_argument('ip_target', action='store', help='IP address for Burp Collaborator')
parser.add_argument('subdomain', action='store', help='DNS entry to create in the zone')
parser.add_argument('zone', action='store', help='Domain zone to use')
parser.add_argument('ovhini', action='store', help='Path to OVH ini file')

ovh_method = ""
if len(sys.argv)==4:
    # Do env variables to get OVH keys
    ovh_method="env"
if len(sys.argv)==5:
    # Do OVH ini to get OVH keys
    ovh_method = "file"
else:
    parser.print_help()
    sys.exit(1)

options = parser.parse_args()
target_ip = options.ip_target
zone = options.zone
subdomain = options.subdomain
ovhini = options.ovhini
ns_servers = ['ns1']
a_records = ['ns1.'+subdomain, subdomain]

if ovh_method == "env":
    # Build OVH Client from env variables
    try:
        client = ovh.Client(
                endpoint=os.environ['OVH_ENDPOINT'],    # OVH Endpoint
                application_key=os.environ['OVH_APP_KEY'],    # Application Key
                application_secret=os.environ['OVH_APP_SECRET'], # Application Secret
                consumer_key=os.environ['OVH_CONSUMER_KEY'],       # Consumer Key
        )
    except KeyError:
        print('Aborting! Environement Varaibles not found!')
        exit(0)
elif ovh_method == "file":
    # Build OVH Client from OVH ini file
    ovhkeys = {}
    with open(ovhini) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            ovhkeys[name.strip()] = var.strip()
    try:
        client = ovh.Client(
                endpoint=ovhkeys['dns_ovh_endpoint'],    # OVH Endpoint
                application_key=ovhkeys['dns_ovh_application_key'],    # Application Key
                application_secret=ovhkeys['dns_ovh_application_secret'], # Application Secret
                consumer_key=ovhkeys['dns_ovh_consumer_key'],       # Consumer Key
        )
    except KeyError:
        print('Aborting! Environement Varaibles not found!')
        exit(0)


# Check A Records
for record in range(len(a_records)):
    result_chk_a_records = client.get('/domain/zone/'+zone+'/record',
            fieldType='A', # Filter the value of fieldType property (like) (type: zone.NamedResolutionFieldTypeEnum)
            subDomain=a_records[record], # Filter the value of subDomain property (ilike) (type: string)
    )
    print("Check A Records: "+str(result_chk_a_records)) # DEBUG
    if result_chk_a_records:
        print('A Record(s) for: '+a_records[record]+'.'+zone+' has been found, deleting record(s) ID:')
        print(result_chk_a_records)
        for record in range(len(result_chk_a_records)):
            result = client.delete('/domain/zone/'+zone+'/record/'+str(result_chk_a_records[record]))

# Create A Records
print('Creating DNS A records: '+str(a_records)+'.'+zone+' with IP: '+target_ip)
for a_record in range(len(a_records)):
    result_a_record = client.post('/domain/zone/'+zone+'/record', 
            fieldType='A',  #Resource record Name (type: zone.NamedResolutionFieldTypeEnum)
            subDomain=a_records[a_record], # Resource record subdomain (type: string)
            target=target_ip, # Resource record target (type: string)
            ttl=0, # Resource record ttl (type: long)
    )
    print(json.dumps(result_a_record, indent=4))

# Check NS Records
for record in range(len(ns_servers)):
    result_chk_ns_records = client.get('/domain/zone/'+zone+'/record',
            fieldType='NS', # Filter the value of fieldType property (like) (type: zone.NamedResolutionFieldTypeEnum)
            subDomain=subdomain, # Filter the value of subDomain property (ilike) (type: string)
    )
    print("Check NS Records: "+str(result_chk_ns_records)) # DEBUG
    if result_chk_ns_records:
        print('NS Record for: '+subdomain+'.'+zone+' has been found, deleting records ID:')
        print(result_chk_ns_records)
        for record in range(len(result_chk_ns_records)):
            result = client.delete('/domain/zone/'+zone+'/record/'+str(result_chk_ns_records[record]))

# Create NS Records
# Ticket OPEN on OVH as the API is not working as expected
print('Creating DNS NS record: '+subdomain+'.'+zone+' with public name: '+str(ns_servers)+'.'+subdomain+'.'+zone)
for server in range(len(ns_servers)):
    result_ns_record = client.post('/domain/zone/'+zone+'/record', 
            fieldType='NS',  #Resource record Name (type: zone.NamedResolutionFieldTypeEnum)
            subDomain=subdomain, # Resource record subdomain (type: string)
            target=ns_servers[server]+'.'+subdomain+'.'+zone, # Resource record target (type: string)
            ttl=0, # Resource record ttl (type: long)
    )
    print(json.dumps(result_ns_record, indent=4))

# Check DNS Servers
# Issue with results from the API

# Refresh to update records
result = client.post('/domain/zone/'+zone+'/refresh')
print("Refreshing to apply modifications")
