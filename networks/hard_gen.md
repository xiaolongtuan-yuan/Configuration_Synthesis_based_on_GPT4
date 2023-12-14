已知网络中包含以下设备组件
2个主机：host1,host2
13个交换机：as1core1,as1border1,as1border2,as3core1,as3border1,as3border2,as2core1,as2core2,as2border1,as2border2,as2dist1,as2dist2
且该网络被划分为3个自治系统AS1,AS2,AS3，其中：
AS1包含设备：as1core1,as1border1,as1border2
AS2包含设备：host1,host2,as2core1,as2core2,as2border1,as2border2,as2dist1,as2dist2
AS3包含设备：as3core1,as3border1,as3border2
网络拓扑图的边由下列设备对组成
[as1core1, as1border1], [as1core1, as1border2], [as1border1, as2border1], [as1border2, as3border2],
[as3border2, as3core1], [as3core1, as3border1], [as3border1, as2border2],
[as2border2,as2core1 ], [as2border2, as2core2], [as2border1, as2core1], [as2border1, as2core2],
[as2core1, as2dist1], [as2core1, as2dist2], [as2core2, as2dist1], [as2core1, as2dist2],
[as2dist1, as2dept1], [as2dist2, as2dept1], [as2dept1, host1], [as2dept1, host2]
根据设备连接关系，基于Cisco IOS为所有设备生成完整的设备配置文件
以下是所有设备的基本配置文件，其中包括了设备名及接口IP地址的分配，在此基础上扩充配置文件使其能够正常运行起来，
只考虑OSPF和BGP协议， 要求网络的路由转发平面满足下列路由策略：
1. AS1中的设备都能到达host1
2. 从as1core1到主机host1不可以经过AS3中的设备
3. AS3的设备要到达主机必须经过as2core2

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
!
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
!
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
!
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
!
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
interface GigabitEthernet2/0
 ip address 90.90.90.1 255.255.255.0
 negotiation auto
!
interface GigabitEthernet3/0
 ip address 90.90.90.2 255.255.255.0
 negotiation auto
!
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
!
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
!
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
!
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
!
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

