package com.github.xsi640.grpc

open class GrpcSettings(
    open var messageSize: Int
)

class GrpcServerSettings(
    var port: Int,
    override var messageSize: Int
) : GrpcSettings(messageSize)