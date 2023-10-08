import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    id("java")
    kotlin("jvm") version "1.8.22"
}

allprojects {

    apply {
        plugin("idea")
        plugin("java")
        plugin("kotlin")
    }

    group = "com.github.xsi640"
    version = "1.0.0"
    java.sourceCompatibility = JavaVersion.VERSION_1_8
    java.targetCompatibility = JavaVersion.VERSION_1_8


    val vers = mapOf(
        "commons_io" to "2.13.0",
        "commons_codec" to "1.16.0",
        "commons_lang" to "3.12.0",
        "jackson" to "2.13.5",
        "okhttp" to "4.10.0"
    )

    rootProject.extra.set("vers", vers)

    dependencies {
        implementation("commons-io:commons-io:${vers["commons_io"]}")
        implementation("commons-codec:commons-codec:${vers["commons_codec"]}")
        implementation("org.apache.commons:commons-lang3:${vers["commons_lang"]}")
        implementation("com.squareup.okhttp3:okhttp:${vers["okhttp"]}")
        implementation("com.squareup.okhttp3:logging-interceptor:${vers["okhttp"]}")

        implementation("com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:1.31")
        implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${vers["jackson"]}")
        implementation("org.jetbrains.kotlin:kotlin-reflect")
        implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
        implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.5.0")
        implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor:1.5.0")
    }

    repositories {
        mavenLocal()
        maven { url = uri("https://maven.aliyun.com/repository/central") }
    }

    tasks.withType<Test> {
        useJUnitPlatform()
    }

    tasks.withType<KotlinCompile> {
        kotlinOptions {
            freeCompilerArgs = listOf("-Xjsr305=strict")
            jvmTarget = "1.8"
        }
    }

    val jar: Jar by tasks
    jar.enabled = true
}