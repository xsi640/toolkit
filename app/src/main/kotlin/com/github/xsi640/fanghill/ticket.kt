package com.github.xsi640.fanghill

import javafx.application.Application.launch
import kotlinx.coroutines.*
import org.apache.http.client.methods.HttpPost
import org.apache.http.impl.client.HttpClients
import org.apache.http.util.EntityUtils
import org.jsoup.Jsoup
import java.lang.Thread.sleep
import java.net.*
import java.text.SimpleDateFormat
import java.util.*


const val CATEGORY_ID = "763149d1-4390-4200-8b32-1f6ac71d3666"
const val LIST_URL = "http://www.fscac.org/Activity/List"
const val ORDER_URL = "http://www.fscac.org/Content/order"
const val DETAIL_URL = "http://www.fscac.org/Activity/detail"
val COOKIES =
    listOf(
        "__RequestVerificationToken=e9b6yhuwBnogAu0oQvHCKvu0utxBELh1iJYGgSyzMDsTEOwGC5amUYJg__kv442Up56z_Ix9SWCiXQ7Uw_k6dg2; .xCookie=80A3CCB0C2694AE6D21BAA0EEC7A3507DA15E7AB8001E1451A57D131DDCF2BCD36F8F8530A14F16F2D75E1F6D51BDD33E18BB35296C600D6E904A183F0E35C3EEF59A4614DE9300FD16F280EB5C515BE4FE8B2BDC64C9F61701FDF4E197DE058F27BCB52651E2194F8E76F9C2E901848",
        "__RequestVerificationToken=2mwMZemxja31qzwqTL2KhAPRdC4FJCTuRB29utVU9lL0fVSLF1ffV02fldsNX4hnBExBtSofHmZEkXXdHAl7LA2; ASP.NET_SessionId=yg02bl0joh4qxkvorufpkdle; .xCookie=9ECE6D12811CE096F252F6EA0D54F4702B56F6D23A412A88D7AC21E339B071DA071AE461EF09C2F867ED71EF011FB061E4C33C9B28841AEC5C9A143FC45F97DB2C40A2387AD8D12AB70C2A14F68089EC8E418AB2C057DC8D93B025EA319B60C67DB8E89CFCDFB8887C73C9F931FA775B"
    )

fun main(args: Array<String>) {
    val keyword = "八仙"
    var item: Item? = null
    while (item == null) {
        val exists = getCategories().firstOrNull { it.title.contains(keyword) }
        if (exists != null) {
            item = exists
        }
        println("not found keyword:$keyword retry...")
        sleep(500)
    }
    println("found $keyword's ticket.")
    val url = "$ORDER_URL?module=Activity&&" +
            "CategoryID=$CATEGORY_ID&&" +
            "id=${item.id}&&OrderTitle=${URLEncoder.encode(URLEncoder.encode(item.title, "UTF-8"), "UTF-8")}&&" +
            "OrderImage=${item.image}&&" +
            "OrderBeginTime=${item.beginTime.toString("yyyy/M/d HH:mm:ss").replace(" ", "%20")}&&" +
            "OrderUrl=${DETAIL_URL}?id=${item.id}"

    val jobs = mutableListOf<Job>()
    COOKIES.forEach { cookie ->
        jobs.add(GlobalScope.launch {
            var result = submitOrder(url, cookie)
            while (result == "0" || result == "-9") {
                result = submitOrder(url, cookie)
                delay(1)
            }
            if (result == "-1") {
                println("please check cookie.")
            } else if (result == "-2") {
                println("submit failured. already expired.")
            }
        })
    }

    while (jobs.any { it.isActive }) {
    }
    println("ok")
}

fun getCategories(): List<Item> {
    val result = mutableListOf<Item>()
    val doc = Jsoup.connect("$LIST_URL?CategoryID=$CATEGORY_ID&Page=1").get()
    val elements = doc.select("div.result ul.list li")
    elements.forEach { element ->
        val id = element.select("a")[0].attr("href").replace("detail?id=", "")
        val title = element.select(".title a").text()
        val image = element.select(".thumbnail").attr("src")
        val beginTime = element.select(".des dl dd")[2].text().toDate("yyyy-MM-dd HH:mm:ss")
        result.add(
            Item(
                id = id,
                title = title,
                image = image,
                beginTime = beginTime,
                url = "$DETAIL_URL?id=$id"
            )
        )
    }
    return result
}

fun submitOrder(url: String, cookie: String): String {
    val httpClient = HttpClients.createDefault()
    val method = HttpPost(url)
    method.addHeader("Content-Type", "application/json; charset=utf-8")
    method.addHeader(
        "Cookie",
        cookie
    )
    val response = httpClient.execute(method)
    return if (response.statusLine.statusCode == 200) {
        EntityUtils.toString(response.entity, Charsets.UTF_8)
    } else {
        ""
    }
}

data class Item(
    val id: String,
    val title: String,
    val image: String,
    val beginTime: Date,
    val url: String
)

fun String.toDate(pattern: String): Date {
    val sdf = SimpleDateFormat(pattern)
    return sdf.parse(this)
}

fun Date.toString(pattern: String): String {
    val sdf = SimpleDateFormat(pattern)
    return sdf.format(this)
}