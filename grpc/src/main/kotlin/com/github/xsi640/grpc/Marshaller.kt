package com.github.xsi640.grpc

import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import io.grpc.MethodDescriptor
import java.io.ByteArrayInputStream
import java.io.InputStream

interface MarshallerSerializer : MethodDescriptor.Marshaller<List<Any?>> {

}


class JsonMarshallerSerializer : MarshallerSerializer {

    private val mapper = jacksonObjectMapper()

    override fun stream(value: List<Any?>): InputStream {
        val bytes = mapper.writeValueAsBytes(value)
        return ByteArrayInputStream(bytes)
    }

    override fun parse(stream: InputStream): List<Any?> {
        return mapper.readValue(stream)
    }

}