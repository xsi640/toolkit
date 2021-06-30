package com.github.xsi640.fanghill

import org.apache.http.client.methods.HttpPost
import org.apache.http.impl.client.HttpClients
import org.apache.http.util.EntityUtils
import org.jsoup.Jsoup
import java.net.*
import java.text.SimpleDateFormat
import java.util.*


const val CATEGORY_ID = "763149d1-4390-4200-8b32-1f6ac71d3666"
const val LIST_URL = "http://www.fscac.org/Activity/List"
const val ORDER_URL = "http://www.fscac.org/Content/order"
const val DETAIL_URL = "http://www.fscac.org/Activity/detail"
const val COOKIE =
    "__RequestVerificationToken=93qWa0mnf8SFSZwItd_sNAreAQgzrGW7znbZ_6TrDtJ6nLBiH0L4AfyFeGAaUMKSGKUWwctUquTY5sF_l_x86w2; .xCookie=DCAD8C0AF759D62DF2F91BDAD0A954B75DD9876C40012B0E03790B2656C6749256C5A4A55B2F31705EA03C8F2049D2D90E1D177F5E1E004F6441D12D69D586F517E3DAA78625AAEA4965348C16DB220494EA912691DF39136B932CC65725BFA4AB11906E06EE576F108EE8AFC98CE1D8; ASP.NET_SessionId=0ydpxo00bubvyrtvzlv1aqn4"

fun main(args: Array<String>) {
    val keyword = "小魔仙"
    var item: Item? = null
    while (item == null) {
        val exists = getCategories().firstOrNull { it.title.contains(keyword) }
        if (exists != null) {
            item = exists
        }
    }
    println("found $keyword's ticket.")
    val url = "$ORDER_URL?module=Activity&&" +
            "CategoryID=$CATEGORY_ID&&" +
            "id=${item.id}&&OrderTitle=${URLEncoder.encode(URLEncoder.encode(item.title, "UTF-8"), "UTF-8")}&&" +
            "OrderImage=${item.image}&&" +
            "OrderBeginTime=${item.beginTime.toString("yyyy/M/d HH:mm:ss").replace(" ", "%20")}&&" +
            "OrderUrl=${DETAIL_URL}?id=${item.id}"

    var result = submitOrder(url).trim()
    while (result == "0" || result == "-9") {
        result = submitOrder(url).trim()
    }
    if (result == "-1") {
        println("please check cookie.")
    } else if (result == "-2") {
        println("submit failured. already expired.")
    }
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

fun submitOrder(url: String): String {
    val httpClient = HttpClients.createDefault()
    val method = HttpPost(url)
    method.addHeader("Content-Type", "application/json; charset=utf-8")
    method.addHeader(
        "Cookie",
        COOKIE
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