import java.io._
import scala.collection.mutable.ListBuffer
import org.broadinstitute.gatk.queue.QScript
import org.broadinstitute.gatk.queue.extensions.gatk._
import org.broadinstitute.gatk.queue.function.{CommandLineFunction, InProcessFunction}
import org.broadinstitute.gatk.queue.util.QScriptUtils
import org.broadinstitute.gatk.utils.commandline.{Output, Input}
import scala.sys.process._




class Qscript_Mutect_with_SomaticDB extends QScript {

  @Argument(shortName = "project_name", required = true, doc = "list of all normal files")
  var project_name: String = "default_project"

  @Argument(shortName = "query", required = true, doc = "list of all normal files")
  var query: String = "all"

  @Argument(shortName = "evaluation_rules", required = true, doc = "evalution rules on a project level")
  var evaluation_rules: String = "tcga:ROCL,hcc:CM"

  @Argument(shortName = "sc", required = false, doc = "base scatter count")
  var scatter = 10


  def script() {

    val tumorFilename: String = "%s_tumor.list".format(project_name)
    val normalFilename: String = "%s_normal.list".format(project_name)
    val intervalsFilename: String = "%s_intervals.list".format(project_name)
    val metadataFilename:String = "%s_metadata.tsv".format(project_name)
    val folder : String = project_name
    val resultsFilename: String = "%s_results.tsv".format(project_name)

    println("Aggretating bams")
    val cmd = AggregateBams(query, normalFilename, tumorFilename, intervalsFilename, folder, metadataFilename)

    cmd !

    println("Aggregation complete.")

    val m2_out_files = new ListBuffer[String]

    val tumor_bams = QScriptUtils.createSeqFromFile(tumorFilename)
    val normal_bams = QScriptUtils.createSeqFromFile(normalFilename)
    val intervals_files = QScriptUtils.createSeqFromFile(intervalsFilename)

    for (sampleIndex <- 0 until normal_bams.size) {

        val m2 = new mutect2(tumor_bams(sampleIndex), normal_bams(sampleIndex), intervals_files(sampleIndex), scatter)

        m2_out_files += m2.out

        add(m2)
    }

    add(new MakeStringFileList(m2_out_files, resultsFilename))


    /*

    add(new CreateAssessment(metadata_filename, results_filename, submissions_filename, evaluation_rules))

    add(new VariantAssessment(submissions_filename, query))
    */
    }



  case class mutect2(tumor: File, normal: File, interval: File, scatter: Int) extends M2 {

    /*
    def swapExt(orig: String, ext: String) = (orig.split('.') match {
      case xs @ Array(x) => xs
      case y => y.init
    }) :+ ext mkString "."
    */
    @Input(doc = "")
    val tumorFile: File = tumor

    @Input(doc = "")
    val normalFile: File = normal

    @Input(doc = "")
    val intervalFile: File = interval

    this.reference_sequence = new File("/humgen/1kg/reference/human_g1k_v37_decoy.fasta")
    this.cosmic :+= new File("/dsde/working/kcarr/b37_cosmic_v54_120711.vcf")
    this.dbsnp = new File("/humgen/gsa-hpprojects/GATK/bundle/current/b37/dbsnp_138.b37.vcf")
    this.intervalsString = List(intervalFile.toString)
    this.interval_padding = Some(50)
    this.memoryLimit = Some(2)
    this.input_file = List(new TaggedFile(normalFile, "normal"), new TaggedFile(tumorFile, "tumor"))
    this.out = new File(swapExt(tumorFile.toString,"bam", "vcf"))
    this.scatterCount = scatter

    //this.allowNonUniqueKmersInRef = true
    //this.minDanglingBranchLength = 2
  }


  case class MakeStringFileList ( stringList: Seq[String], outputFilename: File) extends InProcessFunction {

    @Output(doc = "")
    val f: File = outputFilename

    override def run (): Unit ={
      writeList(stringList, outputFilename)
    }

    def writeList (inFile : Seq[String], outFile : File) = {
      val writer = new PrintWriter(new File(outFile.getAbsolutePath))
      writer.write(inFile.mkString("\n"))
      writer.close()
    }
  }


  /*
somaticdb bam_aggregate [-h] -q <query>
                             -n <normal_bam_list>
                             -t <tumor_bam_list>
                             -i <interval_list>
                             -f <folder>
                             -m <metadata>
*/
 def AggregateBams(query: String,
                   normal_bam_list: File,
                   tumor_bam_list: File,
                   interval_list: File,
                   folder: File,
                   metadata: String) : String = {


   val cmd: String = "somaticdb bam_aggregate -q \"%s\" -n %s -t %s -i %s -f %s -m %s".format(query, normal_bam_list, tumor_bam_list, interval_list, folder, metadata)

    return(cmd)
  }



  /*
somaticdb assessment_file_create -t <tsv>
                                 -r <results>
                                 -o <output_file>
                                 -e <evaluation_rules>
*/
  case class CreateAssessment(tsv: String,
                              results: String,
                              output_file: String,
                              rules: String) extends CommandLineFunction {
    @Input(doc = "")
    val t: String = tsv

    @Input(doc = "")
    val r: String = results

    @Output(doc = "")
    val o: String = output_file

    @Input(doc = "")
    val e: String = rules

    override def commandLine: String = {
      "somaticdb assessment_file_create -t %s -r %s -o %s -e %s".format(t, r, o, e)
    }
  }


  /*
somaticdb variant_assess -t <tsv>
                         -q <query>
*/
  case class VariantAssessment(tsv: String,
                               query: String) extends CommandLineFunction {
    @Input(doc = "")
    val t: String = tsv

    @Input(doc = "")
    val q: String = query

    override def commandLine: String = {
      "somaticdb variant_assess -t %s -q %s".format(t, q)
    }
  }

}











