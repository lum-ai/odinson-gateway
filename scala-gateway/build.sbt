name := "scala-gateway"
organization := "ai.lum"
scalaVersion := "2.12.14"
assemblyJarName := "odinson-entrypoint.jar"
libraryDependencies ++= Seq(
    "ai.lum" %% "odinson-core" % "0.5.0",
)
