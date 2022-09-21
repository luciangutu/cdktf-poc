#!/usr/bin/env python
from cdktf import App, TerraformStack, TerraformOutput, S3Backend
from constructs import Construct
from imports.aws import AwsProvider, ec2, ssm


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        self.region_1 = "us-east-1"
        self.region_2 = "eu-west-1"

        self.provider_aws1 = AwsProvider(self, "aws1", region=self.region_1, alias="aws1")
        self.provider_aws2 = AwsProvider(self, "aws2", region=self.region_2, alias="aws2")

        # initialising backend
        S3Backend(self, bucket='cdktf-aws-demo', key='cdktf-instance', region=self.region_1)

        self.ec2_instance = self.create_ec2()
        self.ssm_param = self.create_ssm()

    def create_ec2(self):
        instance_name = "cdkdemo"
        instance = ec2.Instance(self, instance_name,
                                ami="ami-05fa00d4c63e32376",
                                instance_type="t2.micro",
                                provider=self.provider_aws1
                                )
        TerraformOutput(self, f'{instance_name}-name',
                        value=instance.public_ip
                        )
        return instance

    def create_ssm(self):
        return ssm.SsmParameter(self, "cdk-poc",
                                description="The value Foo",
                                name="FooCDKParameter",
                                value="FooValue",
                                type="String",
                                provider=self.provider_aws2
                                )


app = App()
try:
    MyStack(app, "cdktf-aws-demo")
    app.synth()
except Exception as e:
    print(e)
