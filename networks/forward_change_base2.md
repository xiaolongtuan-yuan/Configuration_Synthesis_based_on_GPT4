## base/configs/leaf1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname leaf1
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.1.2 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip access-group RESTRICT_NETWORK_TRAFFIC_IN in
 ip address 2.34.101.4 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip access-group RESTRICT_NETWORK_TRAFFIC_IN in
 ip address 2.34.201.4 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.128.0.2 255.255.255.252
 ip access-group RESTRICT_HOST_TRAFFIC_IN in
 ip access-group RESTRICT_HOST_TRAFFIC_OUT out
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.128.1.2 255.255.255.252
 ip access-group RESTRICT_HOST_TRAFFIC_IN in
 ip access-group RESTRICT_HOST_TRAFFIC_OUT out
 negotiation auto
!
router bgp 65001
 bgp router-id 2.1.4.1
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor 2.34.101.3 peer-group as2
 neighbor 2.34.201.3 peer-group as2
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  network 2.128.0.0 mask 255.255.255.252
  network 2.128.1.0 mask 255.255.255.252
  neighbor as2 send-community
  neighbor as2 route-map as2_to_dept in
  neighbor as2 route-map dept_to_as2 out
  neighbor 2.34.101.3 activate
  neighbor 2.34.201.3 activate
  ! maximum-paths eibgp 5
 exit-address-family
!
ip forward-protocol nd
!
ip bgp-community new-format
ip community-list expanded as2_community permit _2:
!
no ip http server
no ip http secure-server
!
ip access-list extended RESTRICT_HOST_TRAFFIC_IN
 permit ip 2.128.0.0 0.0.255.255 any
 deny   ip any any
 permit icmp any any
ip access-list extended RESTRICT_HOST_TRAFFIC_OUT
 permit tcp any 2.128.0.0 0.0.1.255 eq www
 permit tcp any 2.128.0.0 0.0.1.255 eq ssh
 permit udp any 2.128.0.0 0.0.255.255 
 deny   ip any any
ip access-list extended RESTRICT_NETWORK_TRAFFIC_IN
 deny ip any 2.128.0.2 0.0.0.0
 deny ip any 2.128.1.2 0.0.0.0
 permit ip any any
!
access-list 102 permit ip host 2.128.0.0 host 255.255.255.252
access-list 102 permit ip host 2.128.1.0 host 255.255.255.252
access-list 105 permit ip host 1.0.1.0 host 255.255.255.0
access-list 105 permit ip host 1.0.2.0 host 255.255.255.0
access-list 105 permit ip host 3.0.1.0 host 255.255.255.0
access-list 105 permit ip host 3.0.2.0 host 255.255.255.0
!
route-map dept_to_as2 permit 100
 match ip address 102
 set metric 50
 set community 65001:2 additive
!
route-map as2_to_dept permit 100
 match community as2_community
 set local-preference 350
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件

## base/configs/core2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname core2
!
boot-start-marker
boot-end-marker
!
!
logging host 1.1.1.1
logging host 2.2.2.2
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.2.2 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 mtu 1800
 ip address 2.12.22.2 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
 ip ospf cost 100
!
interface GigabitEthernet1/0
 mtu 1600
 ip address 2.12.12.2 255.255.255.0
 negotiation auto
 ip ospf cost 100
!
interface GigabitEthernet2/0
 mtu 1700
 ip address 2.23.22.2 255.255.255.0
 negotiation auto
 ip ospf cost 100
!
interface GigabitEthernet3/0
 ip address 2.23.21.2 255.255.255.0
 negotiation auto
 ip ospf cost 100
!
router ospf 1
 router-id 2.1.2.2
 network 2.0.0.0 0.255.255.255 area 1
!
router bgp 2
 bgp router-id 2.1.2.2
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor 2.1.1.1 peer-group as2
 neighbor 2.1.1.1 update-source Loopback0
 neighbor 2.1.1.2 peer-group as2
 neighbor 2.1.1.2 update-source Loopback0
 neighbor 2.1.3.1 peer-group as2
 neighbor 2.1.3.1 update-source Loopback0
 neighbor 2.1.3.2 peer-group as2
 neighbor 2.1.3.2 update-source Loopback0
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  neighbor as2 send-community
  neighbor as2 route-reflector-client
  neighbor as2 advertise additional-paths all
  neighbor as3 peer-group
  neighbor as3 route-map filter-bogons in
  neighbor 2.1.1.1 activate
  neighbor 2.1.1.2 activate
  neighbor 2.1.3.1 activate
  neighbor 2.1.3.2 activate
 exit-address-family
!
ip forward-protocol nd
!
no ip http server
no ip http secure-server
!
ip route 2.128.1.1 255.255.255.255 null0
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件

## base/configs/core1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname core1
!
boot-start-marker
boot-end-marker
!
!
logging host 1.1.1.1
logging host 2.1.2.2
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.2.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 2.12.11.2 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
 ip ospf cost 1
!
interface GigabitEthernet1/0
 ip address 2.12.21.2 255.255.255.0
 negotiation auto
 ip ospf cost 1
