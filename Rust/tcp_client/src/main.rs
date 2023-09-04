//Tcp client
use std::net::TcpStream;
use std::io::{Read, Write};
use std::process::exit;

fn main(){
    //アドレスとポートに接続しストリームを得る
    let stream = TcpStream::connect("localhost:5123");
    if let Err(e) = stream{
        eprintln!("failed to connect. {}",e);
        exit(1);

    }
    let mut stream = stream.unwrap();
    //接続したストリームに書き込み
    if let Err(e) = stream.write(b"hello"){
        eprintln!("failed to write_all. {}",e);
        exit(1);

    }
    //接続したストリームから読み込み
    let mut buf:[u8; 512] = [0; 512];
    if let Err(e) = stream.read(&mut buf){
        eprintln!("failed to read. {}",e);
        exit(1);
    }
    //読み込んだバイトをutf8に変換
    let s = String::from_utf8(buf.to_vec()).unwrap();
    println!("{}",s);
}
