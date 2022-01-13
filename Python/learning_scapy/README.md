# [Scapyの勉強](https://scapy.readthedocs.io/en/latest/usage.html)

## scapyを起動
```python
from scapy.all import *
```
でインポートしてコードをかけるが，
```scapy```とコマンドラインに売って使った方が便利

## スタッキングレイヤー
/演算子は2つのレイヤー間の合成演算子として使用される．
その際，階層では，上位層に応じて１つ移譲のデフォルトフィールドがオーバーロードされる．

例えば，IP()/TCP()ではIPとTCPでパケットを生成する．/を使うことで，複数のレイヤのパケットを作れる

各フィールドに対応している変数はls(クラス名)で調べられる
ex)```ls(Ether)```
Ether: SrcMacAddr,DstMacAddr ```Ether(src="",dst="")```
IP: SrcIPAddr,DstIPAddr ```IP(src="",dst="")```
TCP: Src port,Dst port,Flag:SYN ```TCP(sport=1111,dport=1111,flags='S')```


```
>>>IP()
<IP |>
>>>IP()/TCP()
<IP frag=0 proto=TCP |<TCP |>>
>>>Ether()/IP()/TCP()
<Ether type=0x800 |<IP frag=0 proto=TCP |<TCP |>>>
>>>IP()/TCP()/"GET / HTTP/1.0\r\n\r\n"
<IP frag=0 proto=TCP |<TCP |<Raw load='GET / HTTP/1.0\r\n\r\n' |>>>
>>>Ether()/IP()/IP()/UDP()
<Ether type=0x800 |<IP frag=0 proto=IP |<IP frag=0 proto=UDP |<UDP |>>>>
>>>IP(proto=55)/TCP()
<IP frag=0 proto=55 |<TCP |>>
```

```
>>> raw(IP())
'E\x00\x00\x14\x00\x01\x00\x00@\x00|\xe7\x7f\x00\x00\x01\x7f\x00\x00\x01'
>>> IP(_)
<IP version=4L ihl=5L tos=0x0 len=20 id=1 flags= frag=0L ttl=64 proto=IP
 chksum=0x7ce7 src=127.0.0.1 dst=127.0.0.1 |>
 >>> a=Ether()/IP(dst="www.slashdot.org")/TCP()/"GET /index.html HTTP/1.0 \n\n"
 >>> hexdump(a)
00 02 15 37 A2 44 00 AE F3 52 AA D1 08 00 45 00  ...7.D...R....E.
00 43 00 01 00 00 40 06 78 3C C0 A8 05 15 42 23  .C....@.x<....B#
FA 97 00 14 00 50 00 00 00 00 00 00 00 00 50 02  .....P........P.
20 00 BB 39 00 00 47 45 54 20 2F 69 6E 64 65 78   ..9..GET /index
2E 68 74 6D 6C 20 48 54 54 50 2F 31 2E 30 20 0A  .html HTTP/1.0 .
0A                                               .
>>> b=raw(a)
>>> b
'\x00\x02\x157\xa2D\x00\xae\xf3R\xaa\xd1\x08\x00E\x00\x00C\x00\x01\x00\x00@\x06x<\xc0
 \xa8\x05\x15B#\xfa\x97\x00\x14\x00P\x00\x00\x00\x00\x00\x00\x00\x00P\x02 \x00
 \xbb9\x00\x00GET /index.html HTTP/1.0 \n\n'
>>> c=Ether(b)
>>> c
<Ether dst=00:02:15:37:a2:44 src=00:ae:f3:52:aa:d1 type=0x800 |<IP version=4L
 ihl=5L tos=0x0 len=67 id=1 flags= frag=0L ttl=64 proto=TCP chksum=0x783c
 src=192.168.5.21 dst=66.35.250.151 options='' |<TCP sport=20 dport=80 seq=0L
 ack=0L dataofs=5L reserved=0L flags=S window=8192 chksum=0xbb39 urgptr=0
 options=[] |<Raw load='GET /index.html HTTP/1.0 \n\n' |>>>>

>>> c.hide_defaults()
>>> c
<Ether dst=00:0f:66:56:fa:d2 src=00:ae:f3:52:aa:d1 type=0x800 |<IP ihl=5L len=67
 frag=0 proto=TCP chksum=0x783c src=192.168.5.21 dst=66.35.250.151 |<TCP dataofs=5L
 chksum=0xbb39 options=[] |<Raw load='GET /index.html HTTP/1.0 \n\n' |>>>>
```

## パケットを送る
```python
# ICMPパケットを生成
packet = IP(dst='')/ICMP(type=8)
#　パケット送信
send(packet)
```
send()で送信が可能，send()の場合，L2プロトコルは自動で調整される．

## 帰ってきたパケットをみる
```python
# 送るパケットを見る
sr(packet)

#最初に帰ってきたパケットをみる
sr1(packet)

```

```python
# 変数にも保存可能
r_packet = sr1(packet)
```

```python
# 引数には初期値を指定
send(packet,count=1,inter=1,iface=N) #L3でのパケット送信
sendp(packet,count1,inter=1,iface=N) #L2でのパケット送信
sendfast(packet,pps=N,mbps=N,iface=N) #tcpreplayを使って送信
sr(packet,filter=N,iface=N) #L3でパケットを送信し，返信を全て受信する．
srp(packet,filter=N,iface=N) #L2でパケットを送信し，返信を全て受信する．
sr1(packet,filter=N,iface=N) #L3でパケットを送信し，返答を１つだけ受信
srp1(packet,filter=N,iface=N) #L2でパケットを送信し，返答を一つだけ受信
srflood(packet,filter=N,iface=N) #L3でパケットを大量に送信し，返信を全て受信
srpflood(packet,filter=N,iface=N) #L2でパケットを大量に送信し，返信を全て受信
```
ちなみに，L2:OSIの第２層，MACアドレス使う
L3:OSIの３層　IPアドレスを使う




## Pcapファイルの読み取り，解析
```python
packets = rdpcap('filepath')
packets
packets[1] #n-1で指定　添字は0から

packets[0]['IP'] #packet0のIPを見る
packets[0]['IP'].src #送信元IPアドレスを表示
packets.summary() #wireshark 的な見え方

```
繰り返しとか使って，特定のパケットのみ取り出したりできる
```python
for p in packets:
	if p['Ethernet'].type == 0x800:
		if p['IP'].proto == 1:
			print p['Raw'].load
```



## Pcapに書き込む
```python
packet = Ether()/IP()/TCP()
wireshark(packet)
wrpcap('保存ファイル名',packet)
```
wrpcapで保存が可能．

## IP
IPアドレス
IPアドレスは答えの場所を探すヒント
### プライベートIPアドレス
オンラインCTF→ファイルの中に答え
オフラインCTF→そのアドレスにアクセスできる可能性

プライベートIPアドレスはIPv4のIPアドレス枯渇問題が背景にあり，登場した．
全てのデバイスが，インターネットからアクセスできる必要はないので，LAN内のコンピュータには一定の範囲のIPアドレスをプライベートIPアドレスとして割り当て，LANとWANを接続する機器にのみグローバルIPアドレスを割り当て，グローバルIPアドレスを節約する．

プライベートIPアドレスの範囲はRFC1918で規定されていて，通常はその範囲内で設定する．
クラスA:10.0.0.0~10.255.255.255 (10.0.0.0/8)
クラスB:172.16.0.0~172.31.255.255(172.16.0.0/12)
クラスC:192.168.0.0~192.168.255.255(192.168.0.0/16)


### グローバルIPアドレス
オンラインCTF→アドレスにアクセスできる可能性
オフラインCTF→ファイルの中に答えがある可能性

