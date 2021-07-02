package com.github.xsi640.grpc

import com.google.common.util.concurrent.Uninterruptibles
import io.grpc.*
import java.lang.Thread.sleep
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit


fun main() {
    val channel = ManagedChannelBuilder.forAddress("127.0.0.1", 8080)
        .usePlaintext()
//        .defaultLoadBalancingPolicy("round_robin")
        .maxInboundMessageSize(4096)
        .build()
    val md = MethodDescriptor.newBuilder<List<Any?>, List<Any?>>()
        .setType(MethodDescriptor.MethodType.UNARY)
        .setFullMethodName("demo/sayHello")
        .setRequestMarshaller(marshallerSerializer)
        .setResponseMarshaller(marshallerSerializer)
        .build()

    val latch = CountDownLatch(1)
    val call = channel.newCall(md, CallOptions.DEFAULT)
    call.start(object : ClientCall.Listener<List<Any?>>() {
        override fun onClose(status: Status?, trailers: Metadata?) {
            latch.countDown()
        }

        override fun onMessage(message: List<Any?>?) {
            message!!.forEach { println(it) }
        }


    }, Metadata())

    call.sendMessage(listOf("hello"))
    call.request(1)
    call.halfClose()
//https://vimsky.com/zh-tw/examples/detail/java-method-io.grpc.ClientCall.sendMessage.html
    if (!Uninterruptibles.awaitUninterruptibly(latch, 30, TimeUnit.SECONDS)) {
        throw RuntimeException("timeout!");
    }
}