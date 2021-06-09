import org.apache.ratis.client.RaftClient;
import org.apache.ratis.conf.Parameters;
import org.apache.ratis.conf.RaftProperties;
import org.apache.ratis.grpc.GrpcFactory;
import org.apache.ratis.protocol.*;
import org.apache.ratis.thirdparty.com.google.protobuf.ByteString;

import java.io.*;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;
import java.net.InetSocketAddress;
import java.nio.charset.Charset;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

public class Cliente
{
    public static void main(String[] args) throws IOException, ExecutionException, InterruptedException {

        String raftGroupId = "raft_group____um"; // 16 caracteres.

        Map<String,InetSocketAddress> id2addr = new HashMap<>();
        id2addr.put("p1", new InetSocketAddress("127.0.0.1", 3000));
        id2addr.put("p2", new InetSocketAddress("127.0.0.1", 3500));
        id2addr.put("p3", new InetSocketAddress("127.0.0.1", 4000));

        List<RaftPeer> addresses = id2addr.entrySet()
                .stream()
                .map(e -> RaftPeer.newBuilder().setId(e.getKey()).setAddress(e.getValue()).build())
                .collect(Collectors.toList());

        final RaftGroup raftGroup = RaftGroup.valueOf(RaftGroupId.valueOf(ByteString.copyFromUtf8(raftGroupId)), addresses);
        RaftProperties raftProperties = new RaftProperties();

        RaftClient client = RaftClient.newBuilder()
                                      .setProperties(raftProperties)
                                      .setRaftGroup(raftGroup)
                                      .setClientRpc(new GrpcFactory(new Parameters())
                                      .newRaftClientRpc(ClientId.randomId(), raftProperties))
                                      .build();

        RaftClientReply getValue;
        CompletableFuture<RaftClientReply> compGetValue;
        String response;

        ServerSocket Server = new ServerSocket (5100);

        while(true){

            String[] req;
            System.out.println("Esperando cliente na porta 5100");

            Socket connected = Server.accept();
            System.out.println("cliente"+" "+ connected.getInetAddress() +":"+connected.getPort()+" conectado");

            BufferedReader inFromClient = new BufferedReader(new InputStreamReader(connected.getInputStream()));
            req = inFromClient.readLine().split(",");
            connected.close();

            switch(req[0]){
                
                case "add":
                    getValue = client.io().send(Message.valueOf("add:" + req[1] + ":" + req[2]));
                    response = getValue.getMessage().getContent().toString(Charset.defaultCharset());
                    System.out.println("Resposta: " + response);
                    break;
                
                case "get":
                    getValue = client.io().sendReadOnly(Message.valueOf("get:" + req[1]));
                    response = getValue.getMessage().getContent().toString(Charset.defaultCharset());
                    System.out.println("Resposta: " + response);
                    break;
                
                case "delete":
                    getValue = client.io().send(Message.valueOf("delete:" + req[1]));
                    response = getValue.getMessage().getContent().toString(Charset.defaultCharset());
                    System.out.println("Resposta: " + response);
                    break;
                    
                case "update":
                    getValue = client.io().send(Message.valueOf("update:" + req[1] + ":" + req[2]));
                    response = getValue.getMessage().getContent().toString(Charset.defaultCharset());
                    System.out.println("Resposta: " + response);
                    break;
 
                default:
                    System.out.println("Comando inválido");
            }

            client.close();
        }
    }
}
