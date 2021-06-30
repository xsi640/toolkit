import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.5.0"
}

allprojects {

    apply {
        plugin("idea")
        plugin("kotlin")
    }

    group = "com.github.xsi640"
    version = "1.0.0"
    java.sourceCompatibility = JavaVersion.VERSION_1_8
    java.targetCompatibility = JavaVersion.VERSION_1_8


    val vers = mapOf(
        "commons_io" to "2.8.0",
        "commons_codec" to "1.15",
        "commons_lang" to "3.12.0",
        "apache_httpclient" to "4.5.13",
        "jackson" to "2.11.3"
    )

    rootProject.extra.set("vers", vers)

    dependencies {
        implementation("commons-io:commons-io:${vers["commons_io"]}")
        implementation("commons-codec:commons-codec:${vers["commons_codec"]}")
        implementation("org.apache.commons:commons-lang3:${vers["commons_lang"]}")
        implementation("org.apache.httpcomponents:httpclient:${vers["apache_httpclient"]}")

        implementation("org.jetbrains.kotlin:kotlin-reflect")
        implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    }

    val user = System.getProperty("repoUser")
    val pwd = System.getProperty("repoPassword")

    repositories {
        mavenLocal()
        maven {
            credentials {
                username = user
                password = pwd
                isAllowInsecureProtocol = true
            }
            url = uri("http://nexus.suyang.home/repository/maven-group/")
//            url = uri("http://172.16.11.231:8081/nexus/repository/maven2-group/")
        }
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