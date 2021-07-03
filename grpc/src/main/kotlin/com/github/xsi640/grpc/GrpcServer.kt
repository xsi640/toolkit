package com.github.xsi640.grpc

import io.grpc.MethodDescriptor
import io.grpc.ServerBuilder
import io.grpc.ServerServiceDefinition
import io.grpc.stub.ServerCalls
import io.grpc.stub.ServerCalls.asyncUnaryCall
import io.grpc.stub.StreamObserver
import java.io.InputStream
import java.lang.Thread.sleep



fun main() {
    val builder = ServerBuilder.forPort(8080)
    builder.maxInboundMessageSize(4096)
//    builder.intercept()
    builder.addService(buildServiceDefinition())
    val server = builder.build()
    server.start()
    sleep(100000000)
}

val marshallerSerializer = JsonMarshallerSerializer()

fun buildServiceDefinition(): ServerServiceDefinition {
    val builder = ServerServiceDefinition.builder("demo")
    val md = MethodDescriptor
        .newBuilder<List<Any?>, List<Any?>>()
        .setType(MethodDescriptor.MethodType.UNARY)
        .setFullMethodName("demo/sayHello")
        .setRequestMarshaller(marshallerSerializer)
        .setResponseMarshaller(marshallerSerializer).build()
    builder.addMethod(md, asyncUnaryCall { request, responseObserver ->
        println("invoke")
        responseObserver.onNext(listOf("ok"))
        responseObserver.onCompleted()
    })
    return builder.build()
}
