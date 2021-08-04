package com.github.xsi640.plusplus

import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import org.apache.http.client.methods.HttpPost
import org.apache.http.entity.StringEntity
import org.apache.http.impl.client.HttpClients

class Example {
}

val token = "fa88055d65df41dd881b0ea0cffa8f78"
val group = "home"
val url = "http://pushplus.hxtrip.com/send"

fun main() {
    val objectMapper = jacksonObjectMapper()
    HttpClients.createDefault().use { httpClient ->
        val post = HttpPost(url)
        val json = objectMapper.createObjectNode()
        json.put("token", token)
        json.put("title", "test 标题")
        json.put("content", "test 内容")
        json.put("topic", group)
        post.entity = StringEntity(json.toString(), Charsets.UTF_8)
        post.addHeader("Content-Type", "application/json;charset=UTF-8")
        httpClient.execute(post).use { response ->
            if (response.statusLine.statusCode == 200) {
                println("发送成功")
            }
        }
    }
}