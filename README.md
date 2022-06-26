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

![capture](/readme/ec2_tags.png)

Whenever the EC2 instance starts, it will run a script that will:

* Grab the information from the above tags
* Retrieve the instance's current public IP address
* Update the Route 53 record set with the new IP address

```
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
