package odinson

import java.nio.file.Paths
import java.util.{ ArrayList, HashMap }
import scala.collection.JavaConverters._
import org.apache.lucene.store.FSDirectory
import com.typesafe.config.ConfigValueFactory
import ai.lum.common.ConfigFactory
import ai.lum.odinson.lucene.index.OdinsonIndex
import ai.lum.odinson._

class EntryPoint {

    def mkExtractorEngine(): ExtractorEngine = {
        ExtractorEngine.fromConfig()
    }

    def mkExtractorEngine(path: String): ExtractorEngine = {
        val config = ConfigFactory.load().withValue("odinson.indexDir", ConfigValueFactory.fromAnyRef(path))
        ExtractorEngine.fromConfig(config)
    }

    def indexDocuments(docs: ArrayList[HashMap[String, Any]]): Unit = {
        val config = ConfigFactory.load()
        val index = OdinsonIndex.fromConfig(config)
        for (d <- mkDocuments(docs)) {
            index.indexOdinsonDoc(d)
        }
        index.close()
    }

    def indexDocuments(path: String, docs: ArrayList[HashMap[String, Any]]): Unit = {
        val config = ConfigFactory.load().withValue("odinson.indexDir", ConfigValueFactory.fromAnyRef(path))
        val index = OdinsonIndex.fromConfig(config)
        for (d <- mkDocuments(docs)) {
            index.indexOdinsonDoc(d)
        }
        index.close()
    }

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
        field.get("$type").toString() match {
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
            case "ai.lum.odinson.StringField" =>
                val name = field.get("name").toString()
                val string = field.get("string").toString()
                StringField(name, string)
            case "ai.lum.odinson.DateField" =>
                val name = field.get("name").toString()
                val date = field.get("date").toString()
                DateField(name, date)
            case "ai.lum.odinson.NumberField" =>
                val name = field.get("name").toString()
                val value = field.get("value").asInstanceOf[Double]
                NumberField(name, value)
            case "ai.lum.odinson.NestedField" =>
                val name = field.get("name").toString()
                val fields = field.get("fields").asInstanceOf[ArrayList[HashMap[String, Any]]].asScala.toSeq.map(mkField)
                NestedField(name, fields)
        }
    }

}
