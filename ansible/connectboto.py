import boto
import boto.ec2
from boto.ec2.regioninfo import RegionInfo
import time
#set the region
region=RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

#connect to nectar by using keys
#go nectar security - API - download ec2 credentials -ec2rc.sh - copy the keys
ec2_conn = boto.connect_ec2(aws_access_key_id='16a9a9a7d53441268ddbaaf8fc275030',
aws_secret_access_key='844cd078793546ce9fa97d05d21645af', is_secure=True, region=region, port=8773, path='/services/Cloud', validate_certs=False)

# create 4 instances
ec2_conn.run_instances('ami-e3cb07b2', key_name="cloudcomputing", instance_type='m1.medium', security_groups=['default','ssh','Webservers','database ingress','workload balance'],placement='melbourne-np')
ec2_conn.run_instances('ami-e3cb07b2', key_name="cloudcomputing", instance_type='m1.medium', security_groups=['default','ssh','Webservers','database ingress','workload balance'],placement='melbourne-np')
ec2_conn.run_instances('ami-e3cb07b2', key_name="cloudcomputing", instance_type='m1.medium', security_groups=['default','ssh','Webservers','database ingress','workload balance'],placement='melbourne-np')
ec2_conn.run_instances('ami-e3cb07b2', key_name="cloudcomputing", instance_type='m1.medium', security_groups=['default','ssh','Webservers','database ingress','workload balance'],placement='melbourne-np')
time.sleep(300)
print "Sleep for 300 seconds wait for instances set up "


vol_req1 = ec2_conn.create_volume(5, "melbourne-np")
vol_req2 = ec2_conn.create_volume(5, "melbourne-np")
vol_req3 = ec2_conn.create_volume(5, "melbourne-np")
vol_req4 = ec2_conn.create_volume(5, "melbourne-np")

'''
curr_vol = ec2_conn.get_all_volumes([vol_req.id])[0]
print curr_vol.status
print curr_vol.zone
'''
#conn = boto.ec2.connect_to_region("us-west-2", aws_access_key_id='16a9a9a7d53441268ddbaaf8fc275030', aws_secret_access_key='844cd078793546ce9fa97d05d21645af')



#List images
'''
i=0
images = ec2_conn.get_all_images()
for img in images:
	print 'id: ', img.id, 'name: ', img.name
	i+=1
	if(i>4):
		break
'''


volumes=[vol_req1.id, vol_req2.id, vol_req3.id, vol_req4.id]

#Get reservations:
instanceids=[]
reservations = ec2_conn.get_all_reservations()
for r in reservations:
	instanceids.append(r.id)
	print r.id

for i in range(0,4)
    ec2_conn.attach_volume (volumes[i], instanceids[i], "/dev/vdc")


#Show reservation details:
reservations = ec2_conn.get_all_reservations()
'''
for idx, res in enumerate(reservations):
	print idx, res.id, res.instances
'''

#Show instance details:
f=open('hosts.ini','w')
f.write('-\n')
f.write('[allservers]')
for i in range(4):
	f.write(str(reservations[i].instances[0].private_ip_address)+"\n")
    print reservations[i].instances[0].private_ip_address
f.write("\n")
f.write("[res]\n")

f.write('hi')
