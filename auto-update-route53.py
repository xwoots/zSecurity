import boto3, requests
import difflib


d = difflib.Differ()

r = requests.get("https://checkip.amazonaws.com")

current_ip = r.text.strip()
zoneid = "Z0780024JLJK9BTLLRT5"
hostname = "znetwork.fr."

route53 = boto3.client('route53')

def updatedns(hostname, newdns):
    sets = route53.list_resource_record_sets(HostedZoneId=zoneid)
    for rset in sets['ResourceRecordSets']:
#        print(rset)
        if rset['Name'] == hostname and rset['Type'] == 'A':
            curdnsrecord = rset['ResourceRecords']
            print(curdnsrecord)
            if type(curdnsrecord) in [list, tuple, set]:
                for record in curdnsrecord:
                    curdns = record['Value']
            # print('Current DNS CNAME: %s' % curdns)
            curttl = rset['TTL']
            # print('Current DNS TTL: %s' % curttl)
            if curdns != newdns:
                # UPSERT the record
                print('Updating %s' % hostname)
                route53.change_resource_record_sets(
                    HostedZoneId=zoneid,
                    ChangeBatch={
                    'Changes': [
                        {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': hostname,
                            'Type': 'A',
                            'TTL': curttl,
                            'ResourceRecords': [
                            {
                                'Value': newdns
                            }
                            ]
                        }
                        }
                    ]
                    }
                )
try:
    updatedns(hostname, current_ip)
except:
    print('DNS Update failed. Check credentials or IAM roles.')
