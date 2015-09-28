import java.io.{File, PrintWriter}
import scala.collection.mutable.ListBuffer
import org.broadinstitute.gatk.queue.QScript
import org.broadinstitute.gatk.queue.extensions.gatk._
import org.broadinstitute.gatk.queue.function.{CommandLineFunction, InProcessFunction}
import org.broadinstitute.gatk.queue.util.QScriptUtils
import org.broadinstitute.gatk.utils.commandline.{Output, Input}
import scala.sys.process._
import scala.reflect.io.Path




class Qscript_Mutect_with_SomaticDB extends QScript {

  @Argument(shortName = "project_name", required = true, doc = "list of all normal files")
  var project_name: String = "default_project"

  @Argument(shortName = "query", required = true, doc = "list of all normal files")
  var query: String = "all"

  @Argument(shortName = "sc", required = false, doc = "base scatter count")
  var scatter = 50


  def script() {

    val cwd = System.getProperty("user.dir")
    val project_dir: String = (Path( cwd ) / project_name).toString()

    println(project_dir)

    val tumorFilename: File = new File(project_dir,"%s_tumor.list".format(project_name))
    val normalFilename: File = new File(project_dir,"%s_normal.list".format(project_name))

    val metadataFilename: File = new File(project_dir,"%s_metadata.tsv".format(project_name))

    val mutectResultsFilename: File = new File(project_dir,"%s_mutect_results.tsv".format(project_name))

    (new File(project_dir)).mkdir()

    println("Project directory created: "+project_dir)

    println("Collecting bams")
    val cmd = normalNormalCollector(query, normalFilename, tumorFilename, metadataFilename)

    println(cmd)

    cmd !

    println("Collection complete.")

    val m2_out_files = new ListBuffer[String]

    val tumor_bams = QScriptUtils.createSeqFromFile(tumorFilename)
    val normal_bams = QScriptUtils.createSeqFromFile(normalFilename)

    for (sampleIndex <- 0 until normal_bams.size) {

        val mutect_out_dir: String = (Path( cwd ) / project_name / "mutect_results").toString()

        (new File(mutect_out_dir)).mkdir()

        val m2 = new mutect2_normal_normal(tumor_bams(sampleIndex), normal_bams(sampleIndex), scatter, mutect_out_dir.toString)

        m2.out = new File(project_dir,swapExt(tumor_bams(sampleIndex).toString,"bam", "")+swapExt(normal_bams(sampleIndex).toString,"bam", "")+"vcf")

        m2_out_files += m2.out

        add(m2)
    }

    add(new MakeStringFileList(m2_out_files, mutectResultsFilename))


    val submissionsFilename: File = new File(project_dir,"%s_submission.tsv".format(project_name))

    add(new normalNormalCreateAssessment(metadataFilename, mutectResultsFilename, submissionsFilename))

    val assessmentFilename: File = new File(project_dir,"%s_assessment.tsv".format(project_name))

    println(assessmentFilename.toString)

    add(new NormalNormalVariantAssessment(m2_out_files.map(x => new File(x)) ,submissionsFilename, query,assessmentFilename,project_dir))

    }






  case class mutect2_normal_normal(tumor: File, normal: File, scatter: Int, project_path: String)  extends MuTect {

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

    this.reference_sequence = new File("/seq/references/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta")
    this.cosmic :+= new File("/dsde/working/kcarr/b37_cosmic_v54_120711.vcf")
    this.dbsnp = List(new File("/humgen/gsa-hpprojects/GATK/bundle/current/b37/dbsnp_138.b37.vcf"))
    this.normal_panel = List(new File("/dsde/working/mutect/panel_of_normals/panel_of_normals_m2_ice/m2_406_ice_normals_ice+agilent_10bp.vcf"))
    this.memoryLimit = Some(2)
    this.input_file = List(new TaggedFile(normalFile, "normal"), new TaggedFile(tumorFile, "tumor"))
    this.out = new File(project_path, swapExt(tumorFile.toString,"bam", "vcf").toString() )
    this.scatterCount = scatter
    this.intervalsString :+= new File("/dsde/working/mutect/crsp_nn/whole_exome_illumina_coding_v1.Homo_sapiens_assembly19.targets.no_empty.interval_list")

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
       mutest normal_normal_collector -q "{'project':'CRSP'}"
                                      -o test.tsv
                                      -n normal.list
                                      -t tumor.list
*/
 def normalNormalCollector(query: String,
                   normal_bam_list: File,
                   tumor_bam_list: File,
                   tsv: String) : String = {


   val cmd: String = "mutest normal_normal_collector -q \"%s\" -n %s -t %s -o %s".format(query, normal_bam_list, tumor_bam_list, tsv)

    return(cmd)
  }



  /*
mutest assessment_file_create -t <tsv>
                                 -r <results>
                                 -o <output_file>
                                 -e <evaluation_rules>
*/
  case class normalNormalCreateAssessment(@Input tsv: File,
                              @Input results: File,
                              @Output output_file: File) extends CommandLineFunction {


    override def commandLine: String = {
      "mutest assessment_file_create -t %s -r %s -o %s -e NN".format(tsv, results, output_file)
    }
  }


  /*
mutest variant_assess -t <tsv>
                      -q <query>
                      -o <output>
*/
  case class NormalNormalVariantAssessment(@Input resultsFiles: Seq[File],
                                           @Input tsv: File,
                                           @Argument query: String,
                                           @Argument folder: File,
                                           @Output output: File) extends CommandLineFunction {

    override def commandLine: String = {
      "mutest variant_assess -t %s -q \"%s\" -o %s -d %s".format(tsv, query, output,folder)
    }
  }

}











