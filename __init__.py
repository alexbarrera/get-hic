import re
import tempfile

from flask import Flask, send_file, render_template
import subprocess
import constants
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html', mess='WIP')


@app.route('/projects/')
def projects():
    return 'Projects description!'


@app.route('/projects/GGR/hic/<int:timepoint>/<string:region>')
def region(timepoint, region):
    foo1, chrom1, start1, end1, \
    foo2, chrom2, start2, end2 = re.match('(chr|)(\w+)\:(\d+)\-(\d+)\.(chr|)(\w+)\:(\d+)\-(\d+)', region).groups(0)
    # return 'Looking for HiC interaction maps: Time Point %d, regions: %s' % (timepoint, region)
    # simply create a file with the contents on demand
    outfile = "ggr_%dhs_pairs_" % timepoint + \
              ".".join(["chr%s"%chrom1, start1, end1, "chr%s"%chrom2, start2, end2]) + \
              '.txt'
    tmpfile = tempfile.NamedTemporaryFile('w')
    juicebox_error = subprocess.call(["java",
                         "-jar",
                         constants.JUICEBOX_CLT_JAR,
                         "dump",
                         "observed",
                         "KR",
                         "%s/%dHR_merged.txt.hic" % (constants.DATA_DIR, timepoint),
                         "chr%s" % chrom1,
                         "chr%s" % chrom2,
                         "BP",
                         "5000",
                         tmpfile.name
                          ])
    if juicebox_error:
        return "Error!"

    with open(outfile, 'w') as ofile:
        sort_file = subprocess.Popen(["sort", "-k1,1n", "-k2,2n", tmpfile.name], stdout=subprocess.PIPE)
        filter_awk = u"$1>%s{exit}$1>=%s && $1<=%s && $2>=%s && $2<=%s{print}" % (end1, start1, end1, start2, end2)
        print filter_awk
        filter_file = subprocess.Popen(["awk", filter_awk],
                                       stdin=sort_file.stdout,
                                       stdout=ofile)
        # sort_file.stdout.close()
        filter_file.communicate()
    return send_file(outfile, as_attachment=True)
