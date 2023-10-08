package com.github.xsi640.openfile

import java.util.*
import kotlin.io.path.Path

class App {
}

fun main() {
    val dir = Path("F:\\private\\temp")
    val files = dir.toFile().listFiles()!!.toMutableList()
    val size = files.size
    println("size: $size")
    val scan = Scanner(System.`in`)
    while (true) {
        val index = Random().nextInt(files.size)
        val file = files[index]
        Runtime.getRuntime().exec("cmd /c \"${file.absolutePath}\"")
        println(file.absolutePath)
        scan.nextLine()
    }
}