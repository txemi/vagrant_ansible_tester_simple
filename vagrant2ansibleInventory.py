#!/usr/bin/env python

import vagrant


def iterate_ssh_configs():
    va = vagrant.Vagrant()
    statuses = va.status()
    for status in statuses:
        name = status[0]
        machine_status = status[1]
        if machine_status == 'not_created':
            continue
        ssh_conf_1 = va.ssh_config(vm_name=name)

        yield ssh_conf_1


def parse_ssh_config(ssh_config_string):
    ssh_config_map = {}
    for ssh_config_line in ssh_config_string.split('\n'):
        if ssh_config_line == '':
            continue
        ssh_config_words = ssh_config_line.split()
        ssh_config_map[ssh_config_words[0]] = ssh_config_words[1]
    return ssh_config_map


def printInventoryLine(ssh_config_map):
    formatstring = "{Host:<10} ansible_host={HostName:<16} ansible_port={Port:<5} ansible_user={User} ansible_ssh_private_key_file={IdentityFile}"
    formattedstring = formatstring.format(**ssh_config_map)
    print(formattedstring)


def main():
    for sshconf in iterate_ssh_configs():
        ssh_config_map = parse_ssh_config(sshconf)
        printInventoryLine(ssh_config_map)


if __name__ == "__main__":
    main()
