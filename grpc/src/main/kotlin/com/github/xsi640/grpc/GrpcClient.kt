package com.github.xsi640.grpc

import io.grpc.*
import io.grpc.stub.ClientCalls
import java.util.concurrent.CountDownLatch


fun main() {
    val channel = ManagedChannelBuilder.forAddress("127.0.0.1", 8080)
        .usePlaintext()
        .maxInboundMessageSize(4096)
        .build()
    val md = MethodDescriptor.newBuilder<List<Any?>, List<Any?>>()
        .setType(MethodDescriptor.MethodType.UNARY)
        .setFullMethodName("demo/sayHello")
        .setRequestMarshaller(marshallerSerializer)
        .setResponseMarshaller(marshallerSerializer)
        .build()

    val latch = CountDownLatch(1)
    val r = ClientCalls.blockingUnaryCall(channel, md, CallOptions.DEFAULT, listOf("hello"))
    println(r)
}