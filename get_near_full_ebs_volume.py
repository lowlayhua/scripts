import subprocess
import re

from vungle_ec2 import *


def round_to_nearest_half(number):
    return round(number*2) / 2

def calculate_new_size(current_size, current_util_percentage, safe_disk_threshold):
    new_size = 1/safe_disk_threshold * (current_util_percentage * current_size)
    new_size = int(max(round_to_nearest_half(new_size) * 1000, current_size*1000+500))
    return new_size

def get_ebs_volume_id_for_nitro_disk(device, private_ip):
    ssh_remote_command = "ssh -o StrictHostKeyChecking=no ubuntu@%s -i ~/.keys/vungle-legacy sudo nvme id-ctrl %s | grep vol | awk '{print $3}'" % (private_ip, device)
    ssh_remote_command = ssh_remote_command.split()

    df = subprocess.check_output(ssh_remote_command)
    output = df.decode().split('\n')
    volume_id = output[0].replace('vol', 'vol-')
    return volume_id

def get_ebs_volume_id(ec2_client, instance_id, device, private_ip):
    if '/dev/xvd' in device:
        return ec2_client.get_ebs_volume_id(instance_id=instance_id, devices=[device])[0]
    else:
        if not private_ip:
            print("Private IP is required to retrieve Volume ID for Nitro-based disk")
            return
        else:
            return get_ebs_volume_id_for_nitro_disk(device, private_ip)

def main():
    if len(sys.argv) < 3:
        print("\033[91mTo run the script, you need to provide the following args:\033[0m")
        print("\033[93m- Instance name prefix eg. kafka-broker, kafka-221\033[0m")
        print("\033[93m- Max instance index eg. 30 (this will let the script search for kafka-221-0 to kafka-221-29\033[0m")
        print("\033[93m- Safe disk threshold to maintain eg. 75, 85 (if not specified, default is set to 75)\033[0m")
        print("\033[92mExample on how to run the script: python get_near_full_ebs_volume.py kafka-221 33 85\033[0m")
        return

    instance_prefix = sys.argv[1]
    instance_max_idx = int(sys.argv[2])
    if len(sys.argv) >= 4:
        safe_disk_threshold = int(sys.argv[3]) 
    else:
        safe_disk_threshold = 75

    print("Checking for the following instances: {}-[0-{}]".format(instance_prefix,instance_max_idx-1))
    print("Safe disk threshold is {}".format(safe_disk_threshold))
    ec2 = VungleEC2()

    modification_list = []
    mountpoint_list = ['/data3', '/data4', '/data5', '/data6', '/data7']
    for kafka_broker_idx in range(instance_max_idx):
        if instance_prefix == 'kafka-broker' and kafka_broker_idx == 5:
            continue
        kafka_broker_name = "{}-{}".format(instance_prefix, kafka_broker_idx)
        instance_id = ec2.get_instance_id_from_instance_name(kafka_broker_name)
        private_ip = ec2.get_private_ip_from_instance_name(kafka_broker_name)

        ssh_remote_command = "ssh -o StrictHostKeyChecking=no ubuntu@%s -i ~/.keys/vungle-legacy df -h" % private_ip
        ssh_remote_command = ssh_remote_command.split()
        print(ssh_remote_command)

        df = subprocess.check_output(ssh_remote_command)
        output = df.decode().split('\n')

        for line in output[1:-1]:
            [device, size, used, available, percent, mountpoint] = line.split()
            if mountpoint in mountpoint_list:
                percent = int(percent.replace('%', ''))
                if percent > safe_disk_threshold:
                    size = float(re.sub('[a-z|A-Z]', '', size))
                    size = round_to_nearest_half(size)
                    new_size = calculate_new_size(size, float(percent), safe_disk_threshold)
                    volume_id = get_ebs_volume_id(ec2, instance_id=instance_id, device=device, private_ip=private_ip)
                    modification_list.append(
                        { 'instance_name': kafka_broker_name, 'device': device, 'mountpoint': mountpoint,
                          'size': size, 'percent': percent, 'volume_id': volume_id,
                          'private_ip': private_ip, 'new_size': new_size}
                    )
                    print("[x] {0}.{1}.{2} => {3} ({4}%)".format(kafka_broker_name, device, mountpoint, size, percent))
                else:
                    print("[-] {0}.{1}.{2} => {3} ({4}%)".format(kafka_broker_name, device, mountpoint, size, percent))

    for modification in modification_list:
        print("{0}.{1}.{2} => {3} => {4} ({5}%) => {6} => {7}".format(
                    modification['instance_name'], \
                    modification['device'], \
                    modification['mountpoint'], \
                    modification['private_ip'], \
                    modification['size'], \
                    modification['percent'], \
                    modification['volume_id'], \
                    modification['new_size']))

if __name__ == "__main__":
    main()