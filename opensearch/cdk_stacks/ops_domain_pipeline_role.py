#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_iam
)
from constructs import Construct


class OpsDomainPipelineRoleStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, ops_domain_arn, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    domain_pipeline_policy_doc = aws_iam.PolicyDocument()

    domain_pipeline_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "effect": aws_iam.Effect.ALLOW,
      "resources": [f"arn:aws:es:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:domain/*"],
      "actions": [
        "es:DescribeDomain"
      ]
    }))

    domain_pipeline_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "effect": aws_iam.Effect.ALLOW,
      "resources": [ops_domain_arn],
      "actions": [
        "es:ESHttp*"
      ]
    }))

    pipeline_role = aws_iam.Role(self, 'OpenSearchIngestionPipelineRole',
      role_name='OpenSearchDomainPipelineRole',
      assumed_by=aws_iam.ServicePrincipal('osis-pipelines.amazonaws.com'),
      inline_policies={
        'domain-pipeline-policy': domain_pipeline_policy_doc
      }
    )
    self.iam_role = pipeline_role

    cdk.CfnOutput(self, 'RoleName',
      value=self.iam_role.role_name,
      export_name=f'{self.stack_name}-RoleName')
    cdk.CfnOutput(self, 'RoleArn',
      value=self.iam_role.role_arn,
      export_name=f'{self.stack_name}-RoleArn')