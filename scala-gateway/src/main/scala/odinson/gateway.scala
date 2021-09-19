package odinson

import py4j.GatewayServer

object OdinsonGatewayServer {
    def main(args: Array[String]): Unit = {
        val gatewayServer = new GatewayServer(new OdinsonEntryPoint())
        gatewayServer.start()
        println("OdinsonGatewayServer started")
    }
}
