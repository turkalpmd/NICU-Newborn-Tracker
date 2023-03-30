import boto3
import sys
from loguru import logger

logger.remove()
logger.add(
    sink=sys.stdout,
    format="<level>{time:HH:mm:ss}</level> | <level>{level: <8}</level> | <level>{message}</level>",
    level="DEBUG"
)
# Create an EC2 client
ec2 = boto3.client('ec2', region_name='eu-central-1')
# Create a VPC
vpc = ec2.create_vpc(
    CidrBlock='10.0.0.0/16'
)
# Wait for the VPC to be available
waiter = ec2.get_waiter('vpc_available')
waiter.wait(VpcIds=[vpc['Vpc']['VpcId']])
logger.info("Created VPC with ID: {}", vpc['Vpc']['VpcId'])
ec2.create_tags(Resources=[vpc['Vpc']['VpcId']], Tags=[{'Key': 'Name', 'Value': 'premature-vpc'}])
# Enable DNS support for the VPC
ec2.modify_vpc_attribute(
    VpcId=vpc['Vpc']['VpcId'],
    EnableDnsSupport={'Value': True}
)
# Enable DNS hostnames for the VPC
ec2.modify_vpc_attribute(
    VpcId=vpc['Vpc']['VpcId'],
    EnableDnsHostnames={'Value': True}
)
# Create an Internet Gateway
igw = ec2.create_internet_gateway()
logger.info("Created Internet Gateway with ID: {}", igw['InternetGateway']['InternetGatewayId'])
# Attach the Internet Gateway to the VPC
ec2.attach_internet_gateway(
    InternetGatewayId=igw['InternetGateway']['InternetGatewayId'],
    VpcId=vpc['Vpc']['VpcId']
)
# Create three subnets in the VPC
subnet1 = ec2.create_subnet(
    VpcId=vpc['Vpc']['VpcId'],
    CidrBlock='10.0.0.0/24',
    AvailabilityZone='eu-central-1a'
)
waiter = ec2.get_waiter('subnet_available')
waiter.wait(SubnetIds=[subnet1['Subnet']['SubnetId']])
logger.info("Created Subnet 1 with ID: {}", subnet1['Subnet']['SubnetId'])
subnet2 = ec2.create_subnet(
    VpcId=vpc['Vpc']['VpcId'],
    CidrBlock='10.0.1.0/24',
    AvailabilityZone='eu-central-1b'
)
waiter.wait(SubnetIds=[subnet2['Subnet']['SubnetId']])
logger.info("Created Subnet 2 with ID: {}", subnet2['Subnet']['SubnetId'])
subnet3 = ec2.create_subnet(
    VpcId=vpc['Vpc']['VpcId'],
    CidrBlock='10.0.2.0/24',
    AvailabilityZone='eu-central-1c'
)
waiter.wait(SubnetIds=[subnet3['Subnet']['SubnetId']])
logger.info("Created Subnet 3 with ID: {}", subnet3['Subnet']['SubnetId'])
# Create a route table for the VPC
route_table = ec2.create_route_table(VpcId=vpc['Vpc']['VpcId'])
logger.info("Created Route Table with ID: {}", route_table['RouteTable']['RouteTableId'])
# Create a route to the Internet Gateway in the route table
ec2.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igw['InternetGateway']['InternetGatewayId'],
    RouteTableId=route_table['RouteTable']['RouteTableId']
)
logger.info("Created route to Internet Gateway in Route Table")
# Associate the subnets with the route table
ec2.associate_route_table(
    SubnetId=subnet1['Subnet']['SubnetId'],
    RouteTableId=route_table['RouteTable']['RouteTableId']
)
ec2.associate_route_table(
    SubnetId=subnet2['Subnet']['SubnetId'],
    RouteTableId=route_table['RouteTable']['RouteTableId']
)
ec2.associate_route_table(
    SubnetId=subnet3['Subnet']['SubnetId'],
    RouteTableId=route_table['RouteTable']['RouteTableId']
)
logger.info("Associated subnets with Route Table")