import "dart:io";
import "dart:async";
import "dart:math";
import "package:dart_amqp/dart_amqp.dart";

var UUID = () => "${(new Random()).nextDouble()}";

class RPCClient {
    Client client;
    String queueTag;
    String _replyQueueTag;
    Completer contextChannel;
    Map<String, Completer> _channels = new Map<String, Completer>();
    Queue _queue;
    ConnectionSettings setting;
     
    
    RPCClient(ConnectionSettings setting) :
        client = new Client(settings: setting),
        queueTag = "auth_queue" {
        contextChannel = new Completer();
        client
        .channel()
        .then((Channel channel) => channel.queue(queueTag))
        .then((Queue rpcQueue) {
            _queue = rpcQueue;
            return rpcQueue.channel.privateQueue();
        })
        .then((Queue rpcQueue) {
            rpcQueue.consume(noAck: true)
                .then((Consumer consumer) {
                    _replyQueueTag = consumer.queue.name;
                    consumer.listen(handler);
                    contextChannel.complete();
                });
        });
    }

    void handler (AmqpMessage event) {
        if (!_channels
            .containsKey(
                event.properties.corellationId)) return;
        print(" [.] Got ${event.payloadAsString}");
        _channels
            .remove(event.properties.corellationId)
            .complete(event.payloadAsString);
    }

    Future<String> call(Map input) {
        return contextChannel.future
            .then((_) {
                String uuid = UUID();
                Completer<String> channel = new Completer<String>();
                MessageProperties properties = new MessageProperties()
                    ..replyTo = _replyQueueTag
                    ..corellationId = uuid;
                _channels[uuid] = channel;
                print(" [x] Requesting ${input}");
                _queue.publish(input, properties: properties);
                return channel.future;
            });
    }

    Future close() {
        _channels.forEach((_, var next) => next.complete("RPC client closed"));
        _channels.clear();
        client.close();
    }
}

class User {
  final int phone_number;

  User(this.phone_number);

  User.fromJson(Map<String, dynamic> json)
      : phone_number = json['phone_number'];

  Map toJson() =>
    {
      'phone_number': phone_number
    };
}

String call(User user) {
    ConnectionSettings setting = new ConnectionSettings(
              host: "172.18.0.4",
              port: 5672,
              virtualHost: "logi-rabbitmq",
              authProvider: new PlainAuthenticator("admin", "admin")
          );
    RPCClient client = new RPCClient(setting);
    
    String out = "";
    client.call(user.toJson())
        .then((String res) {
          out = res;
          print(out);
        })
        .then((_) => client.close())
        .then((_) => null);
    return out;
}