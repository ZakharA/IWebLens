import sys
import subprocess
import time
import re
import json
import paramiko
import iWebLens_client


def main():
    if len(sys.argv) != 4:
        raise ValueError("Arguments list is wrong. Please use the following format: {} {} {}".format(
            "<instance_ip_address>", "<path_to_RSA_key>", "kubernetes_deployment"))
    instance_ip = sys.argv[1]
    app_url = "http://{}:1025/api/object_detection".format(instance_ip)
    key_path = sys.argv[2]
    k8_deployment = sys.argv[3]
    result = dict()
    instance = connectToInstance(instance_ip, key_path)
    for i in range(1, 4):
        # set new replica size and wait
        print("scaling {} to {} pods".format(k8_deployment, i))
        instance.exec_command(
            "kubectl scale {} --replicas={}".format(k8_deployment, i))
        time.sleep(10)
        mesurments = []
        print("let k8 to roll out new pods")
        # send images
        print("testing")
        for x in (2**p for p in range(6)):
            print("number of threads = {}".format(x))
            proc = subprocess.Popen(["python", 'iWebLens_client.py', "./inputfolder/",
                                     app_url, str(x)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            test_result_str = proc.communicate(
            )[0].splitlines()[-1].decode("utf-8")
            mesurments.append(re.findall("\d+\.\d+", test_result_str)[1])
        result[str(i)] = mesurments
        with open('results', 'w') as f:
            f.write(json.dumps(result))


def connectToInstance(ip, key):
    rsa_key = paramiko.RSAKey.from_private_key_file(key)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting to {}".format(ip))
    client.connect(ip, username="ubuntu", pkey=rsa_key)
    print("connected to {}".format(ip))
    return client


if __name__ == "__main__":
    main()
