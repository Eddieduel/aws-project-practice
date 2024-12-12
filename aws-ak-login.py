import boto3
from kubernetes import client, config

ak_list = [
  {
    "AK": "AKIA3RS2JAHI5341EDAD",
    "AKS": "ucMU7wrbHHjC"
  }
]

def generate_kube_config(cluster_name, access_key_id, secret_access_key, region):
  """
  Generates a kubeconfig file for accessing an EKS cluster using AWS access key ID and secret access key.

  Args:
    cluster_name: The name of your EKS cluster.
    access_key_id: Your AWS access key ID.
    secret_access_key: Your AWS secret access key.
    region: The AWS region where your EKS cluster is located. 
  """

  session = boto3.Session(
      aws_access_key_id=access_key_id,
      aws_secret_access_key=secret_access_key,
      region_name=region
  )

  eks = session.client('eks')

  response = eks.describe_cluster(name=cluster_name)
  cluster_info = response['cluster']

  # Get cluster CA certificate and endpoint
  certificate = cluster_info['certificateAuthority']['data']
  endpoint = cluster_info['endpoint']

  with open('~/.kube/config', 'w') as f:
    f.writelines([f'apiVersion: v1\n',
                  'clusters:\n',
                  '- cluster:\n',
                  f'    certificate-authority-data: {certificate}\n',
                  f'    server: {endpoint}\n',
                  '  name: kubernetes\n',
                  'contexts:\n',
                  '- context:\n',
                  '    cluster: kubernetes\n',
                  '    user: aws\n',
                  '  name: aws\n',
                  'current-context: aws\n',
                  'kind: Config\n',
                  'preferences: {}\n',
                  'users:\n',
                  '- name: aws\n',
                  '  user:\n',
                  '    exec:\n',
                  '      apiVersion: client.authentication.k8s.io/v1beta1\n',
                  '      command: aws\n',
                  '      args:\n',
                  '        - --region\n',
                  '        - {region}\n',
                  '        - eks\n',
                  '        - get-token\n',
                  '        --cluster-name\n',
                  f'        - {cluster_name}\n',
                  '        --aws-access-key-id\n',
                  f'        - {access_key_id}\n',
                  '        --aws-secret-access-key\n',
                  f'        - {secret_access_key}\n'
                  ])

# Replace with your cluster name, access key, secret key, and region
cluster_name = "your-cluster-name" 
access_key_id = "YOUR_ACCESS_KEY_ID"
secret_access_key = "YOUR_SECRET_ACCESS_KEY"
region = "YOUR_AWS_REGION"  # e.g., 'us-west-2' 

generate_kube_config(cluster_name, access_key_id, secret_access_key, region)