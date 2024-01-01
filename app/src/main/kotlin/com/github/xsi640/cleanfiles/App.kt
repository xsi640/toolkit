package com.github.xsi640.cleanfiles

import java.lang.Thread.sleep
import java.nio.file.FileVisitOption
import java.nio.file.Files
import kotlin.io.path.*

class App {
}

@OptIn(ExperimentalPathApi::class)
fun main() {
    val dir = "f:\\"
    val p = Path(dir)
    Files.walk(p).use {
        it.forEach {
            if (it.isDirectory())
                return@forEach
            if (it.fileName.toString() == ".DS_Store") {
                println(it.absolutePathString())
                Files.delete(it)
            }
        }
    }
}