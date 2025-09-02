package com.github.xsi640.copy

import com.fasterxml.jackson.databind.annotation.JsonAppend.Prop
import jcifs.CIFSContext
import jcifs.SmbResource
import jcifs.config.BaseConfiguration
import jcifs.config.PropertyConfiguration
import jcifs.context.BaseContext
import jcifs.smb.NtlmPasswordAuthenticator
import jcifs.smb.SmbFile
import jcifs.smb.SmbFileInputStream
import java.io.File
import java.io.FileOutputStream
import java.util.Properties

class Copy {
}

val SMB_FILE = "smb://192.168.1.1/aria2"
val SMB_USERNAME = System.getenv("SMB_ARIA2_USERNAME")
val SMB_PASSWORD = System.getenv("SMB_ARIA2_PASSWORD")
val SAVE_DIRECTORY = "F:\\private\\"
val SAVE_FILE_SIZE = 100 * 1024 * 1024
val SAVE_FILE_EXTNAME = ".mp4"

fun main() {
    val p = Properties()
    p["jcifs.smb.client.enableSMB2"] = true
    p["jcifs.smb.client.dfs.disabled"] = true
    val config = PropertyConfiguration(p)
    val baseCtx = BaseContext(config)
    val cifsContext = baseCtx.withCredentials(
        NtlmPasswordAuthenticator(SMB_USERNAME, SMB_PASSWORD)
    )
    val smbFile = SmbFile(SMB_FILE, cifsContext)
    if (smbFile.exists()) {
        val files = mutableListOf<SmbFile>()
        val directories = mutableListOf<SmbFile>()
        smbFile.listFiles().forEach {
            if (it.isFile) {
                files.add(it)
            } else {
                directories.add(it)
            }
        }
        val copyDirectory = mutableListOf<SmbFile>()
        directories.forEach { dir ->
            val name = dir.locator.uncPath.trim('\\')
            if (files.none { it.locator.uncPath.trim('\\') == "$name.aria2" }) {
                copyDirectory.add(dir)
            }
        }
        copyDirectory.forEach { dir ->
            dir.listFiles().filter {
                it.contentLengthLong > SAVE_FILE_SIZE &&
                        it.locator.uncPath.trim('\\').lastIndexOf(SAVE_FILE_EXTNAME, ignoreCase = true) > 0
            }.forEach { file ->
                copy(file, cifsContext)
            }
            dir.delete()
            println("delete directory ${dir.uncPath}")
        }
    }
}

fun copy(smbFile: SmbFile, cifsContext: CIFSContext) {
    val saveFile = File(SAVE_DIRECTORY, smbFile.locator.uncPath.substringAfterLast('\\').trim('\\'))
    println("copy file ${saveFile.name}")
    if (saveFile.exists()) {
        println("file exists. skip.")
        return
    }
    var current = 0L
    val total = smbFile.length()
    SmbFileInputStream(smbFile).use { smbInputStream ->
        FileOutputStream(saveFile).use { fileOutputStream ->
            val buffer = ByteArray(1024000)
            var bytesRead: Int

            while (smbInputStream.read(buffer).also { bytesRead = it } != -1) {
                fileOutputStream.write(buffer, 0, bytesRead)
                current += bytesRead
                print("\rcopied file $current/$total...")
            }
            fileOutputStream.flush()
        }
    }
    println("\nfinished....${saveFile.name}")
}
