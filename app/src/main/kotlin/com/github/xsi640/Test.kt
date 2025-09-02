package com.github.xsi640

class Test {
}

fun main() {
    println("print:")
    for (i in 0..5) {
        Thread.sleep(1000)
        print("\ri:$i")
    }
    println("\nfinish.")
}