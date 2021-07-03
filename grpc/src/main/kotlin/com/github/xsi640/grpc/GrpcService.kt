package com.github.xsi640.grpc

import io.grpc.*
import io.grpc.stub.ServerCalls
import io.grpc.stub.StreamObserver
import java.lang.reflect.Method

interface GrpcService {
    val registerClasses: MutableList<Class<*>>

    fun register(clazz: Class<*>)
    fun start()
    fun stop()
}

interface GrpcServiceFactory {
    fun create(settings: GrpcServerSettings): GrpcService
}

class GrpcServiceImpl(
    val settings: GrpcServerSettings,
    val marshallerSerializer: MarshallerSerializer
) : GrpcService {

    override val registerClasses: MutableList<Class<*>> = mutableListOf()

    private lateinit var server: Server

    override fun register(clazz: Class<*>) {
        if (!registerClasses.contains(clazz)) {
            registerClasses.add(clazz)
        }
    }

    override fun start() {
        val builder = ServerBuilder.forPort(settings.port)
        builder.maxInboundMessageSize(settings.messageSize)
        registerClasses.forEach { clazz ->
            builder.addService(buildServiceDefinition(clazz))
        }
        server = builder.build()
        server.start()
    }

    override fun stop() {
        server.shutdown()
    }

    private fun buildServiceDefinition(clazz: Class<*>): ServerServiceDefinition {
        val serviceName = clazz.name
        val builder = ServerServiceDefinition.builder(serviceName)
        clazz.declaredMethods.forEach { method ->
            val md = MethodDescriptor
                .newBuilder<List<Any?>, List<Any?>>()
                .setType(MethodDescriptor.MethodType.UNARY)
                .setFullMethodName("$serviceName/${method.name}")
                .setRequestMarshaller(marshallerSerializer)
                .setResponseMarshaller(marshallerSerializer).build()
            builder.addMethod(md, ServerCalls.asyncUnaryCall(ServerUnaryCall(clazz, method)))
        }
        return builder.build()
    }

    class ServerUnaryCall(
        val clazz: Class<*>,
        val method: Method
    ) : ServerCalls.UnaryMethod<List<Any?>, List<Any?>> {
        override fun invoke(request: List<Any?>, responseObserver: StreamObserver<List<Any?>>) {
            val result = invokeMethod(request)
            responseObserver.onNext(result)
            responseObserver.onCompleted()
        }

        fun invokeMethod(request: List<Any?>): List<Any?> {
            TODO("处理逻辑")
        }
    }
}