extern crate pnet;

use pnet::packet::icmp::echo_request::{IcmpCodes, MutableEchoRequestPacket};
use pnet::packet::icmp::{time_exceeded, IcmpPacket, IcmpTypes};
use pnet::packet::ip::IpNextHeaderProtocols;
use pnet::packet::ipv4::{Ipv4Packet, MutableIpv4Packet};
use pnet::packet::Packet;
use pnet::transport::{ipv4_packet_iter, transport_channel, TransportChannelType};

use std::env;
use std::net::{IpAddr, Ipv4Addr};
use std::str::FromStr;

const IP_SIZE: usize = 20; // Size of an IPv4 header is typically 20 bytes
const ICMP_SIZE: usize = 8; // Size of an ICMP Echo Request packet is typically 8 bytes
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        panic!("Arg [Target IP]");
    }

    // set ip packet
    let mut ip_packet: [u8; IP_SIZE] = [0; IP_SIZE];
    let mut ip = MutableIpv4Packet::new(&mut ip_packet).unwrap();
    make_ip_packet(&mut ip, Ipv4Addr::from_str(&args[1]).unwrap());

    // set icmp packet
    let mut icmp_packet: [u8; ICMP_SIZE] = [0; ICMP_SIZE];
    let mut icmp = MutableEchoRequestPacket::new(&mut icmp_packet).unwrap();
    make_icmp_echo_packet(&mut icmp);
    let checksum = checksum(icmp.packet());
    icmp.set_checksum(checksum);

    // add for ip packet
    ip.set_payload(&icmp_packet);

    send_recv_packet(&mut ip);
}

// ipv4packet settings

fn make_ip_packet(ip: &mut MutableIpv4Packet, target_ip: Ipv4Addr) {
    ip.set_version(4);
    ip.set_header_length(5);
    ip.set_total_length(28);
    ip.set_identification(1);
    ip.set_ttl(1);
    ip.set_next_level_protocol(IpNextHeaderProtocols::Icmp);
    ip.set_destination(target_ip);
}

// icmp settings
fn make_icmp_echo_packet(icmp: &mut MutableEchoRequestPacket) {
    icmp.set_icmp_type(IcmpTypes::EchoRequest);
    icmp.set_icmp_code(IcmpCodes::NoCode);
    icmp.set_checksum(0);
    icmp.set_identifier(1);
    icmp.set_sequence_number(1);
}

fn checksum(data: &[u8]) -> u16 {
    let mut sum: u32 = 0;
    let mut s = data.len();
    for i in 0..s / 2 {
        sum += (((data[i * 2] as u16) << 8) + data[i * 2] as u16) as u32;
        s -= 2;
        if sum & 0x80000000 == 1 {
            sum = (sum >> 16) + (sum & 0xffff);
        }
    }
    if s == 1 {
        sum = (sum >> 16) + (sum & 0xffff);
    }
    sum = (sum >> 8) + ((sum << 8) & 0xff00);

    !sum as u16
}

// packet sending settings
fn send_recv_packet(ip: &mut MutableIpv4Packet) {
    let (mut tx, mut rx) = transport_channel(
        512,
        TransportChannelType::Layer3(IpNextHeaderProtocols::Icmp),
    )
    .unwrap();
    let mut rx = ipv4_packet_iter(&mut rx);

    let mut reach = 0;
    println!("[*] scanning route -> {}", ip.get_destination());
    for i in 1..255 {
        // set packet
        ip.set_ttl(i);
        let ipv4 = Ipv4Packet::new(&ip.packet()).unwrap();
        tx.send_to(ipv4, IpAddr::V4(ip.get_destination())).unwrap();

        for i in 0..3 {
            match rx.next() {
                Ok(ip_response) => {
                    let i_pac = Ipv4Packet::new(ip_response.0.packet()).unwrap();
                    let res = analyze(&i_pac);
                    if res == 1 {
                        reach = 1;
                        println!("[*] Reach ttl: {} from {}", i, i_pac.get_source());
                        break;
                    } else if res == 0 {
                        println!("- ttl: {} from {}", i, i_pac.get_source());
                        break;
                    }
                }
                _ => {
                    println!(".");
                }
            }
        }
        if reach == 1 {
            break;
        }
    }
}

fn analyze(i_pac: &Ipv4Packet) -> u8 {
    match i_pac.get_next_level_protocol() {
        IpNextHeaderProtocols::Icmp => {
            let ic_pac = IcmpPacket::new(i_pac.payload()).unwrap();
            match ic_pac.get_icmp_type() {
                IcmpTypes::EchoReply => {
                    return 1;
                }
                IcmpTypes::TimeExceeded => match ic_pac.get_icmp_code() {
                    time_exceeded::IcmpCodes::TimeToLiveExceededInTransit => {
                        return 0;
                    }
                    _ => {
                        println!("[*] IcmpType:TimeExceeded Unknown Response")
                    }
                },
                _ => {}
            }
        }
        _ => {}
    }
    2
}