インターネットを利用する時に割り振られるIPアドレス．
グローバルIPアドレスは，インターネットで相手と通信するために持つ，他のアドレスとは重複しない一意のIPアドレスのこと．TCP/IPでは，通信相手を特定してIPパケットを送信したり，ルーティングしたりするために必要となる．

## 対応プロトコル
ls()で対応プロトコルを探すことができる．
AH         : AH
AKMSuite   : AKM suite
ARP        : ARP
ASN1P_INTEGER : None
ASN1P_OID  : None
ASN1P_PRIVSEQ : None
ASN1_Packet : None
ATT_Error_Response : Error Response
ATT_Exchange_MTU_Request : Exchange MTU Request
ATT_Exchange_MTU_Response : Exchange MTU Response
ATT_Execute_Write_Request : Execute Write Request
ATT_Execute_Write_Response : Execute Write Response
ATT_Find_By_Type_Value_Request : Find By Type Value Request
ATT_Find_By_Type_Value_Response : Find By Type Value Response
ATT_Find_Information_Request : Find Information Request
ATT_Find_Information_Response : Find Information Response
ATT_Handle : ATT Short Handle
ATT_Handle_UUID128 : ATT Handle (UUID 128)
ATT_Handle_Value_Indication : Handle Value Indication
ATT_Handle_Value_Notification : Handle Value Notification
ATT_Handle_Variable : None
ATT_Hdr    : ATT header
ATT_Prepare_Write_Request : Prepare Write Request
ATT_Prepare_Write_Response : Prepare Write Response
ATT_Read_Blob_Request : Read Blob Request
ATT_Read_Blob_Response : Read Blob Response
ATT_Read_By_Group_Type_Request : Read By Group Type Request
ATT_Read_By_Group_Type_Response : Read By Group Type Response
ATT_Read_By_Type_Request : Read By Type Request
ATT_Read_By_Type_Request_128bit : Read By Type Request
ATT_Read_By_Type_Response : Read By Type Response
ATT_Read_Multiple_Request : Read Multiple Request
ATT_Read_Multiple_Response : Read Multiple Response
ATT_Read_Request : Read Request
ATT_Read_Response : Read Response
ATT_Write_Command : Write Request
ATT_Write_Request : Write Request
ATT_Write_Response : Write Response
BOOTP      : BOOTP
BTLE       : BT4LE
BTLE_ADV   : BTLE advertising header
BTLE_ADV_DIRECT_IND : BTLE ADV_DIRECT_IND
BTLE_ADV_IND : BTLE ADV_IND
BTLE_ADV_NONCONN_IND : BTLE ADV_NONCONN_IND
BTLE_ADV_SCAN_IND : BTLE ADV_SCAN_IND
BTLE_CONNECT_REQ : BTLE connect request
BTLE_CTRL  : BTLE_CTRL
BTLE_DATA  : BTLE data header
BTLE_EMPTY_PDU : Empty data PDU
BTLE_PPI   : BTLE PPI header
BTLE_RF    : BTLE RF info header
BTLE_SCAN_REQ : BTLE scan request
BTLE_SCAN_RSP : BTLE scan response
CookedLinux : cooked linux
DHCP       : DHCP options
DHCP6      : DHCPv6 Generic Message
DHCP6OptAuth : DHCP6 Option - Authentication
DHCP6OptBCMCSDomains : DHCP6 Option - BCMCS Domain Name List
DHCP6OptBCMCSServers : DHCP6 Option - BCMCS Addresses List
DHCP6OptBootFileUrl : DHCP6 Boot File URL Option
DHCP6OptClientArchType : DHCP6 Client System Architecture Type Option
DHCP6OptClientFQDN : DHCP6 Option - Client FQDN
DHCP6OptClientId : DHCP6 Client Identifier Option
DHCP6OptClientLinkLayerAddr : DHCP6 Option - Client Link Layer address
DHCP6OptClientNetworkInterId : DHCP6 Client Network Interface Identifier Option
DHCP6OptDNSDomains : DHCP6 Option - Domain Search List option
DHCP6OptDNSServers : DHCP6 Option - DNS Recursive Name Server
DHCP6OptERPDomain : DHCP6 Option - ERP Domain Name List
DHCP6OptElapsedTime : DHCP6 Elapsed Time Option
DHCP6OptGeoConf : DHCP6 Option - Civic Location
DHCP6OptGeoConfElement : None
DHCP6OptIAAddress : DHCP6 IA Address Option (IA_TA or IA_NA suboption)
DHCP6OptIAPrefix : DHCP6 Option - IA Prefix option
DHCP6OptIA_NA : DHCP6 Identity Association for Non-temporary Addresses Option
DHCP6OptIA_PD : DHCP6 Option - Identity Association for Prefix Delegation
DHCP6OptIA_TA : DHCP6 Identity Association for Temporary Addresses Option
DHCP6OptIfaceId : DHCP6 Interface-Id Option
DHCP6OptInfoRefreshTime : DHCP6 Option - Information Refresh Time
DHCP6OptLQClientLink : DHCP6 Client Link Option
DHCP6OptMudUrl : DHCP6 Option - MUD URL
DHCP6OptNISDomain : DHCP6 Option - NIS Domain Name
DHCP6OptNISPDomain : DHCP6 Option - NIS+ Domain Name
DHCP6OptNISPServers : DHCP6 Option - NIS+ Servers
DHCP6OptNISServers : DHCP6 Option - NIS Servers
DHCP6OptNewPOSIXTimeZone : DHCP6 POSIX Timezone Option
DHCP6OptNewTZDBTimeZone : DHCP6 TZDB Timezone Option
DHCP6OptOptReq : DHCP6 Option Request Option
DHCP6OptPanaAuthAgent : DHCP6 PANA Authentication Agent Option
DHCP6OptPref : DHCP6 Preference Option
DHCP6OptRapidCommit : DHCP6 Rapid Commit Option
DHCP6OptReconfAccept : DHCP6 Reconfigure Accept Option
DHCP6OptReconfMsg : DHCP6 Reconfigure Message Option
DHCP6OptRelayAgentERO : DHCP6 Option - RelayRequest Option
DHCP6OptRelayMsg : DHCP6 Relay Message Option
DHCP6OptRelaySuppliedOpt : DHCP6 Relay-Supplied Options Option
DHCP6OptRemoteID : DHCP6 Option - Relay Agent Remote-ID
DHCP6OptSIPDomains : DHCP6 Option - SIP Servers Domain Name List
DHCP6OptSIPServers : DHCP6 Option - SIP Servers IPv6 Address List
DHCP6OptSNTPServers : DHCP6 option - SNTP Servers
DHCP6OptServerId : DHCP6 Server Identifier Option
DHCP6OptServerUnicast : DHCP6 Server Unicast Option
DHCP6OptStatusCode : DHCP6 Status Code Option
DHCP6OptSubscriberID : DHCP6 Option - Subscriber ID
DHCP6OptUnknown : Unknown DHCPv6 Option
DHCP6OptUserClass : DHCP6 User Class Option
DHCP6OptVSS : DHCP6 Option - Virtual Subnet Selection
DHCP6OptVendorClass : DHCP6 Vendor Class Option
DHCP6OptVendorSpecificInfo : DHCP6 Vendor-specific Information Option
DHCP6_Advertise : DHCPv6 Advertise Message
DHCP6_Confirm : DHCPv6 Confirm Message
DHCP6_Decline : DHCPv6 Decline Message
DHCP6_InfoRequest : DHCPv6 Information Request Message
DHCP6_Rebind : DHCPv6 Rebind Message
DHCP6_Reconf : DHCPv6 Reconfigure Message
DHCP6_RelayForward : DHCPv6 Relay Forward Message (Relay Agent/Server Message)
DHCP6_RelayReply : DHCPv6 Relay Reply Message (Relay Agent/Server Message)
DHCP6_Release : DHCPv6 Release Message
DHCP6_Renew : DHCPv6 Renew Message
DHCP6_Reply : DHCPv6 Reply Message
DHCP6_Request : DHCPv6 Request Message
DHCP6_Solicit : DHCPv6 Solicit Message
DIR_PPP    : None
DNS        : DNS
DNSQR      : DNS Question Record
DNSRR      : DNS Resource Record
DNSRRDLV   : DNS DLV Resource Record
DNSRRDNSKEY : DNS DNSKEY Resource Record
DNSRRDS    : DNS DS Resource Record
DNSRRMX    : DNS MX Resource Record
DNSRRNSEC  : DNS NSEC Resource Record
DNSRRNSEC3 : DNS NSEC3 Resource Record
DNSRRNSEC3PARAM : DNS NSEC3PARAM Resource Record
DNSRROPT   : DNS OPT Resource Record
DNSRRRSIG  : DNS RRSIG Resource Record
DNSRRSOA   : DNS SOA Resource Record
DNSRRSRV   : DNS SRV Resource Record
DNSRRTSIG  : DNS TSIG Resource Record
DUID_EN    : DUID - Assigned by Vendor Based on Enterprise Number
DUID_LL    : DUID - Based on Link-layer Address
DUID_LLT   : DUID - Link-layer address plus time
DUID_UUID  : DUID - Based on UUID
Dot11      : 802.11
Dot11ATIM  : 802.11 ATIM
Dot11Ack   : 802.11 Ack packet
Dot11AssoReq : 802.11 Association Request
Dot11AssoResp : 802.11 Association Response
Dot11Auth  : 802.11 Authentication
Dot11Beacon : 802.11 Beacon
Dot11CCMP  : 802.11 CCMP packet
Dot11Deauth : 802.11 Deauthentication
Dot11Disas : 802.11 Disassociation
Dot11Elt   : 802.11 Information Element
Dot11EltCountry : 802.11 Country
Dot11EltCountryConstraintTriplet : 802.11 Country Constraint Triplet
Dot11EltDSSSet : 802.11 DSSS Parameter Set
Dot11EltERP : 802.11 ERP
Dot11EltHTCapabilities : 802.11 HT Capabilities
Dot11EltMicrosoftWPA : 802.11 Microsoft WPA
Dot11EltRSN : 802.11 RSN information
Dot11EltRates : 802.11 Rates
Dot11EltVendorSpecific : 802.11 Vendor Specific
Dot11Encrypted : 802.11 Encrypted (unknown algorithm)
Dot11FCS   : 802.11-FCS
Dot11ProbeReq : 802.11 Probe Request
Dot11ProbeResp : 802.11 Probe Response
Dot11QoS   : 802.11 QoS
Dot11ReassoReq : 802.11 Reassociation Request
Dot11ReassoResp : 802.11 Reassociation Response
Dot11TKIP  : 802.11 TKIP packet
Dot11WEP   : 802.11 WEP packet
Dot15d4    : 802.15.4
Dot15d4Ack : 802.15.4 Ack
Dot15d4AuxSecurityHeader : 802.15.4 Auxiliary Security Header
Dot15d4Beacon : 802.15.4 Beacon
Dot15d4Cmd : 802.15.4 Command
Dot15d4CmdAssocReq : 802.15.4 Association Request Payload
Dot15d4CmdAssocResp : 802.15.4 Association Response Payload
Dot15d4CmdCoordRealign : 802.15.4 Coordinator Realign Command
Dot15d4CmdCoordRealignPage : 802.15.4 Coordinator Realign Page
Dot15d4CmdDisassociation : 802.15.4 Disassociation Notification Payload
Dot15d4CmdGTSReq : 802.15.4 GTS request command
Dot15d4Data : 802.15.4 Data
Dot15d4FCS : 802.15.4 - FCS
Dot1AD     : 802_1AD
Dot1Q      : 802.1Q
Dot3       : 802.3
EAP        : EAP
EAPOL      : EAPOL
EAP_FAST   : EAP-FAST
EAP_MD5    : EAP-MD5
EAP_PEAP   : PEAP
EAP_TLS    : EAP-TLS
EAP_TTLS   : EAP-TTLS
ECCurve    : None
ECDSAPrivateKey : None
ECDSAPrivateKey_OpenSSL : ECDSA Params + Private Key
ECDSAPublicKey : None
ECDSASignature : None
ECFieldID  : None
ECParameters : None
ECSpecifiedDomain : None
EDNS0TLV   : DNS EDNS0 TLV
EIR_CompleteList128BitServiceUUIDs : Complete list of 128-bit service UUIDs
EIR_CompleteList16BitServiceUUIDs : Complete list of 16-bit service UUIDs
EIR_CompleteLocalName : Complete Local Name
EIR_Device_ID : Device ID
EIR_Element : EIR Element
EIR_Flags  : Flags
EIR_Hdr    : EIR Header
EIR_IncompleteList128BitServiceUUIDs : Incomplete list of 128-bit service UUIDs
EIR_IncompleteList16BitServiceUUIDs : Incomplete list of 16-bit service UUIDs
EIR_Manufacturer_Specific_Data : EIR Manufacturer Specific Data
EIR_Raw    : EIR Raw
EIR_ServiceData16BitUUID : EIR Service Data - 16-bit UUID
EIR_ShortenedLocalName : Shortened Local Name
EIR_TX_Power_Level : TX Power Level
ESP        : ESP
Ether      : Ethernet
EtherCat   : None
EtherCatAPRD : None
EtherCatAPRW : None
EtherCatAPWR : None
EtherCatARMW : None
EtherCatBRD : None
EtherCatBRW : None
EtherCatBWR : None
EtherCatFPRD : None
EtherCatFPRW : None
EtherCatFPWR : None
EtherCatFRMW : None
EtherCatLRD : None
EtherCatLRW : None
EtherCatLWR : None
EtherCatType12DLPDU : None
GPRS       : GPRSdummy
GRE        : GRE
GRE_PPTP   : GRE PPTP
GRErouting : GRE routing information
HAO        : Home Address Option
HBHOptUnknown : Scapy6 Unknown Option
HCI_ACL_Hdr : HCI ACL header
HCI_Cmd_Complete_LE_Read_White_List_Size : LE Read White List Size
HCI_Cmd_Complete_Read_BD_Addr : Read BD Addr
HCI_Cmd_Connect_Accept_Timeout : Connection Attempt Timeout
HCI_Cmd_Disconnect : Disconnect
HCI_Cmd_LE_Add_Device_To_White_List : LE Add Device to White List
HCI_Cmd_LE_Clear_White_List : LE Clear White List
HCI_Cmd_LE_Connection_Update : LE Connection Update
HCI_Cmd_LE_Create_Connection : LE Create Connection
HCI_Cmd_LE_Create_Connection_Cancel : LE Create Connection Cancel
HCI_Cmd_LE_Host_Supported : LE Host Supported
HCI_Cmd_LE_Long_Term_Key_Request_Negative_Reply : LE Long Term Key Request Negative Reply
HCI_Cmd_LE_Long_Term_Key_Request_Reply : LE Long Term Key Request Reply
HCI_Cmd_LE_Read_Buffer_Size : LE Read Buffer Size
HCI_Cmd_LE_Read_Remote_Used_Features : LE Read Remote Used Features
HCI_Cmd_LE_Read_White_List_Size : LE Read White List Size
HCI_Cmd_LE_Remove_Device_From_White_List : LE Remove Device from White List
HCI_Cmd_LE_Set_Advertise_Enable : LE Set Advertise Enable
HCI_Cmd_LE_Set_Advertising_Data : LE Set Advertising Data
HCI_Cmd_LE_Set_Advertising_Parameters : LE Set Advertising Parameters
HCI_Cmd_LE_Set_Random_Address : LE Set Random Address
HCI_Cmd_LE_Set_Scan_Enable : LE Set Scan Enable
HCI_Cmd_LE_Set_Scan_Parameters : LE Set Scan Parameters
HCI_Cmd_LE_Set_Scan_Response_Data : LE Set Scan Response Data
HCI_Cmd_LE_Start_Encryption_Request : LE Start Encryption
HCI_Cmd_Read_BD_Addr : Read BD Addr
HCI_Cmd_Reset : Reset
HCI_Cmd_Set_Event_Filter : Set Event Filter
HCI_Cmd_Set_Event_Mask : Set Event Mask
HCI_Cmd_Write_Extended_Inquiry_Response : Write Extended Inquiry Response
HCI_Cmd_Write_Local_Name : None
HCI_Command_Hdr : HCI Command header
HCI_Event_Command_Complete : Command Complete
HCI_Event_Command_Status : Command Status
HCI_Event_Disconnection_Complete : Disconnection Complete
HCI_Event_Encryption_Change : Encryption Change
HCI_Event_Hdr : HCI Event header
HCI_Event_LE_Meta : LE Meta
HCI_Event_Number_Of_Completed_Packets : Number Of Completed Packets
HCI_Hdr    : HCI header
HCI_LE_Meta_Advertising_Report : Advertising Report
HCI_LE_Meta_Advertising_Reports : Advertising Reports
HCI_LE_Meta_Connection_Complete : Connection Complete
HCI_LE_Meta_Connection_Update_Complete : Connection Update Complete
HCI_LE_Meta_Long_Term_Key_Request : Long Term Key Request
HCI_PHDR_Hdr : HCI PHDR transport layer
HDLC       : None
HSRP       : HSRP
HSRPmd5    : HSRP MD5 Authentication
ICMP       : ICMP
ICMPerror  : ICMP in ICMP
ICMPv6DestUnreach : ICMPv6 Destination Unreachable
ICMPv6EchoReply : ICMPv6 Echo Reply
ICMPv6EchoRequest : ICMPv6 Echo Request
ICMPv6HAADReply : ICMPv6 Home Agent Address Discovery Reply
ICMPv6HAADRequest : ICMPv6 Home Agent Address Discovery Request
ICMPv6MLDMultAddrRec : ICMPv6 MLDv2 - Multicast Address Record
ICMPv6MLDone : MLD - Multicast Listener Done
ICMPv6MLQuery : MLD - Multicast Listener Query
ICMPv6MLQuery2 : MLDv2 - Multicast Listener Query
ICMPv6MLReport : MLD - Multicast Listener Report
ICMPv6MLReport2 : MLDv2 - Multicast Listener Report
ICMPv6MPAdv : ICMPv6 Mobile Prefix Advertisement
ICMPv6MPSol : ICMPv6 Mobile Prefix Solicitation
ICMPv6MRD_Advertisement : ICMPv6 Multicast Router Discovery Advertisement
ICMPv6MRD_Solicitation : ICMPv6 Multicast Router Discovery Solicitation
ICMPv6MRD_Termination : ICMPv6 Multicast Router Discovery Termination
ICMPv6NDOptAdvInterval : ICMPv6 Neighbor Discovery - Interval Advertisement
ICMPv6NDOptDNSSL : ICMPv6 Neighbor Discovery Option - DNS Search List Option
ICMPv6NDOptDstLLAddr : ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address
ICMPv6NDOptEFA : ICMPv6 Neighbor Discovery Option - Expanded Flags Option
ICMPv6NDOptHAInfo : ICMPv6 Neighbor Discovery - Home Agent Information
ICMPv6NDOptIPAddr : ICMPv6 Neighbor Discovery - IP Address Option (FH for MIPv6)
ICMPv6NDOptLLA : ICMPv6 Neighbor Discovery - Link-Layer Address (LLA) Option (FH for MIPv6)
ICMPv6NDOptMAP : ICMPv6 Neighbor Discovery - MAP Option
ICMPv6NDOptMTU : ICMPv6 Neighbor Discovery Option - MTU
ICMPv6NDOptNewRtrPrefix : ICMPv6 Neighbor Discovery - New Router Prefix Information Option (FH for MIPv6)
ICMPv6NDOptPrefixInfo : ICMPv6 Neighbor Discovery Option - Prefix Information
ICMPv6NDOptRDNSS : ICMPv6 Neighbor Discovery Option - Recursive DNS Server Option
ICMPv6NDOptRedirectedHdr : ICMPv6 Neighbor Discovery Option - Redirected Header
ICMPv6NDOptRouteInfo : ICMPv6 Neighbor Discovery Option - Route Information Option
ICMPv6NDOptShortcutLimit : ICMPv6 Neighbor Discovery Option - NBMA Shortcut Limit
ICMPv6NDOptSrcAddrList : ICMPv6 Inverse Neighbor Discovery Option - Source Address List
ICMPv6NDOptSrcLLAddr : ICMPv6 Neighbor Discovery Option - Source Link-Layer Address
ICMPv6NDOptTgtAddrList : ICMPv6 Inverse Neighbor Discovery Option - Target Address List
ICMPv6NDOptUnknown : ICMPv6 Neighbor Discovery Option - Scapy Unimplemented
ICMPv6ND_INDAdv : ICMPv6 Inverse Neighbor Discovery Advertisement
ICMPv6ND_INDSol : ICMPv6 Inverse Neighbor Discovery Solicitation
ICMPv6ND_NA : ICMPv6 Neighbor Discovery - Neighbor Advertisement
ICMPv6ND_NS : ICMPv6 Neighbor Discovery - Neighbor Solicitation
ICMPv6ND_RA : ICMPv6 Neighbor Discovery - Router Advertisement
ICMPv6ND_RS : ICMPv6 Neighbor Discovery - Router Solicitation
ICMPv6ND_Redirect : ICMPv6 Neighbor Discovery - Redirect
ICMPv6NIQueryIPv4 : ICMPv6 Node Information Query - IPv4 Address Query
ICMPv6NIQueryIPv6 : ICMPv6 Node Information Query - IPv6 Address Query
ICMPv6NIQueryNOOP : ICMPv6 Node Information Query - NOOP Query
ICMPv6NIQueryName : ICMPv6 Node Information Query - IPv6 Name Query
ICMPv6NIReplyIPv4 : ICMPv6 Node Information Reply - IPv4 addresses
ICMPv6NIReplyIPv6 : ICMPv6 Node Information Reply - IPv6 addresses
ICMPv6NIReplyNOOP : ICMPv6 Node Information Reply - NOOP Reply
ICMPv6NIReplyName : ICMPv6 Node Information Reply - Node Names
ICMPv6NIReplyRefuse : ICMPv6 Node Information Reply - Responder refuses to supply answer
ICMPv6NIReplyUnknown : ICMPv6 Node Information Reply - Qtype unknown to the responder
ICMPv6PacketTooBig : ICMPv6 Packet Too Big
ICMPv6ParamProblem : ICMPv6 Parameter Problem
ICMPv6RPL  : RPL
ICMPv6TimeExceeded : ICMPv6 Time Exceeded
ICMPv6Unknown : Scapy6 ICMPv6 fallback class
IP         : IP
IPOption   : IP Option
IPOption_Address_Extension : IP Option Address Extension
IPOption_EOL : IP Option End of Options List
IPOption_LSRR : IP Option Loose Source and Record Route
IPOption_MTU_Probe : IP Option MTU Probe
IPOption_MTU_Reply : IP Option MTU Reply
IPOption_NOP : IP Option No Operation
IPOption_RR : IP Option Record Route
IPOption_Router_Alert : IP Option Router Alert
IPOption_SDBM : IP Option Selective Directed Broadcast Mode
IPOption_SSRR : IP Option Strict Source and Record Route
IPOption_Security : IP Option Security
IPOption_Stream_Id : IP Option Stream ID
IPOption_Timestamp : IP Option Timestamp
IPOption_Traceroute : IP Option Traceroute
IPerror    : IP in ICMP
IPerror6   : IPv6 in ICMPv6
IPv46      : IP
IPv6       : IPv6
IPv6ExtHdrDestOpt : IPv6 Extension Header - Destination Options Header
IPv6ExtHdrFragment : IPv6 Extension Header - Fragmentation header
IPv6ExtHdrHopByHop : IPv6 Extension Header - Hop-by-Hop Options Header
IPv6ExtHdrRouting : IPv6 Option Header Routing
IPv6ExtHdrSegmentRouting : IPv6 Option Header Segment Routing
IPv6ExtHdrSegmentRoutingTLV : IPv6 Option Header Segment Routing - Generic TLV
IPv6ExtHdrSegmentRoutingTLVEgressNode : IPv6 Option Header Segment Routing - Egress Node TLV
IPv6ExtHdrSegmentRoutingTLVHMAC : IPv6 Option Header Segment Routing - HMAC TLV
IPv6ExtHdrSegmentRoutingTLVIngressNode : IPv6 Option Header Segment Routing - Ingress Node TLV
IPv6ExtHdrSegmentRoutingTLVPad1 : IPv6 Option Header Segment Routing - Pad1 TLV
IPv6ExtHdrSegmentRoutingTLVPadN : IPv6 Option Header Segment Routing - PadN TLV
ISAKMP     : ISAKMP
ISAKMP_class : None
ISAKMP_payload : ISAKMP payload
ISAKMP_payload_Hash : ISAKMP Hash
ISAKMP_payload_ID : ISAKMP Identification
ISAKMP_payload_KE : ISAKMP Key Exchange
ISAKMP_payload_Nonce : ISAKMP Nonce
ISAKMP_payload_Proposal : IKE proposal
ISAKMP_payload_SA : ISAKMP SA
ISAKMP_payload_Transform : IKE Transform
ISAKMP_payload_VendorID : ISAKMP Vendor ID
InheritOriginDNSStrPacket : None
IrLAPCommand : IrDA Link Access Protocol Command
IrLAPHead  : IrDA Link Access Protocol Header
IrLMP      : IrDA Link Management Protocol
Jumbo      : Jumbo Payload
L2CAP_CmdHdr : L2CAP command header
L2CAP_CmdRej : L2CAP Command Rej
L2CAP_ConfReq : L2CAP Conf Req
L2CAP_ConfResp : L2CAP Conf Resp
L2CAP_ConnReq : L2CAP Conn Req
L2CAP_ConnResp : L2CAP Conn Resp
L2CAP_Connection_Parameter_Update_Request : L2CAP Connection Parameter Update Request
L2CAP_Connection_Parameter_Update_Response : L2CAP Connection Parameter Update Response
L2CAP_DisconnReq : L2CAP Disconn Req
L2CAP_DisconnResp : L2CAP Disconn Resp
L2CAP_Hdr  : L2CAP header
L2CAP_InfoReq : L2CAP Info Req
L2CAP_InfoResp : L2CAP Info Resp
L2TP       : L2TP
LEAP       : Cisco LEAP
LLC        : LLC
LLMNRQuery : Link Local Multicast Node Resolution - Query
LLMNRResponse : Link Local Multicast Node Resolution - Response
LLTD       : LLTD
LLTDAttribute : LLTD Attribute
LLTDAttribute80211MaxRate : LLTD Attribute - 802.11 Max Rate
LLTDAttribute80211PhysicalMedium : LLTD Attribute - 802.11 Physical Medium
LLTDAttributeCharacteristics : LLTD Attribute - Characteristics
LLTDAttributeDeviceUUID : LLTD Attribute - Device UUID
LLTDAttributeEOP : LLTD Attribute - End Of Property
LLTDAttributeHostID : LLTD Attribute - Host ID
LLTDAttributeIPv4Address : LLTD Attribute - IPv4 Address
LLTDAttributeIPv6Address : LLTD Attribute - IPv6 Address
LLTDAttributeLargeTLV : LLTD Attribute - Large TLV
LLTDAttributeLinkSpeed : LLTD Attribute - Link Speed
LLTDAttributeMachineName : LLTD Attribute - Machine Name
LLTDAttributePerformanceCounterFrequency : LLTD Attribute - Performance Counter Frequency
LLTDAttributePhysicalMedium : LLTD Attribute - Physical Medium
LLTDAttributeQOSCharacteristics : LLTD Attribute - QoS Characteristics
LLTDAttributeSeesList : LLTD Attribute - Sees List Working Set
LLTDDiscover : LLTD - Discover
LLTDEmit   : LLTD - Emit
LLTDEmiteeDesc : LLTD - Emitee Desc
LLTDHello  : LLTD - Hello
LLTDQueryLargeTlv : LLTD - Query Large Tlv
LLTDQueryLargeTlvResp : LLTD - Query Large Tlv Response
LLTDQueryResp : LLTD - Query Response
LLTDRecveeDesc : LLTD - Recvee Desc
LL_CHANNEL_MAP_IND : LL_CHANNEL_MAP_IND
LL_CONNECTION_PARAM_REQ : LL_CONNECTION_PARAM_REQ
LL_CONNECTION_PARAM_RSP : LL_CONNECTION_PARAM_RSP
LL_CONNECTION_UPDATE_IND : LL_CONNECTION_UPDATE_IND
LL_ENC_REQ : LL_ENC_REQ
LL_ENC_RSP : LL_ENC_RSP
LL_FEATURE_REQ : LL_FEATURE_REQ
LL_FEATURE_RSP : LL_FEATURE_RSP
LL_LENGTH_REQ :  LL_LENGTH_REQ
LL_LENGTH_RSP :  LL_LENGTH_RSP
LL_MIN_USED_CHANNELS_IND : LL_MIN_USED_CHANNELS_IND
LL_PAUSE_ENC_REQ : LL_PAUSE_ENC_REQ
LL_PAUSE_ENC_RSP : LL_PAUSE_ENC_RSP
LL_PHY_REQ : LL_PHY_REQ
LL_PHY_RSP : LL_PHY_RSP
LL_PHY_UPDATE_IND : LL_PHY_UPDATE_IND
LL_PING_REQ : LL_PING_REQ
LL_PING_RSP : LL_PING_RSP
LL_REJECT_EXT_IND : LL_REJECT_EXT_IND
LL_REJECT_IND : LL_REJECT_IND
LL_SLAVE_FEATURE_REQ : LL_SLAVE_FEATURE_REQ
LL_START_ENC_REQ : LL_START_ENC_REQ
LL_START_ENC_RSP : LL_START_ENC_RSP
LL_TERMINATE_IND : LL_TERMINATE_IND
LL_UNKNOWN_RSP : LL_UNKNOWN_RSP
LL_VERSION_IND : LL_VERSION_IND
LinkStatusEntry : ZigBee Link Status Entry
LinuxTunIfReq : None
LinuxTunPacketInfo : None
LoWPANBroadcast : 6LoWPAN Broadcast
LoWPANFragmentationFirst : 6LoWPAN First Fragmentation Packet
LoWPANFragmentationSubsequent : 6LoWPAN Subsequent Fragmentation Packet
LoWPANMesh : 6LoWPAN Mesh Packet
LoWPANUncompressedIPv6 : 6LoWPAN Uncompressed IPv6
LoWPAN_HC1 : LoWPAN_HC1 Compressed IPv6
LoWPAN_HC2_UDP : 6LoWPAN HC1 UDP encoding
LoWPAN_IPHC : LoWPAN IP Header Compression Packet
LoWPAN_NHC : LOWPAN_NHC
LoWPAN_NHC_Hdr : None
LoWPAN_NHC_IPv6Ext : None
LoWPAN_NHC_UDP : None
Loopback   : Loopback
MACsecSCI  : SCI
MGCP       : MGCP
MIP6MH_BA  : IPv6 Mobility Header - Binding ACK
MIP6MH_BE  : IPv6 Mobility Header - Binding Error
MIP6MH_BRR : IPv6 Mobility Header - Binding Refresh Request
MIP6MH_BU  : IPv6 Mobility Header - Binding Update
MIP6MH_CoT : IPv6 Mobility Header - Care-of Test
MIP6MH_CoTI : IPv6 Mobility Header - Care-of Test Init
MIP6MH_Generic : IPv6 Mobility Header - Generic Message
MIP6MH_HoT : IPv6 Mobility Header - Home Test
MIP6MH_HoTI : IPv6 Mobility Header - Home Test Init
MIP6OptAltCoA : MIPv6 Option - Alternate Care-of Address
MIP6OptBRAdvice : Mobile IPv6 Option - Binding Refresh Advice
MIP6OptBindingAuthData : MIPv6 Option - Binding Authorization Data
MIP6OptCGAParams : MIPv6 option - CGA Parameters
MIP6OptCGAParamsReq : MIPv6 option - CGA Parameters Request
MIP6OptCareOfTest : MIPv6 option - Care-of Test
MIP6OptCareOfTestInit : MIPv6 option - Care-of Test Init
MIP6OptHomeKeygenToken : MIPv6 option - Home Keygen Token
MIP6OptLLAddr : MIPv6 Option - Link-Layer Address (MH-LLA)
MIP6OptMNID : MIPv6 Option - Mobile Node Identifier
MIP6OptMobNetPrefix : NEMO Option - Mobile Network Prefix
MIP6OptMsgAuth : MIPv6 Option - Mobility Message Authentication
MIP6OptNonceIndices : MIPv6 Option - Nonce Indices
MIP6OptReplayProtection : MIPv6 option - Replay Protection
MIP6OptSignature : MIPv6 option - Signature
MIP6OptUnknown : Scapy6 - Unknown Mobility Option
MKABasicParamSet : Basic Parameter Set
MKADistributedCAKParamSet : Distributed CAK parameter set
MKADistributedSAKParamSet : Distributed SAK parameter set
MKAICVSet  : ICV
MKALivePeerListParamSet : Live Peer List Parameter Set
MKAPDU     : MKPDU
MKAParamSet : None
MKAPeerListTuple : Peer List Tuple
MKAPotentialPeerListParamSet : Potential Peer List Parameter Set
MKASAKUseParamSet : SAK Use Parameter Set
MPacketPreamble : MPacket Preamble
MobileIP   : Mobile IP (RFC3344)
MobileIPRRP : Mobile IP Registration Reply (RFC3344)
MobileIPRRQ : Mobile IP Registration Request (RFC3344)
MobileIPTunnelData : Mobile IP Tunnel Data Message (RFC3519)
NBNSNodeStatusResponse : NBNS Node Status Response
NBNSNodeStatusResponseEnd : NBNS Node Status Response
NBNSNodeStatusResponseService : NBNS Node Status Response Service
NBNSQueryRequest : NBNS query request
NBNSQueryResponse : NBNS query response
NBNSQueryResponseNegative : NBNS query response (negative)
NBNSRequest : NBNS request
NBNSWackResponse : NBNS Wait for Acknowledgement Response
NBTDatagram : NBT Datagram Packet
NBTSession : NBT Session Packet
NTP        : None
NTPAuthenticator : Authenticator
NTPClockStatusPacket : clock status
NTPConfPeer : conf_peer
NTPConfRestrict : conf_restrict
NTPConfTrap : conf_trap
NTPConfUnpeer : conf_unpeer
NTPControl : Control message
NTPErrorStatusPacket : error status
NTPExtension : extension
NTPExtensions : NTPv4 extensions
NTPHeader  : NTPHeader
NTPInfoAuth : info_auth
NTPInfoControl : info_control
NTPInfoIOStats : info_io_stats
NTPInfoIfStatsIPv4 : info_if_stats
NTPInfoIfStatsIPv6 : info_if_stats
NTPInfoKernel : info_kernel
NTPInfoLoop : info_loop
NTPInfoMemStats : info_mem_stats
NTPInfoMonitor1 : InfoMonitor1
NTPInfoPeer : info_peer
NTPInfoPeerList : info_peer_list
NTPInfoPeerStats : info_peer_stats
NTPInfoPeerSummary : info_peer_summary
NTPInfoSys : info_sys
NTPInfoSysStats : info_sys_stats
NTPInfoTimerStats : info_timer_stats
NTPPeerStatusDataPacket : data / peer status
NTPPeerStatusPacket : peer status
NTPPrivate : Private (mode 7)
NTPPrivatePktTail : req_pkt_tail
NTPPrivateReqPacket : request data
NTPStatusPacket : status
NTPSystemStatusPacket : system status
NetBIOS_DS : NetBIOS datagram service
NetflowDataflowsetV9 : Netflow DataFlowSet V9/10
NetflowFlowsetV9 : Netflow FlowSet V9/10
NetflowHeader : Netflow Header
NetflowHeaderV1 : Netflow Header v1
NetflowHeaderV10 : IPFix (Netflow V10) Header
NetflowHeaderV5 : Netflow Header v5
NetflowHeaderV9 : Netflow Header V9
NetflowOptionsFlowset10 : Netflow V10 (IPFix) Options Template FlowSet
NetflowOptionsFlowsetOptionV9 : Netflow Options Template FlowSet V9/10 - Option
NetflowOptionsFlowsetScopeV9 : Netflow Options Template FlowSet V9/10 - Scope
NetflowOptionsFlowsetV9 : Netflow Options Template FlowSet V9
NetflowOptionsRecordOptionV9 : Netflow Options Template Record V9/10 - Option
NetflowOptionsRecordScopeV9 : Netflow Options Template Record V9/10 - Scope
NetflowRecordV1 : Netflow Record v1
NetflowRecordV5 : Netflow Record v5
NetflowRecordV9 : Netflow DataFlowset Record V9/10
NetflowTemplateFieldV9 : Netflow Flowset Template Field V9/10
NetflowTemplateV9 : Netflow Flowset Template V9/10
NoPayload  : None
OCSP_ByKey : None
OCSP_ByName : None
OCSP_CertID : None
OCSP_CertStatus : None
OCSP_GoodInfo : None
OCSP_ResponderID : None
OCSP_Response : None
OCSP_ResponseBytes : None
OCSP_ResponseData : None
OCSP_RevokedInfo : None
OCSP_SingleResponse : None
OCSP_UnknownInfo : None
PMKIDListPacket : PMKIDs
PPI        : Per-Packet Information header (PPI)
PPI_Element : PPI Element
PPI_Hdr    : PPI Header
PPP        : PPP Link Layer
PPP_CHAP   : PPP Challenge Handshake Authentication Protocol
PPP_CHAP_ChallengeResponse : PPP Challenge Handshake Authentication Protocol
PPP_ECP    : None
PPP_ECP_Option : PPP ECP Option
PPP_ECP_Option_OUI : PPP ECP Option
PPP_IPCP   : None
PPP_IPCP_Option : PPP IPCP Option
PPP_IPCP_Option_DNS1 : PPP IPCP Option: DNS1 Address
PPP_IPCP_Option_DNS2 : PPP IPCP Option: DNS2 Address
PPP_IPCP_Option_IPAddress : PPP IPCP Option: IP Address
PPP_IPCP_Option_NBNS1 : PPP IPCP Option: NBNS1 Address
PPP_IPCP_Option_NBNS2 : PPP IPCP Option: NBNS2 Address
PPP_LCP    : PPP Link Control Protocol
PPP_LCP_ACCM_Option : PPP LCP Option
PPP_LCP_Auth_Protocol_Option : PPP LCP Option
PPP_LCP_Callback_Option : PPP LCP Option
PPP_LCP_Code_Reject : PPP Link Control Protocol
PPP_LCP_Configure : PPP Link Control Protocol
PPP_LCP_Discard_Request : PPP Link Control Protocol
PPP_LCP_Echo : PPP Link Control Protocol
PPP_LCP_MRU_Option : PPP LCP Option
PPP_LCP_Magic_Number_Option : PPP LCP Option
PPP_LCP_Option : PPP LCP Option
PPP_LCP_Protocol_Reject : PPP Link Control Protocol
PPP_LCP_Quality_Protocol_Option : PPP LCP Option
PPP_LCP_Terminate : PPP Link Control Protocol
PPP_PAP    : PPP Password Authentication Protocol
PPP_PAP_Request : PPP Password Authentication Protocol
PPP_PAP_Response : PPP Password Authentication Protocol
PPPoE      : PPP over Ethernet
PPPoED     : PPP over Ethernet Discovery
PPPoED_Tags : PPPoE Tag List
PPPoETag   : PPPoE Tag
PPTP       : PPTP
PPTPCallClearRequest : PPTP Call Clear Request
PPTPCallDisconnectNotify : PPTP Call Disconnect Notify
PPTPEchoReply : PPTP Echo Reply
PPTPEchoRequest : PPTP Echo Request
PPTPIncomingCallConnected : PPTP Incoming Call Connected
PPTPIncomingCallReply : PPTP Incoming Call Reply
PPTPIncomingCallRequest : PPTP Incoming Call Request
PPTPOutgoingCallReply : PPTP Outgoing Call Reply
PPTPOutgoingCallRequest : PPTP Outgoing Call Request
PPTPSetLinkInfo : PPTP Set Link Info
PPTPStartControlConnectionReply : PPTP Start Control Connection Reply
PPTPStartControlConnectionRequest : PPTP Start Control Connection Request
PPTPStopControlConnectionReply : PPTP Stop Control Connection Reply
PPTPStopControlConnectionRequest : PPTP Stop Control Connection Request
PPTPWANErrorNotify : PPTP WAN Error Notify
Packet     : None
Pad1       : Pad1
PadN       : PadN
Padding    : Padding
PrismHeader : Prism header
PseudoIPv6 : Pseudo IPv6 Header
RIP        : RIP header
RIPAuth    : RIP authentication
RIPEntry   : RIP entry
RSAOtherPrimeInfo : None
RSAPrivateKey : None
RSAPrivateKey_OpenSSL : None
RSAPublicKey : None
RSNCipherSuite : Cipher suite
RTP        : RTP
RTPExtension : RTP extension
RadioTap   : RadioTap
RadioTapExtendedPresenceMask : RadioTap Extended presence mask
RadioTapTLV : None
Radius     : RADIUS
RadiusAttr_ARAP_Security : Radius Attribute
RadiusAttr_Acct_Delay_Time : Radius Attribute
RadiusAttr_Acct_Input_Gigawords : Radius Attribute
RadiusAttr_Acct_Input_Octets : Radius Attribute
RadiusAttr_Acct_Input_Packets : Radius Attribute
RadiusAttr_Acct_Interim_Interval : Radius Attribute
RadiusAttr_Acct_Link_Count : Radius Attribute
RadiusAttr_Acct_Output_Gigawords : Radius Attribute
RadiusAttr_Acct_Output_Octets : Radius Attribute
RadiusAttr_Acct_Output_Packets : Radius Attribute
RadiusAttr_Acct_Session_Time : Radius Attribute
RadiusAttr_Acct_Tunnel_Packets_Lost : Radius Attribute
RadiusAttr_EAP_Message : EAP-Message
RadiusAttr_Egress_VLANID : Radius Attribute
RadiusAttr_Framed_AppleTalk_Link : Radius Attribute
RadiusAttr_Framed_AppleTalk_Network : Radius Attribute
RadiusAttr_Framed_IPX_Network : Radius Attribute
RadiusAttr_Framed_IP_Address : Radius Attribute
RadiusAttr_Framed_IP_Netmask : Radius Attribute
RadiusAttr_Framed_MTU : Radius Attribute
RadiusAttr_Framed_Protocol : Radius Attribute
RadiusAttr_Idle_Timeout : Radius Attribute
RadiusAttr_Login_IP_Host : Radius Attribute
RadiusAttr_Login_TCP_Port : Radius Attribute
RadiusAttr_Management_Privilege_Level : Radius Attribute
RadiusAttr_Message_Authenticator : Radius Attribute
RadiusAttr_Mobility_Domain_Id : Radius Attribute
RadiusAttr_NAS_IP_Address : Radius Attribute
RadiusAttr_NAS_Port : Radius Attribute
RadiusAttr_NAS_Port_Type : Radius Attribute
RadiusAttr_PMIP6_Home_DHCP4_Server_Address : Radius Attribute
RadiusAttr_PMIP6_Home_IPv4_Gateway : Radius Attribute
RadiusAttr_PMIP6_Home_LMA_IPv4_Address : Radius Attribute
RadiusAttr_PMIP6_Visited_DHCP4_Server_Address : Radius Attribute
RadiusAttr_PMIP6_Visited_IPv4_Gateway : Radius Attribute
RadiusAttr_PMIP6_Visited_LMA_IPv4_Address : Radius Attribute
RadiusAttr_Password_Retry : Radius Attribute
RadiusAttr_Port_Limit : Radius Attribute
RadiusAttr_Preauth_Timeout : Radius Attribute
RadiusAttr_Service_Type : Radius Attribute
RadiusAttr_Session_Timeout : Radius Attribute
RadiusAttr_State : Radius Attribute
RadiusAttr_Tunnel_Preference : Radius Attribute
RadiusAttr_User_Name : Radius Attribute
RadiusAttr_User_Password : Radius Attribute
RadiusAttr_Vendor_Specific : Vendor-Specific
RadiusAttr_WLAN_AKM_Suite : Radius Attribute
RadiusAttr_WLAN_Group_Cipher : Radius Attribute
RadiusAttr_WLAN_Group_Mgmt_Cipher : Radius Attribute
RadiusAttr_WLAN_Pairwise_Cipher : Radius Attribute
RadiusAttr_WLAN_RF_Band : Radius Attribute
RadiusAttr_WLAN_Reason_Code : Radius Attribute
RadiusAttr_WLAN_Venue_Info : Radius Attribute
RadiusAttribute : Radius Attribute
Raw        : Raw
RouterAlert : Router Alert
SCTP       : None
SCTPChunkAbort : None
SCTPChunkAddressConf : None
SCTPChunkAddressConfAck : None
SCTPChunkAuthentication : None
SCTPChunkCookieAck : None
SCTPChunkCookieEcho : None
SCTPChunkData : None
SCTPChunkError : None
SCTPChunkHeartbeatAck : None
SCTPChunkHeartbeatReq : None
SCTPChunkInit : None
SCTPChunkInitAck : None
SCTPChunkParamAdaptationLayer : None
SCTPChunkParamAddIPAddr : None
SCTPChunkParamChunkList : None
SCTPChunkParamCookiePreservative : None
SCTPChunkParamDelIPAddr : None
SCTPChunkParamECNCapable : None
SCTPChunkParamErrorIndication : None
SCTPChunkParamFwdTSN : None
SCTPChunkParamHearbeatInfo : None
SCTPChunkParamHostname : None
SCTPChunkParamIPv4Addr : None
SCTPChunkParamIPv6Addr : None
SCTPChunkParamRandom : None
SCTPChunkParamRequestedHMACFunctions : None
SCTPChunkParamSetPrimaryAddr : None
SCTPChunkParamStateCookie : None
SCTPChunkParamSuccessIndication : None
SCTPChunkParamSupportedAddrTypes : None
SCTPChunkParamSupportedExtensions : None
SCTPChunkParamUnrocognizedParam : None
SCTPChunkSACK : None
SCTPChunkShutdown : None
SCTPChunkShutdownAck : None
SCTPChunkShutdownComplete : None
SMB2_Compression_Capabilities : SMB2 Compression Capabilities
SMB2_Compression_Transform_Header : SMB2 Compression Transform Header
SMB2_Encryption_Capabilities : SMB2 Encryption Capabilities
SMB2_Header : SMB2 Header
SMB2_Negociate_Context : SMB2 Negociate Context
SMB2_Negociate_Protocol_Request_Header : SMB2 Negociate Protocol Request Header
SMB2_Negociate_Protocol_Response_Header : SMB2 Negociate Protocol Response Header
SMB2_Netname_Negociate_Context_ID : SMB2 Netname Negociate Context ID
SMB2_Preauth_Integrity_Capabilities : SMB2 Preauth Integrity Capabilities
SMBMailSlot : None
SMBNegociate_Protocol_Request_Header : SMBNegociate Protocol Request Header
SMBNegociate_Protocol_Request_Header_Generic : SMBNegociate Protocol Request Header Generic
SMBNegociate_Protocol_Request_Tail : SMB Negotiate Protocol Request Tail
SMBNegociate_Protocol_Response_Advanced_Security : SMBNegociate Protocol Response Advanced Security
SMBNegociate_Protocol_Response_No_Security : SMBNegociate Protocol Response No Security
SMBNegociate_Protocol_Response_No_Security_No_Key : None
SMBNetlogon_Protocol_Response_Header : SMBNetlogon Protocol Response Header
SMBNetlogon_Protocol_Response_Tail_LM20 : SMB Netlogon Protocol Response Tail LM20
SMBNetlogon_Protocol_Response_Tail_SAM : SMB Netlogon Protocol Response Tail SAM
SMBSession_Setup_AndX_Request : Session Setup AndX Request
SMBSession_Setup_AndX_Response : Session Setup AndX Response
SM_Confirm : Pairing Confirm
SM_DHKey_Check : DHKey Check
SM_Encryption_Information : Encryption Information
SM_Failed  : Pairing Failed
SM_Hdr     : SM header
SM_Identity_Address_Information : Identity Address Information
SM_Identity_Information : Identity Information
SM_Master_Identification : Master Identification
SM_Pairing_Request : Pairing Request
SM_Pairing_Response : Pairing Response
SM_Public_Key : Public Key
SM_Random  : Pairing Random
SM_Signing_Information : Signing Information
SNAP       : SNAP
SNMP       : None
SNMPbulk   : None
SNMPget    : None
SNMPinform : None
SNMPnext   : None
SNMPresponse : None
SNMPset    : None
SNMPtrapv1 : None
SNMPtrapv2 : None
SNMPvarbind : None
STP        : Spanning Tree Protocol
SixLoWPAN  : SixLoWPAN Dispatcher
SixLoWPAN_ESC : SixLoWPAN Dispatcher ESC
Skinny     : Skinny
TCP        : TCP
TCPerror   : TCP in ICMP
TFTP       : TFTP opcode
TFTP_ACK   : TFTP Ack
TFTP_DATA  : TFTP Data
TFTP_ERROR : TFTP Error
TFTP_OACK  : TFTP Option Ack
TFTP_Option : None
TFTP_Options : None
TFTP_RRQ   : TFTP Read Request
TFTP_WRQ   : TFTP Write Request
TunPacketInfo : None
UDP        : UDP
UDPerror   : UDP in ICMP
USER_CLASS_DATA : user class data
VENDOR_CLASS_DATA : vendor class data
VENDOR_SPECIFIC_OPTION : vendor specific option data
VRRP       : None
VRRPv3     : None
VXLAN      : VXLAN
X509_AccessDescription : None
X509_AlgorithmIdentifier : None
X509_Attribute : None
X509_AttributeTypeAndValue : None
X509_AttributeValue : None
X509_CRL   : None
X509_Cert  : None
X509_DNSName : None
X509_DirectoryName : None
X509_EDIPartyName : None
X509_ExtAuthInfoAccess : None
X509_ExtAuthorityKeyIdentifier : None
X509_ExtBasicConstraints : None
X509_ExtCRLDistributionPoints : None
X509_ExtCRLNumber : None
X509_ExtCertificateIssuer : None
X509_ExtCertificatePolicies : None
X509_ExtComment : None
X509_ExtDefault : None
X509_ExtDeltaCRLIndicator : None
X509_ExtDistributionPoint : None
X509_ExtDistributionPointName : None
X509_ExtExtendedKeyUsage : None
X509_ExtFreshestCRL : None
X509_ExtFullName : None
X509_ExtGeneralSubtree : None
X509_ExtInhibitAnyPolicy : None
X509_ExtInvalidityDate : None
X509_ExtIssuerAltName : None
X509_ExtIssuingDistributionPoint : None
X509_ExtKeyUsage : None
X509_ExtNameConstraints : None
X509_ExtNameRelativeToCRLIssuer : None
X509_ExtNetscapeCertType : None
X509_ExtNoticeReference : None
X509_ExtPolicyConstraints : None
X509_ExtPolicyInformation : None
X509_ExtPolicyMappings : None
X509_ExtPolicyQualifierInfo : None
X509_ExtPrivateKeyUsagePeriod : None
X509_ExtQcStatement : None
X509_ExtQcStatements : None
X509_ExtReasonCode : None
X509_ExtSubjInfoAccess : None
X509_ExtSubjectAltName : None
X509_ExtSubjectDirectoryAttributes : None
X509_ExtSubjectKeyIdentifier : None
X509_ExtUserNotice : None
X509_Extension : None
X509_Extensions : None
X509_GeneralName : None
X509_IPAddress : None
X509_OtherName : None
X509_PolicyMapping : None
X509_RDN   : None
X509_RFC822Name : None
X509_RegisteredID : None
X509_RevokedCertificate : None
X509_SubjectPublicKeyInfo : None
X509_TBSCertList : None
X509_TBSCertificate : None
X509_URI   : None
X509_Validity : None
X509_X400Address : None
ZCLGeneralReadAttributes : General Domain: Command Frame Payload: read_attributes
ZCLGeneralReadAttributesResponse : General Domain: Command Frame Payload: read_attributes_response
ZCLMeteringGetProfile : Metering Cluster: Get Profile Command (Server: Received)
ZCLPriceGetCurrentPrice : Price Cluster: Get Current Price Command (Server: Received)
ZCLPriceGetScheduledPrices : Price Cluster: Get Scheduled Prices Command (Server: Received)
ZCLPricePublishPrice : Price Cluster: Publish Price Command (Server: Generated)
ZCLReadAttributeStatusRecord : ZCL Read Attribute Status Record
ZEP1       : Zigbee Encapsulation Protocol (V1)
ZEP2       : Zigbee Encapsulation Protocol (V2)
ZigBeeBeacon : ZigBee Beacon Payload
ZigbeeAppCommandPayload : Zigbee Application Layer Command Payload
ZigbeeAppDataPayload : Zigbee Application Layer Data Payload (General APS Frame Format)
ZigbeeAppDataPayloadStub : Zigbee Application Layer Data Payload for Inter-PAN Transmission
ZigbeeClusterLibrary : Zigbee Cluster Library (ZCL) Frame
ZigbeeDeviceProfile : Zigbee Device Profile (ZDP) Frame
ZigbeeNWK  : Zigbee Network Layer
ZigbeeNWKCommandPayload : Zigbee Network Layer Command Payload
ZigbeeNWKStub : Zigbee Network Layer for Inter-PAN Transmission
ZigbeeSecurityHeader : Zigbee Security Header