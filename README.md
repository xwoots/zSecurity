## Amazon Route 53: How to automatically update IP addresses without using Elastic IPs :

### Architecture

The architecture is quite simple:

* When the EC2 instance starts, it should get its new public IP address and update its own record in Route 53
* The DNS name to update is stored in a Tag on the EC2 instance
* The script should execute every time the EC2 instance starts (that is, every time it starts, not just the first boot)

### Implementation

First, there should be a **Record Set in Amazon Route 53** that defines the existing domain name.

Next, add some tags to the EC2 instance that will be used by the script:

* **DNS Name**: The DNS Name to associate with the instance
* **Hosted Zone ID**: Uniquely identifies the Zone record in Route 53 that needs to be updated (get it from your Route 53 Hosted Zone record)

Whenever the EC2 instance starts, it will run a script that will:

* Grab the information from the above tags
* Retrieve the instance's current public IP address
* Update the Route 53 record set with the new IP address

```bash
#!/bin/bash
# Extract information about the Instance
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id/)
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone/)
MY_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4/)

# Extract tags associated with instance
ZONE_TAG=$(aws ec2 describe-tags --region ${AZ::-1} --filters "Name=resource-id,Values=${INSTANCE_ID}" --query 'Tags[?Key==`AUTO_DNS_ZONE`].Value' --output text)
NAME_TAG=$(aws ec2 describe-tags --region ${AZ::-1} --filters "Name=resource-id,Values=${INSTANCE_ID}" --query 'Tags[?Key==`AUTO_DNS_NAME`].Value' --output text)

# Update Route 53 Record Set based on the Name tag to the current Public IP address of the Instance
aws route53 change-resource-record-sets --hosted-zone-id $ZONE_TAG --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"'$NAME_TAG'","Type":"A","TTL":300,"ResourceRecords":[{"Value":"'$MY_IP'"}]}}]}'
```

To execute the script automatically each time the instance starts (as opposed to User Data scripts that only run on the first boot), put the above script in this directory:

``` /var/lib/cloud/scripts/per-boot/ ```

Finally, the EC2 instance will need an IAM Role assigned that has permission to run the above commands (Replace HOSTED-ZONE-ID by the ID you retrieved):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:DescribeTags",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/HOSTED-ZONE-ID"
        }
    ]
}
```

## How to test

To test the script, simply Stop the instance then Start it again.

This will result in a new public IP address being assigned to the instance. The script will call Amazon Route 53 to update the record set. This might take a minute to update.

Then, return to Route 53 and look at the IP address assigned to the A-Record. It should be updated with the new IP address.

Credits / Source : https://dev.to/aws/amazon-route-53-how-to-automatically-update-ip-addresses-without-using-elastic-ips-h7o
