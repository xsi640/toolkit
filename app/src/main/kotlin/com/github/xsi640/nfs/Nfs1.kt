package com.github.xsi640.nfs

import org.apache.commons.vfs2.FileObject
import org.apache.commons.vfs2.FileSystemManager
import org.apache.commons.vfs2.VFS


class Nfs1 {
}

fun main() {
    val nfsPath = "nfs://10.10.3.28:/data1/nfs_root" // 替换为实际的NFS路径

    var fsManager: FileSystemManager? = null

    try {
        fsManager = VFS.getManager()
        val nfsFile: FileObject = fsManager.resolveFile(nfsPath)
        val children: Array<FileObject> = nfsFile.getChildren()
        for (child in children) {
            System.out.println(child.getName().getBaseName())
        }
    } catch (e: FileSystemException) {
        e.printStackTrace()
    } finally {
        if (fsManager != null) {
            try {
                fsManager.close()
            } catch (e: FileSystemException) {
                e.printStackTrace()
            }
        }
    }
}