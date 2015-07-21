import java.io.File

import org.broadinstitute.gatk.queue.QScript
import org.broadinstitute.gatk.queue.extensions.gatk._
import org.broadinstitute.gatk.queue.function.CommandLineFunction
import org.broadinstitute.gatk.queue.util.QScriptUtils._
import org.broadinstitute.gatk.utils.commandline.{Output, Input}




class Qscript_Mutect_with_SomaticDB extends QScript {

  @Argument(shortName = "project_name", required = true, doc = "list of all normal files")
  var project_name: String = "default_project"

  @Argument(shortName = "query", required = true, doc = "list of all normal files")
  var query: String = "all"

  @Argument(shortName = "evaluation_rules", required = true, doc = "evalution rules on a project level")
  var evaluation_rules: String = "tcga:ROCL,hcc:CM"

  @Argument(shortName = "sc", required = false, doc = "base scatter count")
  var scatter = 50

  def script() {

    var scatter: Int = 10

    val tumor_filename: String = "%s_tumor.list".format(project_name)
    val normal_filename: String = "%s_normal.list".format(project_name)
    val intervals_filename: String = "%s_intervals.list".format(project_name)
    val metadata_filename: String = "%s_metadata.tsv".format(project_name)

    val Ag = new AggregateBams(query, normal_filename, tumor_filename, intervals_filename, project_name, metadata_filename)
    add(Ag)


    /*
    val tumor_bams = QScriptUtils.createSeqFromFile(Ag.tumors)
    val normal_bams = QScriptUtils.createSeqFromFile(Ag.normals)
    val intervals_files = QScriptUtils.createSeqFromFile(Ag.intervals)

    for (sampleIndex <- 0 until normal_bams.size) {

      val m2 = new mutect2(tumor_bams(sampleIndex), normal_bams(sampleIndex), intervals_files(sampleIndex), scatter)
      add(m2)
    }

    val results_filename: String = "%_results.tsv"
    val submissions_filename: String = "%_submissions.tsv"

    add(new CreateAssessment(metadata_filename, results_filename, submissions_filename, evaluation_rules))

    add(new VariantAssessment(submissions_filename, query))
    */
  }

}


  case class mutect2(tumorFile: String, normalFile: String, intervalFile: String, scatter: Int) extends M2 {

    def swapExt(orig: String, ext: String) = (orig.split('.') match {
      case xs @ Array(x) => xs
      case y => y.init
    }) :+ "js" mkString "."


    this.reference_sequence = new File("/humgen/1kg/reference/human_g1k_v37_decoy.fasta")
    this.cosmic :+= new File("/home/unix/gauthier/workspaces/MuTect/b37_cosmic_v54_120711.vcf")
    this.dbsnp = new File("/humgen/gsa-hpprojects/GATK/bundle/current/b37/dbsnp_138.b37.vcf")
    this.intervalsString = List(intervalFile)
    this.interval_padding = Some(50)
    this.memoryLimit = Some(2)
    this.input_file = List(new TaggedFile(normalFile, "normal"), new TaggedFile(tumorFile, "tumor"))
    this.out = new File(swapExt(intervalFile.toString, ".vcf"))
    this.scatterCount = scatter

    //this.allowNonUniqueKmersInRef = true
    //this.minDanglingBranchLength = 2
  }


  /*
somaticdb bam_aggregate [-h] -q <query>
                             -n <normal_bam_list>
                             -t <tumor_bam_list>
                             -i <interval_list> 
                             -f <folder>
                             -m <metadata>
*/
  case class AggregateBams(query: String,
                           normal_bam_list: File,
                           tumor_bam_list: File,
                           interval_list: File,
                           folder: File,
                           metadata: String) extends CommandLineFunction {


    @Output(doc = "")
    val f: File = folder

    @Output(doc = "")
    val normals: File = normal_bam_list

    @Output(doc = "")
    val tumors: File = tumor_bam_list

    @Output(doc = "")
    val intervals: File = interval_list

    override def commandLine: String = {
      val cmd = "somaticdb bam_aggregate -q %s -n %s -t %s -i %s -f %s -m %s".format(query,
        normal_bam_list, tumor_bam_list, interval_list, folder, metadata)
      println(cmd)
      cmd
    }
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





