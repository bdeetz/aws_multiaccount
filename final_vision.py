#!/usr/bin/env python

from diagrams import Cluster, Diagram
from diagrams.aws.network import VPC, TransitGateway
from diagrams.aws.management import Cloudtrail
from diagrams.aws.cost import CostExplorer, Budgets, SavingsPlans, ReservedInstanceReporting
from diagrams.aws.security import IAM, IAMRole

graph_attr = {
    'rankdir': 'TB',
#    'nodesep': '9',
#    'pad': '5',
    'ranksep': '12',
#    'fontsize': '100',
#    'margin': '2.0,2.0'
}

with Diagram('AIQ Multi Account Architecture', show=False, graph_attr=graph_attr):
    transit_gateway = None
    central_cloudtrail = None
    central_iam = None

    with Cluster('Security Account'):
        central_cloudtrail = Cloudtrail('Aggregated CloudTrail')
        central_iam = IAM('Centralized IAM')

    with Cluster('Billing Account'):
        CostExplorer('Centralized Cost Explorer')
        Budgets('Centralized Budgets')
        SavingsPlans('Centralized Savings Plans')
        ReservedInstanceReporting('Centralized Reserved Instance Reporting')
        IAMRole('Billing IAM Role') - central_iam

    with Cluster('Shared Services Account'):
        transit_gateway = TransitGateway('Centralized Transit Gateway')

        with Cluster('Public'):
            VPC('Public VPC') - transit_gateway
        with Cluster('Private VPC'):
            VPC('Private VPC') - transit_gateway

        Cloudtrail('Shared Service CloudTrail') - central_cloudtrail
        IAMRole('Shared Services IAM Role') - central_iam

    with Cluster('New Prod Account'):
        with Cluster('Prod VPC'):
            VPC('Prod VPC') - transit_gateway

            Cloudtrail('New Prod CloudTrail') - central_cloudtrail
        IAMRole('New Prod IAM Role') - central_iam

    with Cluster('Dev Account'):
        with Cluster('Dev VPC'):
            VPC('Dev VPC') - transit_gateway

            Cloudtrail('Dev CloudTrail') - central_cloudtrail
        IAMRole('Dev IAM Role') - central_iam

    with Cluster('Sandbox Accounts'):
        with Cluster('Sandbox Account 1'):
            VPC('Sandbox 1 VPC') - transit_gateway

            Cloudtrail('Sandbox 1 CloudTrail') - central_cloudtrail
            IAMRole('Sandbox IAM Role') - central_iam

        with Cluster('Sandbox Account 2'):
            VPC('Sandbox 2 VPC') - transit_gateway

            Cloudtrail('Sandbox 2 CloudTrail') - central_cloudtrail
            IAMRole('Sandbox IAM Role') - central_iam

        with Cluster('Sandbox Account 3'):
            VPC('Sandbox 3 VPC') - transit_gateway

            Cloudtrail('Sandbox 3 CloudTrail') - central_cloudtrail
            IAMRole('Sandbox IAM Role') - central_iam

        with Cluster('Sandbox Account N'):
            VPC('Sandbox N VPC') - transit_gateway

            Cloudtrail('Sandbox N CloudTrail') - central_cloudtrail
            IAMRole('Sandbox IAM Role') - central_iam
