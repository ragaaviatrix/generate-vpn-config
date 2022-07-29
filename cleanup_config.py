import re
import argparse

show_config_pattern = re.compile(r'^(?!\!).+', re.M)
vendor_pattern = re.compile(r'Aviatrix')
replace_interface_pattern_cisco = re.compile(
    r'<interface_name/private_IP_on_outside_interface>')
replace_avx_isakmp_policy_pattern = re.compile(r'<crypto_policy_number>')
replace_avx_tunnel1_pattern = re.compile(r'<tunnel_number1>')
replace_avx_tunnel2_pattern = re.compile(r'<tunnel_number2>')
replace_avx_wan_intf_pattern = re.compile(r'<ios_wan_interface1>|<ios_wan_interface2>')
trim_lines_pattern = re.compile(r'For.*', re.DOTALL)


def cleanup_aws(config):
    with open(config, 'r') as infile:
        full_file = infile.read()
        change = replace_interface_pattern_cisco.sub(
            'Gigabitethernet 1', full_file)
        matches = re.findall(show_config_pattern, change)
        print('\n')
        print('conf t')
        for line in matches:
            print(line)
        print('\n')


def cleanup_aviatrix(config):
    with open(config, 'r') as infile:
        full_file = infile.read()
        trimmed_file = trim_lines_pattern.sub('',full_file)
        matches = re.findall(show_config_pattern, trimmed_file)
        print('\n')
        print('conf t')
        for line in matches:
            policy_match = re.findall(replace_avx_isakmp_policy_pattern, line)
            tunnel1_match = re.findall(replace_avx_tunnel1_pattern, line)
            tunnel2_match = re.findall(replace_avx_tunnel2_pattern, line)
            wan_intf_match = re.findall(replace_avx_wan_intf_pattern,line)
            
            if policy_match:
                change = replace_avx_isakmp_policy_pattern.sub('220', line)
                print(change)
            elif tunnel1_match:
                change = replace_avx_tunnel1_pattern.sub('100', line)
                print(change)
            elif tunnel2_match:
                change = replace_avx_tunnel2_pattern.sub('200', line)
                print(change)
            elif wan_intf_match:
                change = replace_avx_wan_intf_pattern.sub(
                    'Gigabitethernet 1', line)
                print(change)
            else:
                print(line)
        print('\n')


def check_vendor(file):
    with open(file, 'r') as infile:
        full_file = infile.read()
        matches = re.findall(vendor_pattern, full_file)
        if matches:
            vendor = 'aviatrix'
        else:
            vendor = 'aws'
    return vendor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate config for VPN')
    parser.add_argument('-f', '--file-name', required=True, help="VPN file")

    user_input = parser.parse_args()

    file_name = user_input.file_name

    vendor = check_vendor(file_name)

    if vendor == 'aws':
        cleanup_aws(file_name)
    else:
        cleanup_aviatrix(file_name)
