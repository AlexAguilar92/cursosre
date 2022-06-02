from aws_cdk import (
    aws_ec2 as ec2,
    core,
)

# from security_groups import security_groups_dictionary as sgd
# def generate_sg_instance(scope, sg_id, vpc, sg_name):
#  return ec2.SecurityGroup(
#         scope, sg_id, vpc=vpc, security_group_name=sg_name,
#  )

from constructs import Construct
 
class EC2InstanceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        vpc = ec2.Vpc(
            self,
            "VPC",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)
            ],
        )
        
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
        )
        
        prod = ec2.Instance(
            self,
            "instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amzn_linux,
            vpc=vpc,
        )
        
        # for security_group_id in sgd:
        #     group_properties = sgd[security_group_id]
        #     group_name = group_properties['group_name']
        #     group_instance = generate_sg_instance(
        #         self, security_group_id, vpc, group_name,
        #     )
        #     for rule in group_properties['rules']:
        #         group_instance.add_ingress_rule(
        #             ec2.Peer.any_ipv4(), # 0.0.0.0/0
        #             connection=ec2.Port.tcp(rule['port']),
        #             description=rule['description']
        #         )
        #     prod.add_security_group(group_instance)

        
        http =ec2.SecurityGroup(self, 'http', vpc=vpc, security_group_name='htt_sg')
        https = ec2.SecurityGroup(self, 'https', vpc=vpc, security_group_name='htts_sg')
        ssh = ec2.SecurityGroup(self, 'ssh', vpc=vpc, security_group_name='ssh_sg')

        http.add_ingress_rule(
            ec2.Peer.any_ipv4(), #0.0.0.0/0
            connection=ec2.Port.tcp(80),
            description="allow traffic from anywhere thru the port 80"
        )

        https.add_ingress_rule(
            ec2.Peer.any_ipv4(), #0.0.0.0/0
            connection=ec2.Port.tcp(443),
            description="allow traffic from anywhere thru the port 80"
        )

        ssh.add_ingress_rule(
            ec2.Peer.any_ipv4(), #0.0.0.0/0
            connection=ec2.Port.tcp(22),
            description="allow traffic from anywhere thru the port 80"
        )
        
app = core.App()
EC2InstanceStack(app, 'ec2Baseline')
app.synth()