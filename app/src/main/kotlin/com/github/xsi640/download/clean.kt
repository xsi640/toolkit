package com.github.xsi640.download

import org.apache.commons.io.FileUtils
import java.io.File
import java.nio.file.Paths
import kotlin.io.path.exists

object CleanAriaDownload {
    private const val DOWNLOAD_FOLDER = "/Volumes/private/aria2/downloads"
    private const val SAVED_FOLDER = "/Volumes/private/temp"
    private const val ARIA_EXT = ".aria2"
    private const val MOVE_SIZE = 1024 * 1024 * 500

    fun move() {
        val dir = File(DOWNLOAD_FOLDER)
        val toDir = File(SAVED_FOLDER)
        dir.listFiles()?.forEach { f ->
            if (f.isFile) {
                if (f.length() > MOVE_SIZE) {
                    FileUtils.moveFileToDirectory(f, toDir, true)
                    println("${f.name} download finish")
                }
            } else if (f.isDirectory) {
                val ariaFile = Paths.get(f.absolutePath + ARIA_EXT)
                if (!ariaFile.exists()) {
                    f.listFiles()?.forEach {
                        if (it.isFile && it.length() > MOVE_SIZE) {
                            FileUtils.moveFileToDirectory(it, toDir, true)
                            println("${it.name} download finish")
                        }
                    }
                }
            }
        }
        println("clean finish")
    }
}

fun main() {
    CleanAriaDownload.move()
}