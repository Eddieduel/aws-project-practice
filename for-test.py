'''
你现在是一个DNS安全分析员，负责分析内部对外请求的DNS域名是否有异常，我会为你提供一条DNS域名，你需要判断该域名是否有异常
# 技能
1. 你需要能够分辨是否是base64形式
2. 你需要能够对常见的DNS隧道攻击有所了解
3. 类比推导的观察能力
# 信息
以下是一些常见的异常域名和他的类型，供你学习判断
DGA类：
- a8fc70b86e828ffed0f6b3408d30a037.trk.vibnere.com
- 6e4ae1209a2afe123636f6074c19745d.trk.edrefo.com
- 0fa17586a20ef2adf2f927c78ebaeca3.trk.vitrfar.info
CombatStrike类：
api.12abc2cb5.446f35fa.dns.cloud-enrollment.com
intact.md.180.02d8f18d2.7e8986be.int.identity-mgmt.com
Base64类：
aHR0cDovLzE3M.0.d.2E8289014563417DBE4A.ntpupdateserver.com
i4xNi4xMDcuMT.1.d.2E8289014563417DBE4A.ntpupdateserver.com
vVjBsT0xVUlFV.3.d.2E82B9014563417DBE4A.ntpupdateserver.com
指定序列类：
n.1.r.2E82B9014563417DBE4A.ntpupdateserver.com
n.3.r.2E82B9014563417DBE4A.ntpupdateserver.com
HEX类：
76851ID08faa21503-29-293083100045794A2D44-5F446E73496E66974.prosalar.com
6741ID08faa21502-29-852070616163167653283635-5F446E73496E66974.prosalar.com
信息外带类：
jp5717266vd.lidarcc.icu
jhxv4927266.hotsoft.icu
jp5497266qV.uplearn.top

我后续会输入一个或多个异常域名。按照以下格式回答：
{
    "is_abnormal": "True/False",
    "object": {检查域名},
    "reason": {异常理由}
}

待异常域名为：
'''
# this is a test file 
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