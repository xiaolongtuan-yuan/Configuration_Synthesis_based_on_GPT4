已知网络中所有设备的配置文件如下:

## configs/leaf1.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
multilink bundle-name authenticated
!
!
ip tcp synwait-time 5
!
interface Loopback0
 ip address 2.1.1.2 255.255.255.255
!
interface GigabitEthernet0/0
 ip address 2.34.101.4 255.255.255.0
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.34.201.4 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.128.0.2 255.255.255.252
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.128.1.2 255.255.255.252
 negotiation auto
!
router ospf 1
 network 2.1.1.2 0.0.0.0 area 0
 network 2.34.101.0 0.0.0.255 area 0
 network 2.34.201.0 0.0.0.255 area 0
 network 2.128.0.0 0.0.0.3 area 0
 network 2.128.1.0 0.0.0.3 area 0
!
ip route 0.0.0.0 0.0.0.0 GigabitEthernet2/0
!
end

```

## configs/core2.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
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
ip tcp synwait-time 5
!
router ospf 1
 network 2.1.2.2 0.0.0.0 area 0
 network 2.12.22.2 0.0.0.255 area 0
 network 2.12.12.2 0.0.0.255 area 0
 network 2.23.22.2 0.0.0.255 area 0
 network 2.23.21.2 0.0.0.255 area 0
 network 2.128.0.0 0.0.0.3 area 1
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
 ip address 2.12.22.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.12.12.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.23.22.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.23.21.2 255.255.255.0
 negotiation auto
!
ip route 0.0.0.0 0.0.0.0 2.12.22.1
ip route 2.128.0.0 255.255.255.252 2.23.22.3 10
ip route 2.128.1.0 255.255.255.252 2.23.21.3 10
!
end

```

## configs/core1.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
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
ip tcp synwait-time 5
!
router ospf 1
 network 2.1.2.1 0.0.0.0 area 0
 network 2.12.11.2 0.0.0.255 area 0
 network 2.12.21.2 0.0.0.255 area 0
 network 2.23.11.2 0.0.0.255 area 0
 network 2.23.12.2 0.0.0.255 area 0
 network 10.12.11.2 0.0.0.255 area 0
 network 2.128.1.0 0.0.0.3 area 1
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
 negotiation auto
!
interface GigabitEthernet1/0
 ip address 2.12.21.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet2/0
 ip address 2.23.11.2 255.255.255.0
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 2.23.12.2 255.255.255.0
 negotiation auto
!
ip route 0.0.0.0 0.0.0.0 2.12.11.1
ip route 2.128.0.0 255.255.255.0 2.23.11.3
ip route 2.128.1.0 255.255.255.0 2.23.12.3
!
end

```

## configs/spine2.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
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
ip tcp synwait-time 5
!
router ospf 1
 network 2.1.3.2 0.0.0.0 area 0
 network 2.23.22.3 0.0.0.255 area 0
 network 2.23.12.3 0.0.0.255 area 0
 network 2.34.201.3 0.0.0.255 area 0
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
 redistribute connected subnets
 network 2.1.3.2 0.0.0.0 area 0
 network 2.23.22.3 0.0.0.255 area 0
 network 2.23.12.3 0.0.0.255 area 0
 network 2.34.201.3 0.0.0.255 area 0
!
end

```

## configs/border2.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
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
router ospf 1
 network 2.1.1.2 0.0.0.0 area 0
 network 10.23.21.2 0.0.0.255 area 0
 network 2.12.22.1 0.0.0.255 area 0
 network 2.12.21.1 0.0.0.255 area 0
 network 2.128.0.0 0.0.0.3 area 1
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
 area 0 range 2.128.0.0 255.255.0.0
!
ip route 0.0.0.0 0.0.0.0 2.12.22.2
ip route 2.128.0.0 255.255.255.252 2.12.21.2 10
!
end

```

## configs/spine1.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
no ip domain lookup
ip domain name lab.local
no ipv6 cef
!
multilink bundle-name authenticated
!
!
ip tcp synwait-time 5
!
router ospf 1
 network 2.1.3.1 0.0.0.0 area 0
 network 2.23.11.3 0.0.0.255 area 0
 network 2.23.21.3 0.0.0.255 area 0
 network 2.34.101.3 0.0.0.255 area 0
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
end

```

## configs/border1.cfg

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
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
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
router ospf 1
 network 2.1.1.1 0.0.0.0 area 0
 network 10.12.11.2 0.0.0.255 area 0
 network 2.12.11.1 0.0.0.255 area 0
 network 2.12.12.1 0.0.0.255 area 0
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
end

```

## hosts/host-www.json

```
{
	"hostname" : "host-www",
	"hostInterfaces" : {
		"eth0" : {
			"name": "eth0",
      "prefix" : "2.128.1.1/30",
      "gateway" : "2.128.1.2"
		}
	}
}

```

## hosts/host-db.json

```
{
	"hostname" : "host-db",
	"hostInterfaces" : {
		"eth0" : {
			"name": "eth0",
      "prefix" : "2.128.0.1/30",
      "gateway": "2.128.0.2"
		}
	}
}

```