!
interface GigabitEthernet2/0
 ip address 2.23.11.2 255.255.255.0
 negotiation auto
 ip ospf cost 1
!
interface GigabitEthernet3/0
 ip address 2.23.12.2 255.255.255.0
 negotiation auto
 ip ospf cost 1
!
router ospf 1
 router-id 2.1.2.1
 network 2.0.0.0 0.255.255.255 area 1
!
router bgp 2
 bgp router-id 2.1.2.1
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor 2.1.1.1 peer-group as2
 neighbor 2.1.1.1 update-source Loopback0
 neighbor 2.1.1.2 peer-group as2
 neighbor 2.1.1.2 update-source Loopback0
 neighbor 2.1.3.1 peer-group as2
 neighbor 2.1.3.1 update-source Loopback0
 neighbor 2.1.3.2 peer-group as2
 neighbor 2.1.3.2 update-source Loopback0
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  neighbor as2 send-community
  neighbor as2 route-reflector-client
  neighbor as2 advertise additional-paths all
  neighbor 2.1.1.1 activate
  neighbor 2.1.1.2 activate
  neighbor 2.1.3.1 activate
  neighbor 2.1.3.2 activate
  ! maximum-paths eibgp 5
 exit-address-family
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件

## base/configs/spine2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname spine2
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.3.2 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 2.23.22.3 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.23.12.3 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.34.201.3 255.255.255.0
 negotiation auto
!
router ospf 1
 router-id 2.1.3.2
 redistribute connected subnets
 network 2.1.0.0 0.0.255.255 area 1
 network 2.23.0.0 0.0.255.255 area 1
!
router bgp 2
 bgp router-id 2.1.3.2
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor dept peer-group
 neighbor dept remote-as 65001
 neighbor 2.1.2.1 peer-group as2
 neighbor 2.1.2.1 update-source Loopback0
 neighbor 2.1.2.2 peer-group as2
 neighbor 2.1.2.2 update-source Loopback0
 neighbor 2.34.201.4 peer-group dept
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  neighbor as2 send-community
  neighbor as2 advertise additional-paths all
  neighbor dept send-community
  neighbor dept route-map dept_to_as2dist in
  neighbor dept route-map as2dist_to_dept out
  neighbor 2.1.2.1 activate
  neighbor 2.1.2.2 activate
  neighbor 2.34.201.4 activate
  ! maximum-paths eibgp 5
 exit-address-family
!
ip forward-protocol nd
!
ip bgp-community new-format
ip community-list expanded dept_community permit _65001:
!
no ip http server
no ip http secure-server
!
access-list 102 permit ip host 2.128.0.0 host 255.255.0.0
access-list 105 permit ip host 1.0.1.0 host 255.255.255.0
access-list 105 permit ip host 1.0.2.0 host 255.255.255.0
access-list 105 permit ip host 3.0.1.0 host 255.255.255.0
access-list 105 permit ip host 3.0.2.0 host 255.255.255.0
!
route-map as2dist_to_dept permit 100
 match ip address 105
 set metric 50
 set community 2:65001 additive
!
route-map dept_to_as2dist permit 100
 match community dept_community
 set local-preference 350
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件

## base/configs/border2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname border2
!
boot-start-marker
boot-end-marker
!
!
ntp server 18.18.18.18
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.1.2 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 10.23.21.2 255.255.255.0
 ip access-group OUTSIDE_TO_INSIDE in
 ip access-group INSIDE_TO_AS3 out
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.12.22.1 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.12.21.1 255.255.255.0
 negotiation auto
!
router ospf 1
 router-id 2.1.1.2
 redistribute connected subnets
 network 2.0.0.0 0.255.255.255 area 1
!
router bgp 2
 bgp router-id 2.1.1.2
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor 2.1.2.1 peer-group as2
 neighbor 2.1.2.1 update-source Loopback0
 neighbor 2.1.2.2 peer-group as2
 neighbor 2.1.2.2 update-source Loopback0
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  aggregate-address 2.128.0.0 255.255.0.0 summary-only
  neighbor as2 send-community
  neighbor as2 advertise additional-paths all
  neighbor 2.1.2.1 activate
  neighbor 2.1.2.2 activate
  ! maximum-paths eibgp 5
 exit-address-family
!
ip forward-protocol nd
!
ip bgp-community new-format
ip community-list expanded as1_community permit _1:
ip community-list expanded as2_community permit _2:
ip community-list expanded as3_community permit _3:
!
no ip http server
no ip http secure-server
!
ip access-list extended INSIDE_TO_AS3
 permit ip 2.0.0.0 0.255.255.255 3.0.0.0 0.255.255.255
 permit ip 10.23.21.2 0.0.0.0 10.23.21.3 0.0.0.0
 deny   ip any any
ip access-list extended OUTSIDE_TO_INSIDE
 permit tcp any 2.128.0.0 0.0.1.255 eq ssh
 permit udp any 2.0.0.0 0.255.255.255
 deny ip any any
