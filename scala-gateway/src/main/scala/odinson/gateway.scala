package odinson

import py4j.GatewayServer

object OdinsonGateway {
    def main(args: Array[String]): Unit = {
        val gatewayServer = new GatewayServer(new OdinsonEntryPoint())
        gatewayServer.start()
        println("OdinsonGateway server started")
    }
}
