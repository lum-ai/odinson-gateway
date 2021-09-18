package odinson

import java.util.{ ArrayList, HashMap }
import scala.collection.JavaConverters._
import ai.lum.odinson.{ Document, Sentence, Field, TokensField, GraphField }
import ai.lum.odinson.ExtractorEngine

class OdinsonEntryPoint {

    def mkMemoryIndex(docs: ArrayList[HashMap[String, Any]]): ExtractorEngine = {
        ExtractorEngine.inMemory(mkDocuments(docs))
    }

    def mkDocuments(docs: ArrayList[HashMap[String, Any]]): Seq[Document] = {
        docs.asScala.toSeq.map(mkDocument)
    }

    def mkDocument(doc: HashMap[String, Any]): Document = {
        val id = doc.get("id").toString()
        val metadata = doc.get("metadata").asInstanceOf[ArrayList[HashMap[String, Any]]].asScala.toSeq.map(mkField)
        val sentences = doc.get("sentences").asInstanceOf[ArrayList[HashMap[String, Any]]].asScala.toSeq.map(mkSentence)
        Document(id, metadata, sentences)
    }

    def mkSentence(sent: HashMap[String, Any]): Sentence = {
        val numTokens = sent.get("numTokens").asInstanceOf[Int]
        val fields = sent.get("fields").asInstanceOf[ArrayList[HashMap[String, Any]]].asScala.toSeq.map(mkField)
        Sentence(numTokens, fields)
    }

    def mkField(field: HashMap[String, Any]): Field = {
        field.get("type").toString() match {
            case "ai.lum.odinson.TokensField" =>
                val name = field.get("name").toString()
                val tokens = field.get("tokens").asInstanceOf[ArrayList[String]].asScala.toSeq
                TokensField(name, tokens)
            case "ai.lum.odinson.GraphField" =>
                val name = field.get("name").toString()
                val roots = field.get("roots").asInstanceOf[ArrayList[Int]].asScala.toSet
                val edges = field.get("edges").asInstanceOf[ArrayList[ArrayList[Any]]].asScala.toSeq.map {
                    edge => (edge.get(0).asInstanceOf[Int], edge.get(1).asInstanceOf[Int], edge.get(2).toString())
                }
                GraphField(name, edges, roots)
        }
    }

}
