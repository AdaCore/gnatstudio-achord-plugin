# Very simple-minded test runner that allows for consistent testsuite runs.

# The environment variable ACHORD_SERVER_JAR should contain the full path
# to the Achord_Server.jar executable

tests="test_lal_analysis.py test_connection.py test_element_handling.py"

if [ "$ACHORD_SERVER_JAR" = "" ]; then
  echo "set up ACHORD_SERVER_JAR"
  exit 1
fi

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

WORKDIR=`mktemp -d`

# Copy the demo to the temporary dir
cp -R $SCRIPTPATH/../demo $WORKDIR

java -jar $ACHORD_SERVER_JAR $WORKDIR/demo > server_log 2>&1 & pid=`echo $!` 

echo "server launched, pid=$pid"

export PYTHONPATH=$SCRIPTPATH/../achord-integration:$PYTHONPATH

for t in $tests ; do
   echo "# $t"
   python $t $WORKDIR
done

kill $pid 
rm -rf $WORKDIR
