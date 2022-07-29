To simulate on-prem connectivity, we primarily use a Cisco 1000v from the AWS console, deploy it in a VPC and create a site-to-site VPN to a VGW attached to another VPC. This involves downloading the config and then picking out the relevant sections, modifying the tunnel source interfaces, local-address config, etc… which is time-consuming and also error-prone. 

To avoid such issues, you could make use of the below python script which would clean up the config and replace the relevant interfaces. 

Save the python script as cleanup_config.py

Download the VPN config from AWS console or Aviatrix controller and  run the script using the below syntax:

python cleanup_config.py -f <vpn_config_file_name>

Example:

```shell
python cleanup_config.py -f vpn-0302c7988e405b648.txt


conf t
crypto isakmp policy 200
  encryption aes 128
  authentication pre-share
  group 2
  lifetime 28800
  hash sha
exit
crypto keyring keyring-vpn-0302c7988e405b648-0
        local-address Gigabitethernet 1
  pre-shared-key address 13.38.223.177 key Fbmdnpf57DptlYlDejVrHpfE99e9zzlq
exit
crypto isakmp profile isakmp-vpn-0302c7988e405b648-0
  local-address Gigabitethernet 1
  match identity address 13.38.223.177
  keyring keyring-vpn-0302c7988e405b648-0
exit
crypto ipsec transform-set ipsec-prop-vpn-0302c7988e405b648-0 esp-aes 128 esp-sha-hmac
  mode tunnel
exit
crypto ipsec profile ipsec-vpn-0302c7988e405b648-0
  set pfs group2
  set security-association lifetime seconds 3600
  set transform-set ipsec-prop-vpn-0302c7988e405b648-0
exit
crypto ipsec df-bit clear
crypto isakmp keepalive 10 10
crypto ipsec security-association replay window-size 128
crypto ipsec fragmentation before-encryption
interface Tunnel1
  ip address 169.254.107.58 255.255.255.252
  ip virtual-reassembly
  tunnel source Gigabitethernet 1
  tunnel destination 13.38.223.177
  tunnel mode ipsec ipv4
  tunnel protection ipsec profile ipsec-vpn-0302c7988e405b648-0
  ! This option causes the router to reduce the Maximum Segment Size of
  ! TCP packets to prevent packet fragmentation.
  ip tcp adjust-mss 1379
  no shutdown
exit
router bgp 65001
  neighbor 169.254.107.57 remote-as 64512
  neighbor 169.254.107.57 activate
  neighbor 169.254.107.57 timers 10 30 30
  address-family ipv4 unicast
    neighbor 169.254.107.57 remote-as 64512
    neighbor 169.254.107.57 timers 10 30 30
    neighbor 169.254.107.57 default-originate
    neighbor 169.254.107.57 activate
    neighbor 169.254.107.57 soft-reconfiguration inbound
    network 0.0.0.0
  exit
exit
crypto isakmp policy 201
  encryption aes 128
  authentication pre-share
  group 2
  lifetime 28800
  hash sha
exit
crypto keyring keyring-vpn-0302c7988e405b648-1
        local-address Gigabitethernet 1
  pre-shared-key address 15.237.153.40 key 4_uJnzfCfHOubqdeckfR.RmyowtW8zoX
exit
crypto isakmp profile isakmp-vpn-0302c7988e405b648-1
  local-address Gigabitethernet 1
  match identity address 15.237.153.40
  keyring keyring-vpn-0302c7988e405b648-1
exit
crypto ipsec transform-set ipsec-prop-vpn-0302c7988e405b648-1 esp-aes 128 esp-sha-hmac
  mode tunnel
exit
crypto ipsec profile ipsec-vpn-0302c7988e405b648-1
  set pfs group2
  set security-association lifetime seconds 3600
  set transform-set ipsec-prop-vpn-0302c7988e405b648-1
exit
crypto ipsec df-bit clear
crypto isakmp keepalive 10 10
crypto ipsec security-association replay window-size 128
crypto ipsec fragmentation before-encryption
interface Tunnel2
  ip address 169.254.122.178 255.255.255.252
  ip virtual-reassembly
  tunnel source Gigabitethernet 1
  tunnel destination 15.237.153.40
  tunnel mode ipsec ipv4
  tunnel protection ipsec profile ipsec-vpn-0302c7988e405b648-1
  ! This option causes the router to reduce the Maximum Segment Size of
  ! TCP packets to prevent packet fragmentation.
  ip tcp adjust-mss 1379
  no shutdown
exit
router bgp 65001
  neighbor 169.254.122.177 remote-as 64512
  neighbor 169.254.122.177 activate
  neighbor 169.254.122.177 timers 10 30 30
  address-family ipv4 unicast
    neighbor 169.254.122.177 remote-as 64512
    neighbor 169.254.122.177 timers 10 30 30
    neighbor 169.254.122.177 default-originate
    neighbor 169.254.122.177 activate
    neighbor 169.254.122.177 soft-reconfiguration inbound
    network 0.0.0.0
  exit
exit
```
