## Amazon Route 53: How to automatically update IP addresses without using Elastic IPs :

Add some tags to the EC2 instance that will be used by the script:

* **DNS Name**: The DNS Name to associate with the instance
* **Hosted Zone ID**: Uniquely identifies the Zone record in Route 53 that needs to be updated (get it from your Route 53 Hosted Zone record)

