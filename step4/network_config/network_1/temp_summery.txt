已知网络中所有设备的配置文件如下:

## configs/as3border1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as3border1
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
ip tcp synwait-time 5
!
!
interface Loopback0
 ip address 3.1.1.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 3.0.1.1 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 10.23.21.3 255.255.255.0
 negotiation auto
!
router ospf 1
 network 3.1.1.1 0.0.0.0 area 0
 network 3.0.1.0 0.0.0.255 area 0
 network 10.23.21.0 0.0.0.255 area 0
!
router bgp 65003
 bgp log-neighbor-changes
 network 3.1.1.1 mask 255.255.255.255
 neighbor 3.0.1.2 remote-as 65003
 redistribute ospf 1
!
end

```

## configs/as1core1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as1core1
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
ip tcp synwait-time 5
!
!
!
!
interface Loopback0
 ip address 1.10.1.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 1.0.2.2 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 1.0.1.2 255.255.255.0
 negotiation auto
!
router ospf 1
 network 1.10.1.1 0.0.0.0 area 0
 network 1.0.2.0 0.0.0.255 area 0
 network 1.0.1.0 0.0.0.255 area 0
!
ip route 2.128.0.0 255.255.255.0 1.0.1.1 name TO-HOST1
!
end

```

## configs/as3border2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as3border2
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
ip tcp synwait-time 5
!
!
interface Loopback0
 ip address 3.2.2.2 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 10.13.22.3 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 3.0.2.1 255.255.255.0
 negotiation auto
!
router ospf 1
 network 3.2.2.2 0.0.0.0 area 0
 network 10.13.22.0 0.0.0.255 area 0
 network 3.0.2.0 0.0.0.255 area 0
!
router bgp 65003
 bgp log-neighbor-changes
 network 3.2.2.2 mask 255.255.255.255
 neighbor 3.0.2.2 remote-as 65003
 redistribute ospf 1
 neighbor 10.13.22.1 remote-as 65001
!
end

```

## configs/as1border1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as1border1
!
boot-start-marker
boot-end-marker
!
!
!no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
ip tcp synwait-time 5
!
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 1.0.1.1 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 10.12.11.1 255.255.255.0
 negotiation auto
!
router ospf 1
 network 1.1.1.1 0.0.0.0 area 0
 network 1.0.1.0 0.0.0.255 area 0
 network 10.12.11.0 0.0.0.255 area 0
!
router bgp 65001
 bgp log-neighbor-changes
 network 1.1.1.1 mask 255.255.255.255
 neighbor 10.12.11.2 remote-as 65002
!
end

```

## configs/as1border2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as1border2
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
ip tcp synwait-time 5
!
!
!
interface Loopback0
 ip address 1.2.2.2 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 10.13.22.1 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 1.0.2.1 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 10.14.22.1 255.255.255.0
 negotiation auto
!
router ospf 1
 network 1.2.2.2 0.0.0.0 area 0
 network 1.0.2.0 0.0.0.255 area 0
 network 10.13.22.0 0.0.0.255 area 0
 network 10.14.22.0 0.0.0.255 area 0
!
router bgp 65001
 bgp log-neighbor-changes
 network 1.2.2.2 mask 255.255.255.255
 neighbor 10.13.22.3 remote-as 65003
!
end

```

## configs/as2dist1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2dist1
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
ip tcp synwait-time 5
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
router ospf 100
 network 2.1.3.1 0.0.0.0 area 0
 network 2.23.11.0 0.0.0.255 area 0
 network 2.23.21.0 0.0.0.255 area 0
 network 2.34.101.0 0.0.0.255 area 0
!
end

```

## configs/as3core1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as3core1
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
ip tcp synwait-time 5
!
!
interface Loopback0
 ip address 3.10.1.1 255.255.255.255
!
interface Ethernet0/0
 no ip address
 shutdown
 duplex auto
!
interface GigabitEthernet0/0
 ip address 3.0.2.2 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 3.0.1.2 255.255.255.0
 negotiation auto
!
router ospf 1
 network 3.10.1.1 0.0.0.0 area 0
 network 3.0.2.0 0.0.0.255 area 0
 network 3.0.1.0 0.0.0.255 area 0
!
router bgp 65003
 bgp log-neighbor-changes
 network 3.10.1.1 mask 255.255.255.255
 neighbor 10.23.21.3 remote-as 65002
 redistribute ospf 1
!
end

