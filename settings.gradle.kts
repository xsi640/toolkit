rootProject.name = "toolkit"

fun defineSubProject(name: String, path: String) {
    include(name)
    project(":$name").projectDir = file(path)
}

defineSubProject("${rootProject.name}-app", "app")
