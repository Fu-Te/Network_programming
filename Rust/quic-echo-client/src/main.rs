use anyhow::*;
use clap::Clap;
use futures::StreamExt;
use quinn::{Certificate, ClientConfigBuilder, Endpoint, NewConnection};
use std::net::SocketAddr;
use std::path::PathBuf;

#[derive(Clap, Debug)]
#[clap(version = "0.1.0")]
struct Opts {
    #[clap(short, long)]
    ipaddr: SocketAddr,
    #[clap(short, long)]
    ca: PathBuf,
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    // コマンドライン引数のパース
    let opts: Opts = Opts::parse();

    // QUICの設定
    let mut client_config = ClientConfigBuilder::default();
    client_config.add_certificate_authority(Certificate::from_der(&std::fs::read(&opts.ca)?)?)?;
    let mut endpoint_builder = Endpoint::builder();
    endpoint_builder.default_client_config(client_config.build());
    let (endpoint, _incoming) = endpoint_builder.bind(&"0.0.0.0:0".parse().unwrap())?;

    // サーバへ接続
    let NewConnection {
        connection,
        mut uni_streams,
        ..
    } = endpoint.connect(&opts.ipaddr, "localhost")?.await?;
    println!("connected: addr={}", connection.remote_address());

    // メッセージの書き込み
    let msg = "hello";

    let mut send_stream = connection.open_uni().await?;
    send_stream.write(msg.as_bytes()).await?;
    send_stream.finish().await?;
    println!("sent \"{}\"", msg);

    // 返信の読み込み
    if let Some(uni_stream) = uni_streams.next().await {
        let uni_stream = uni_stream?;
        let data = uni_stream.read_to_end(0xFF).await?;
        println!("received \"{}\"", String::from_utf8_lossy(&data));
    } else {
        bail!("cannot open uni stream");
    }

    // 終了
    endpoint.wait_idle().await;

    Ok(())
}
