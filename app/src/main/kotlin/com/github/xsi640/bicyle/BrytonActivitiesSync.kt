package com.github.xsi640.bicyle

import org.apache.commons.io.FileUtils
import java.io.File
import java.text.SimpleDateFormat

class BrytonActivitiesSync {
    companion object {
        val source = "/Volumes/BRYTON/Activities"
        val target = "/Users/suyang/Desktop/activites"

        fun sync() {
            val sourceFiles = File(source).listFiles()
            val targetDirectory = File(target)
            val targetFiles = targetDirectory.listFiles()
            sourceFiles.forEach { file ->
                val name = file.name
                val sdf = SimpleDateFormat("yyMMddHHmmss")
                val time = sdf.parse(file.nameWithoutExtension)

                val sdf2 = SimpleDateFormat("yyyy-MM-dd-HH-MM-ss")
                val newName = "${sdf2.format(time)}.fit"

                val newFile = File(targetDirectory, newName)
                if (!newFile.exists()) {
                    FileUtils.copyFile(file, newFile)
                    println("copy file from:${file.absoluteFile} to:${newFile.absoluteFile}")
                }
            }
        }
    }
}

fun main() {
    BrytonActivitiesSync.sync()
}