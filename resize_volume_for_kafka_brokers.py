import subprocess
import time

from vungle_ec2 import *

def resize_xfs_drive(private_ip, mountpoint):
    # SSH command to print disk stats before growing the volume
    print("========================")
    print("Disk stats before resize")
    print("========================")
    ssh_remote_command = "ssh -o StrictHostKeyChecking=no ubuntu@%s -i ~/.keys/vungle-legacy df -h" % private_ip
    ssh_remote_command = ssh_remote_command.split()
    print(ssh_remote_command)

    df = subprocess.check_output(ssh_remote_command)
    print(df.decode())

    print("========================")
    print("Executing resize command")
    print("========================")
    # SSH command to resize
    ssh_remote_command = "ssh -o StrictHostKeyChecking=no ubuntu@%s -i ~/.keys/vungle-legacy sudo xfs_growfs -d %s"\
                         % (private_ip, mountpoint)
    ssh_remote_command = ssh_remote_command.split()
    print(ssh_remote_command)

    df = subprocess.check_output(ssh_remote_command)
    print(df.decode())

    # SSH command to print disk stats after growing the volume
    print("========================")
    print("Disk stats after resize")
    print("========================")
    ssh_remote_command = "ssh -o StrictHostKeyChecking=no ubuntu@%s -i ~/.keys/vungle-legacy df -h" % private_ip
    ssh_remote_command = ssh_remote_command.split()
    print(ssh_remote_command)

    df = subprocess.check_output(ssh_remote_command)
    print(df.decode())

def remove_idx_to_be_excluded(hostnames_to_process, idx_exclusion, instance_prefix):
    for idx in idx_exclusion:
        instance_name = "{}-{}".format(instance_prefix, idx)
        hostnames_to_process.remove(instance_name)
    return hostnames_to_process

def main():
    if len(sys.argv) < 4:
        print("\033[91mTo run the script, you need to provide the following args:\033[0m")
        print("\033[93m- Input filename\033[0m")
        print("\033[93m- Instance name prefix eg. kafka-broker, kafka-221\033[0m")
        print("\033[93m- Max instance index eg. 30 (this will let the script search for kafka-221-0 to kafka-221-29\033[0m")
        print("\033[93m- Optional - Indexes to be excluded eg. 1,3,4\033[0m")
        print("\033[92mExample on how to run the script: python resize_volume_for_kafka_brokers.py kafka-221 2 1\033[0m")
        return

    input_filename = sys.argv[1]
    instance_prefix = sys.argv[2]
    instance_max_idx = int(sys.argv[3])

    if len(sys.argv) == 5:
        idx_exclusion = sys.argv[4].split(',')
    else:
        idx_exclusion = []

    ec2 = VungleEC2()

    f = open(input_filename)
    data = f.read()
    modification_list = data.split('\n')[:-1]

    hostnames_to_process = ["{}-{}".format(instance_prefix, idx) for idx in range(instance_max_idx)]
    remove_idx_to_be_excluded(hostnames_to_process, idx_exclusion, instance_prefix)
    print(hostnames_to_process)

    for modification in modification_list:
        [instance_detail, private_ip, disk_stats, volume_id, new_size] = modification.split(' => ')

        hostname = instance_detail.split('.')[0]
        if hostname in hostnames_to_process:
            print("Attempting to modify EBS Volume size [%s] to [%sGB]" % (volume_id, new_size))
            modification_status = ec2.modify_ebs_volume_size(volume_id=volume_id, new_size=int(new_size), dry_run=False)
            if modification_status:
                #ec2.show_ebs_modification_progress(volume_id)
                optimizing = False
                while not optimizing:
                    time.sleep(5)
                    ebs_modification_state = ec2.get_ebs_volume_modification_state(volume_id)

                    if ebs_modification_state == 'optimizing':
                        print("EBS Volume is in optimizing state...")
                        optimizing = True
                    else:
                        print("EBS Volume is NOT YET in optimizing state...")

                mountpoint = instance_detail.split('.')[2]
                resize_xfs_drive(private_ip, mountpoint)
            else:
                print("Attempt to modify [%s] did not return success..." % volume_id)
                last_modification_start_time = ec2.get_ebs_volume_modification_start_time(volume_id)
                print("Last modification time was on [%s]" % last_modification_start_time)

if __name__ == '__main__':
    main()