!
!
ip prefix-list inbound_route_filter seq 5 deny 2.0.0.0/8 le 32
ip prefix-list inbound_route_filter seq 10 permit 0.0.0.0/0 le 32
!
ip prefix-list outbound_routes seq 5 permit 2.128.0.0/9 ge 16
access-list 101 permit ip host 1.0.1.0 host 255.255.255.0
access-list 101 permit ip host 1.0.2.0 host 255.255.255.0
access-list 103 permit ip host 3.0.1.0 host 255.255.255.0
access-list 103 permit ip host 3.0.2.0 host 255.255.255.0
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件

## base/configs/spine1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname spine1
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.3.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 2.23.11.3 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.23.21.3 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.34.101.3 255.255.255.0
 negotiation auto
!
router ospf 1
 router-id 2.1.3.1
 ! redistribute connected subnets
 network 2.1.0.0 0.0.255.255 area 1
 network 2.23.0.0 0.0.255.255 area 1
!
router bgp 2
 bgp router-id 2.1.3.1
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor dept peer-group
 neighbor dept remote-as 65001
 neighbor 2.1.2.1 peer-group as2
 neighbor 2.1.2.1 update-source Loopback0
 neighbor 2.1.2.2 peer-group as2
 neighbor 2.1.2.2 update-source Loopback0
 neighbor 2.34.101.4 peer-group dept
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  neighbor as2 send-community
  neighbor as2 advertise additional-paths all
  neighbor dept send-community
  neighbor dept route-map dept_to_as2dist in
  neighbor dept route-map as2dist_to_dept out
  neighbor 2.1.2.1 activate
  neighbor 2.1.2.2 activate
  neighbor 2.34.101.4 activate
  ! maximum-paths eibgp 5
 exit-address-family
!
ip forward-protocol nd
!
ip bgp-community new-format
ip community-list expanded dept_community permit _65001:
!
no ip http server
no ip http secure-server
!
access-list 102 permit ip host 2.128.0.0 host 255.255.0.0
access-list 105 permit ip host 1.0.1.0 host 255.255.255.0
access-list 105 permit ip host 1.0.2.0 host 255.255.255.0
access-list 105 permit ip host 3.0.1.0 host 255.255.255.0
access-list 105 permit ip host 3.0.2.0 host 255.255.255.0
!
route-map as2dist_to_dept permit 100
 match ip address 105
 set metric 50
 set community 2:65001 additive
!
route-map dept_to_as2dist permit 100
 match community dept_community
 set local-preference 350
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件

## base/configs/border1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname border1
!
boot-start-marker
boot-end-marker
!
!
ntp server 18.18.18.18
ntp server 23.23.23.23
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
aaa new-model
aaa authentication login privilege-mode
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 ip address 2.1.1.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 10.12.11.2 255.255.255.0
 ip access-group OUTSIDE_TO_INSIDE in
 ip access-group INSIDE_TO_AS1 out
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.12.11.1 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.12.12.1 255.255.255.0
 negotiation auto
!
router ospf 1
 router-id 2.1.1.1
 redistribute connected subnets
 network 2.0.0.0 0.255.255.255 area 1
!
router bgp 2
 bgp router-id 2.1.1.1
 bgp log-neighbor-changes
 neighbor as2 peer-group
 neighbor as2 remote-as 2
 neighbor 2.1.2.1 peer-group as2
 neighbor 2.1.2.1 update-source Loopback0
 neighbor 2.1.2.2 peer-group as2
 neighbor 2.1.2.2 update-source Loopback0
 !
 address-family ipv4
  bgp dampening
  bgp additional-paths select all
  bgp additional-paths send receive
  aggregate-address 2.128.0.0 255.255.0.0 summary-only
  neighbor as2 send-community
  neighbor as2 advertise additional-paths all
  neighbor 2.1.2.1 activate
  neighbor 2.1.2.2 activate
  ! maximum-paths eibgp 5
 exit-address-family
!
ip forward-protocol nd
!
ip bgp-community new-format
ip community-list expanded as1_community permit _1:
ip community-list expanded as2_community permit _2:
ip community-list expanded as3_community permit _3:
!
no ip http server
no ip http secure-server
!
ip access-list extended INSIDE_TO_AS1
 permit ip 2.0.0.0 0.255.255.255 1.0.0.0 0.255.255.255
 permit ip 10.12.11.2 0.0.0.0 10.12.11.1 0.0.0.0 
 deny   ip any any
ip access-list extended OUTSIDE_TO_INSIDE
 permit tcp any 2.128.0.0 0.0.1.255 eq ssh
 permit udp any 2.0.0.0 0.255.255.255
 deny ip any any
!
!
ip prefix-list inbound_route_filter seq 5 deny 2.0.0.0/8 le 32
ip prefix-list inbound_route_filter seq 10 permit 0.0.0.0/0 le 32
!
ip prefix-list outbound_routes seq 5 permit 2.128.0.0/9 ge 16
access-list 101 permit ip host 1.0.1.0 host 255.255.255.0
access-list 101 permit ip host 1.0.2.0 host 255.255.255.0
access-list 103 permit ip host 3.0.1.0 host 255.255.255.0
access-list 103 permit ip host 3.0.2.0 host 255.255.255.0
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end

```
设备配置文件转换为等效的JunOS配置，生成所有设备完整的配置文件
