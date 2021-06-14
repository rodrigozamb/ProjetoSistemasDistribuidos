import org.apache.ratis.proto.RaftProtos;
import org.apache.ratis.protocol.Message;
import org.apache.ratis.statemachine.TransactionContext;
import org.apache.ratis.statemachine.impl.BaseStateMachine;

import java.nio.charset.Charset;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

public class MaquinaDeEstados extends BaseStateMachine
{
    private final Map<String, String> clients = new ConcurrentHashMap<>();

    @Override
    public CompletableFuture<Message> query(Message request){
        final String[] opKey = request.getContent().toString(Charset.defaultCharset()).split(":");
        final String result = opKey[0]+ ":"+ clients.get(opKey[1]);

        LOG.info("{}: {} = {}", opKey[0], opKey[1], result);
        return CompletableFuture.completedFuture(Message.valueOf(result));
    }

    @Override
    public CompletableFuture<Message> applyTransaction(TransactionContext trx) {
        
        final RaftProtos.LogEntryProto entry = trx.getLogEntry();
        final String[] opKeyValue = entry.getStateMachineLogEntry().getLogData().toString(Charset.defaultCharset()).split(":");
        final RaftProtos.RaftPeerRole role = trx.getServerRole();

        String result;
        
        if(opKeyValue[0].equals("add_client")){
            
            clients.put(opKeyValue[1], opKeyValue[2]);
            result = "add_client," + opKeyValue[1] + "," + opKeyValue[2];
            LOG.info("{}:{} {} {}={}", role, getId(), opKeyValue[0], opKeyValue[1], opKeyValue[2]);
        }
        
        else if(opKeyValue[0].equals("delete_client")){
            
            clients.remove(opKeyValue[1]);
            result = "delete_client," + opKeyValue[1];
            LOG.info("{}:{} {} {}", role, getId(), opKeyValue[0], opKeyValue[1]);
        }
            
        else{
            
            clients.replace(opKeyValue[1], opKeyValue[2]);
            result = "update_client," + opKeyValue[1] + "," + opKeyValue[2];
            LOG.info("{}:{} {} {}={}", role, getId(), opKeyValue[0], opKeyValue[1], opKeyValue[2]);
        }

        final CompletableFuture<Message> f = CompletableFuture.completedFuture(Message.valueOf(result));

        if (LOG.isTraceEnabled()) {
            LOG.trace("{}: key/values={}", getId(), clients);
        }
 
        return f;
    }
}
