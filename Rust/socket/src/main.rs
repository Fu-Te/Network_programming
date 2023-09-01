//! # TCPサーバー
//!
//! アドレスとポートで待ち受けをしてクライアントからの接続を処理する。
//!
use std::io::{Read, Write};
use std::process::exit;
use std::net::TcpListener;

fn main() {
    // リステナーをアドレスとポートにバインド
    let listener = TcpListener::bind("localhost:5123");
    if let Err(e) = listener {
        eprintln!("failed to bind. {}", e);
        exit(1);
    }

    let listener = listener.unwrap();

    // サーバーの受信ループを開始
    loop {
        // クライアントからの接続を待ち受け
        println!("accept...");
        let stream = listener.accept();
        if let Err(e) = stream {
            eprintln!("failed to accept. {}", e);
            exit(1);
        }

        // クライアントからの接続に成功
        let stream = stream.unwrap();
        println!("connected to {}", stream.1);  // クライアントのアドレス表示
        let mut stream = stream.0;  // クライアントと繋がっているストリームを取得

        // クライアントからデータを読み込み
        let mut buf: [u8; 512] = [ 0; 512 ];  // 読み込みデータの保存先
        let size = stream.read(&mut buf);  // 読み込み
        if let Err(e) = size {
            eprintln!("failed to read. {}", e);
            exit(1);
        }
        let size = size.unwrap();
        if size == 0 {
            continue;  // 読み込みサイズが0ならcontinue
        }

        // 読み込んだデータを文字列にしてログとして出力
        let s = String::from_utf8(buf.to_vec()).unwrap();
        println!("{}", s);

        // クライアントにデータを書き込み
        if let Err(e) = stream.write(b"ok") {
            eprintln!("failed to write. {}", e);
        }
    }
}