```

## configs/as2core1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2core1
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
ip tcp synwait-time 5
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
!
interface GigabitEthernet1/0
 ip address 2.12.21.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.23.11.2 255.255.255.0
 ip access-group blocktelnet in
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.23.12.2 255.255.255.0
 ip access-group blocktelnet in
 negotiation auto
!
router ospf 100
 network 2.1.2.1 0.0.0.0 area 0
 network 2.12.11.0 0.0.0.255 area 0
 network 2.12.21.0 0.0.0.255 area 0
 network 2.23.11.0 0.0.0.255 area 0
 network 2.23.12.0 0.0.0.255 area 0
!
router bgp 65002
 bgp log-neighbor-changes
 network 2.1.2.1 mask 255.255.255.255
 neighbor 10.12.11.1 remote-as 65001
 neighbor 10.23.21.2 remote-as 65003
!
end

```

## configs/as2border1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2border1
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
ip tcp synwait-time 5
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
router ospf 100
 network 2.1.1.1 0.0.0.0 area 0
 network 10.12.11.0 0.0.0.255 area 0
 network 2.12.11.0 0.0.0.255 area 0
 network 2.12.12.0 0.0.0.255 area 0
!
router bgp 65002
 bgp log-neighbor-changes
 network 2.1.1.1 mask 255.255.255.255
 neighbor 10.12.11.1 remote-as 65001
!
end

```

## configs/as2dist2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2dist2
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
ip tcp synwait-time 5
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
router ospf 100
 network 2.1.3.2 0.0.0.0 area 0
 network 2.23.22.0 0.0.0.255 area 0
 network 2.23.12.0 0.0.0.255 area 0
 network 2.34.201.0 0.0.0.255 area 0
!
end

```

## configs/as2core2.cfg

```
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2core2
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
ip tcp synwait-time 5
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
!
interface GigabitEthernet1/0
 mtu 1600
 ip address 2.12.12.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 mtu 1700
 ip address 2.23.22.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.23.21.2 255.255.255.0
 negotiation auto
!
router ospf 100
 network 2.1.2.2 0.0.0.0 area 0
 network 2.12.22.0 0.0.0.255 area 0
 network 2.12.12.0 0.0.0.255 area 0
 network 2.23.22.0 0.0.0.255 area 0
 network 2.23.21.0 0.0.0.255 area 0
!
router bgp 65002
 bgp log-neighbor-changes
 network 2.1.2.2 mask 255.255.255.255
 neighbor 10.23.21.3 remote-as 65003
 neighbor 3.0.1.2 route-map RMAP_TO_HOST1 out
 redistribute connected
 redistribute ospf 100
!
ip route 2.128.0.0 255.255.255.0 2.34.101.3 name TO-HOST1
!
route-map RMAP_TO_HOST1 permit 10
 match ip address ACL_TO_HOST1
 set ip next-hop 2.34.101.3
!
access-list ACL_TO_HOST1 permit ip host 3.10.1.1 host 2.128.0.101
access-list ACL_TO_HOST1 permit ip host 3.1.1.1 host 2.128.0.101
access-list ACL_TO_HOST1 permit ip host 3.2.2.2 host 2.128.0.101
access-list ACL_TO_HOST1 deny   ip any any
!
end

```

## configs/as2border2.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2border2
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
ip tcp synwait-time 5
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
router ospf 100
 network 2.1.1.2 0.0.0.0 area 0
 network 10.23.21.0 0.0.0.255 area 0
 network 2.12.22.0 0.0.0.255 area 0
 network 2.12.21.0 0.0.0.255 area 0
!
router bgp 65002
 bgp log-neighbor-changes
 network 2.1.1.2 mask 255.255.255.255
 neighbor 10.23.21.3 remote-as 65003
!
end

```

## configs/as2dept1.cfg

```

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname as2dept1
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
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
ip tcp synwait-time 5
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
 ip address 2.34.101.4 255.255.255.0
 media-type gbic
 speed 1000
 duplex full
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.34.201.4 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.128.0.1 255.255.255.0
 ip access-group RESTRICT_HOST_TRAFFIC_IN in
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.128.1.1 255.255.255.0
 ip access-group RESTRICT_HOST_TRAFFIC_IN in
 negotiation auto
!
!
end

```

## hosts/host2.json

```
{
	"hostname" : "host2",
	"iptablesFile" : "iptables/host2.iptables",
	"hostInterfaces" : {
		"eth0" : {
			"name": "eth0",
      "prefix" : "2.128.1.101/24",
      "gateway" : "2.128.1.1"
		}
	}
}

```

## hosts/host1.json

```
{
	"hostname" : "host1",
	"iptablesFile" : "iptables/host1.iptables",
	"hostInterfaces" : {
		"eth0" : {
			"name": "eth0",
      "prefix" : "2.128.0.101/24",
      "gateway": "2.128.0.1"
		}
	}
}

```

