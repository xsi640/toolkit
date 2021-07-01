package com.github.xsi640.grpc

import io.grpc.MethodDescriptor
import io.grpc.ServerBuilder
import io.grpc.ServerServiceDefinition
import io.grpc.stub.ServerCalls
import io.grpc.stub.ServerCalls.asyncUnaryCall
import io.grpc.stub.StreamObserver
import java.io.InputStream
import java.lang.Thread.sleep

data class GrpcService(
    val clazz: Class<*>,
    val name: String,
    val port: Int
)

fun main() {
    val builder = ServerBuilder.forPort(8080)
    builder.maxInboundMessageSize(4096)
//    builder.intercept()
    builder.addService(buildServiceDefinition())
    val server = builder.build()
    server.start()
    sleep(10000000)
}

fun buildServiceDefinition(): ServerServiceDefinition {
    val builder = ServerServiceDefinition.builder("demo")
    val md = MethodDescriptor
        .newBuilder<List<Any?>, List<Any?>>()
        .setType(MethodDescriptor.MethodType.UNARY)
        .setFullMethodName("demo/sayHello")
        .setRequestMarshaller(object : MethodDescriptor.Marshaller<List<Any?>> {
            override fun stream(value: List<Any?>?): InputStream {
                TODO("Not yet implemented")
            }

            override fun parse(stream: InputStream?): List<Any?> {
                TODO("Not yet implemented")
            }
        })
        .setResponseMarshaller(object : MethodDescriptor.Marshaller<List<Any?>> {
            override fun stream(value: List<Any?>?): InputStream {
                TODO("Not yet implemented")
            }

            override fun parse(stream: InputStream?): List<Any?> {
                TODO("Not yet implemented")
            }
        }).build()
    builder.addMethod(md, asyncUnaryCall(object : ServerCalls.UnaryMethod<List<Any?>, List<Any?>> {
        override fun invoke(request: List<Any?>?, responseObserver: StreamObserver<List<Any?>>?) {
        }
    }))
    return builder.build()
}
