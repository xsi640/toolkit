package com.github.xsi640.fanghill

import com.fasterxml.jackson.databind.ObjectMapper
import okhttp3.HttpUrl
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.logging.HttpLoggingInterceptor
import java.net.URI
import java.security.MessageDigest
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit
import javax.net.ssl.SSLContext
import javax.net.ssl.SSLSocketFactory
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager

const val Mid = 39191
const val OrderWay = 0

const val token =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjEzNjkxMjYyODUzIiwiUm9sZUlkcyI6IiIsInJvbGUiOiIiLCJSZWFsTmFtZSI6IuiLj-aJrCIsIlVzZXJJZCI6IjM0MDQ3IiwiRGVwdElkIjoiMCIsIkRlcHRDb2RlIjoiIiwiRGVwdE5hbWUiOiIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDI0LzgvMSAxOjA0OjEzIiwibmJmIjoxNjkwOTM4MjUzLCJleHAiOjE3MjI0NzQyNTMsImlhdCI6MTY5MDkzODI1MywiaXNzIjoiaG9uZ3hpbiIsImF1ZCI6Imhvbmd4aW4ifQ.tQzxkVJkbVJ3GD95XSqDQO9RESIlcnVd_UAiWlP9uyY"
const val url = "https://tsg.fscac.org:5134/api/FW_Module/AddOrder?"
const val userAgent =
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
const val START_TIME = "2023-08-11 10:00"

val mapper = ObjectMapper()

fun main(args: Array<String>) {
    while (true) {
        val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm")
        val c = Calendar.getInstance()
        c.time = sdf.parse(START_TIME)
        c.add(Calendar.MINUTE, -1)
        if (Date().time > c.time.time) {
            break
        }
        Thread.sleep(1000)
    }
    while (true) {
        if (run()) {
            Thread.sleep(10)
            break
        }
    }
}

fun run(): Boolean {
    val timestamp = System.currentTimeMillis()
    val data = mutableMapOf<String, Any>()
    data["Mid"] = Mid
    data["OrderWay"] = OrderWay
    val newData = mutableMapOf<String, Any>()
    newData["Mid"] = Mid
    newData["OrderWay"] = OrderWay
    newData["token"] = token
    newData["timestamps"] = timestamp

    val builder = OkHttpClient().newBuilder()
        .followRedirects(true)
        .connectTimeout(3000, TimeUnit.MILLISECONDS)
        .readTimeout(3000, TimeUnit.MILLISECONDS)
        .sslSocketFactory(sslSocketFactory(), object : X509TrustManager {
            override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {
            }

            override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {
            }

            override fun getAcceptedIssuers(): Array<X509Certificate> {
                return emptyArray()
            }
        })
        .hostnameVerifier { _, _ -> true }

    val log = HttpLoggingInterceptor()
    log.level = HttpLoggingInterceptor.Level.BODY
    builder.addInterceptor(log)
    val client = builder.build()
    val requestBuilder = Request.Builder()
    requestBuilder.header("Content-Type", "application/json")
    requestBuilder.header("Sign", createRequestSign(newData))
    requestBuilder.header("Timestamps", timestamp.toString())
    requestBuilder.header("User-Agent", userAgent)
    requestBuilder.header("Authorization", "Bearer $token")
    val uri = URI(url)
    val urlBuilder = HttpUrl.Builder()
        .scheme(uri.scheme)
        .host(uri.host)
    if (uri.port != -1) {
        urlBuilder.port(uri.port)
    }
    if (uri.path.isNotEmpty()) {
        uri.path.split("/").forEach {
            if (it.isNotEmpty()) {
                urlBuilder.addPathSegment(it.trim('/'))
            }
        }
    }
    requestBuilder.url(urlBuilder.build())
    val body = mapper.writeValueAsString(data)
        .toRequestBody(contentType = "application/json".toMediaType())
    val request = requestBuilder.post(body).build()
    var result = false
    client.newCall(request).execute().use { resp ->
        val respBody = resp.body!!.string()
        println(respBody)
        val r = mapper.readValue(respBody, Response::class.java)
        if (r.result == 1) {
            result = true
        }
    }
    return result
}

fun createRequestSign(map: Map<String, Any?>): String {
    val keyList = map.keys.toSet().sorted()
    var urlParams = ""
    val sortKey = keyList.filter { key ->
        map[key] != null && map[key].toString() != ""
    }
    sortKey.forEach { key ->
        urlParams += if (sortKey[sortKey.size - 1] != key) {
            "${key}=${map[key]}&"
        } else {
            "${key}=${map[key]}"
        }
    }
    val md = MessageDigest.getInstance("MD5")
    val mdBytes = md.digest(urlParams.toByteArray())
    return mdBytes.joinToString("") { "%02x".format(it) }.lowercase()
}

private fun sslSocketFactory(): SSLSocketFactory {
    val sslContext = SSLContext.getInstance("SSL")
    sslContext.init(null, trustAllCerts, SecureRandom())
    return sslContext.socketFactory
}

val trustAllCerts: Array<TrustManager> = Array(1) {
    object : X509TrustManager {
        override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {
        }

        override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {
        }

        override fun getAcceptedIssuers(): Array<X509Certificate> {
            return emptyArray()
        }
    }
}

class Response(
    val result: Int = 0,
    val msg: String = "",
    val NumData: OrderData? = null
)

class OrderData(
    val Rid: Int = 0,
    val TotalNum: Int = 0,
    val OrderNum: Int = 0
)